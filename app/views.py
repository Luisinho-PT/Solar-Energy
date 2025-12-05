import stripe
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail 

# Imports locais
from .models import PessoaFisica, PessoaJuridica, Categoria, Produto, Pedido, ItemPedido
from .forms import (
    PessoaFisicaForm, PessoaJuridicaForm, ProdutoForm, 
    ClientePFRegisterForm, ClientePJRegisterForm 
)
from .cart import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


# ==========================
#  DECORATORS
# ==========================

def is_staff_check(user):
    return user.is_staff

staff_required = user_passes_test(lambda u: u.is_staff, login_url='app:login')

def enviar_comprovante_email(pedido):
    """
    Envia um recibo simples por e-mail para o cliente após pagamento confirmado.
    """
    assunto = f"Comprovante do Pedido #{pedido.id} - Pagamento Confirmado"
    
    # Determina o nome do cliente e e-mail de destino
    if pedido.pessoa_fisica:
        nome_cliente = pedido.pessoa_fisica.name
        email_destino = pedido.pessoa_fisica.email or pedido.pessoa_fisica.user.email
    elif pedido.pessoa_juridica:
        nome_cliente = pedido.pessoa_juridica.company_name
        email_destino = pedido.pessoa_juridica.email or pedido.pessoa_juridica.user.email
    else:
        # Se não tiver vínculo direto (caso raro), tenta pegar do User
        return 

    # Monta o corpo do e-mail
    mensagem = f"""
    Olá, {nome_cliente}!

    Seu pagamento foi confirmado com sucesso.
    Segue abaixo o resumo do seu pedido:

    ------------------------------------------
    PEDIDO: #{pedido.id}
    TOTAL PAGO: R$ {pedido.total:.2f}
    STATUS: Confirmado
    FORMA DE PAGAMENTO: Stripe (Cartão de Crédito)
    ------------------------------------------
    Itens do Pedido:
    """
    # Lista os itens (ajuste 'itempedido_set' se seu related_name for diferente)
    # Se você definiu related_name='itens' no model ItemPedido, use pedido.itens.all()
    # Se não definiu nada, o padrão do Django é pedido.itempedido_set.all()
    itens = getattr(pedido, 'itens', getattr(pedido, 'itempedido_set', None))
    
    if itens:
        for item in itens.all():
            mensagem += f"\n - {item.quantidade}x {item.produto.nome} (R$ {item.preco_unitario})"
    
    mensagem += "\n\nObrigado por comprar conosco!"

    try:
        send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
            fail_silently=False,
        )
        print(f"✅ E-mail de comprovante enviado para {email_destino}")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

# ==========================
#  CADASTRO DE STAFF / ADMIN
# ==========================

@method_decorator(staff_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('app:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)


# ==========================
#  CADASTRO PÚBLICO
# ==========================

def cadastro_selector(request):
    return render(request, 'clients/client_select_type.html')

def cadastro_pf(request):
    if request.user.is_authenticated:
        return redirect('app:loja_home')

    if request.method == 'POST':
        form = ClientePFRegisterForm(request.POST)
        if form.is_valid():
            pessoa = form.save()
            login(request, pessoa.user)
            messages.success(request, f"Bem-vindo, {pessoa.name}!")
            return redirect('app:loja_home')
    else:
        form = ClientePFRegisterForm()
    
    return render(request, 'clients/client_form.html', {'form': form})

def cadastro_pj(request):
    if request.user.is_authenticated:
        return redirect('app:loja_home')

    if request.method == 'POST':
        form = ClientePJRegisterForm(request.POST)
        if form.is_valid():
            pessoa = form.save()
            login(request, pessoa.user)
            messages.success(request, f"Bem-vindo, {pessoa.company_name}!")
            return redirect('app:loja_home')
    else:
        form = ClientePJRegisterForm()
    
    return render(request, 'clients/client_form.html', {'form': form})


# ==========================
#  CHECKOUT (CORRIGIDO PARA O SEU CART.PY)
# ==========================

@login_required(login_url='app:login')
def checkout(request):
    # 1. Instancia a classe Cart (ela sabe onde os dados estão)
    cart_obj = Cart(request)
    
    # 2. Pega o dicionário interno (self.cart)
    carrinho_dict = cart_obj.cart 

    # 3. Verifica se está vazio
    if not carrinho_dict:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect("app:carrinho")

    # 4. Usa o método da classe para calcular total (mais seguro)
    total_decimal = cart_obj.get_total()
    
    # --- IDENTIFICAÇÃO DO CLIENTE ---
    user = request.user
    pessoa_pf = None
    pessoa_pj = None
    tipo_cliente = None

    if hasattr(user, 'pessoa_fisica'):
        pessoa_pf = user.pessoa_fisica
        tipo_cliente = "PF"
    elif hasattr(user, 'pessoa_juridica'):
        pessoa_pj = user.pessoa_juridica
        tipo_cliente = "PJ"
    else:
        # Se for admin testando, cai aqui
        messages.error(request, "Seu usuário não possui perfil de cliente (PF ou PJ).")
        return redirect("app:profile_view")

    # --- PROCESSAMENTO ---
    if request.method == "POST":
        # Cria o pedido no banco
        pedido = Pedido.objects.create(
            tipo_cliente=tipo_cliente,
            pessoa_fisica=pessoa_pf,
            pessoa_juridica=pessoa_pj,
            vendedor=None,
            total=total_decimal,
            pago=False 
        )

        line_items_stripe = []

        # Itera sobre os itens do dicionário
        for id_prod, item in carrinho_dict.items():
            produto = get_object_or_404(Produto, id=id_prod)
            
            # ATENÇÃO: Aqui usamos item["quantidade"] conforme seu cart.py
            qtd = int(item["quantidade"])
            preco = float(item["preco"])

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=qtd,
                preco_unitario=preco
            )

            # Prepara dados para o Stripe
            line_items_stripe.append({
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': int(preco * 100), # Stripe usa centavos
                    'product_data': {
                        'name': produto.nome,
                    },
                },
                'quantity': qtd,
            })

        base_url = request.build_absolute_uri('/')[:-1] 
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items_stripe,
                mode='payment',
                success_url=f"{base_url}/pagamento/sucesso/",
                cancel_url=f"{base_url}/pagamento/cancelado/",
                client_reference_id=pedido.id,
                customer_email=user.email
            )

            pedido.stripe_checkout_id = checkout_session.id
            pedido.save()

            # Redireciona para o Stripe
            return redirect(checkout_session.url, code=303)
        
        except Exception as e:
            messages.error(request, f"Erro no Stripe: {e}")
            return redirect("app:carrinho")

    cliente_nome = pessoa_pf.name if pessoa_pf else pessoa_pj.company_name
    
    return render(request, "checkout.html", {
        "total": total_decimal,
        "cliente_nome": cliente_nome,
        "tipo_cliente": tipo_cliente
    })


# ==========================
#  LOJA / PRODUTOS
# ==========================

def loja_home(request):
    categorias = Categoria.objects.all()
    q = request.GET.get('q', '').strip()
    produtos_qs = Produto.objects.all().order_by('-id')

    if q:
        produtos_qs = produtos_qs.filter(nome__icontains=q) | produtos_qs.filter(descricao__icontains=q)

    categoria_slug = request.GET.get('categoria') or None
    if categoria_slug:
        produtos_qs = produtos_qs.filter(categoria__slug=categoria_slug)

    paginator = Paginator(produtos_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "loja/home.html", {
        "categorias": categorias,
        "produtos": page_obj.object_list,
        "categoria_ativa": categoria_slug,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
    })


def produtos_por_categoria(request, slug):
    return loja_home(request)


def produto_detalhes(request, id):
    produto = get_object_or_404(Produto, id=id)
    relacionados = Produto.objects.filter(categoria=produto.categoria).exclude(id=produto.id)[:4]
    return render(request, "loja/produto_detalhes.html", {
        "produto": produto,
        "relacionados": relacionados,
    })


# ==========================
#  PERFIL
# ==========================

@login_required
def profile_view(request):
    pf = getattr(request.user, 'pessoa_fisica', None)
    pj = getattr(request.user, 'pessoa_juridica', None)
    
    pedidos = Pedido.objects.filter(
        pessoa_fisica=pf
    ) if pf else Pedido.objects.filter(
        pessoa_juridica=pj
    ) if pj else []

    return render(request, "users/profile.html", {
        "cliente": pf or pj,
        "pedidos": pedidos
    })


# ==========================
#  CLIENTES (STAFF ONLY)
# ==========================

@method_decorator(staff_required, name='dispatch')
class ClientListView(ListView):
    model = PessoaFisica
    template_name = 'clients/client_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pf_clients'] = PessoaFisica.objects.all()
        context['pj_clients'] = PessoaJuridica.objects.all()
        return context

@method_decorator(staff_required, name='dispatch')
class PessoaFisicaCreateView(CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('app:client_list')

@method_decorator(staff_required, name='dispatch')
class PessoaJuridicaCreateView(CreateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('app:client_list')

@method_decorator(staff_required, name='dispatch')
class PessoaFisicaUpdateView(UpdateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('app:client_list')

@method_decorator(staff_required, name='dispatch')
class PessoaJuridicaUpdateView(UpdateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('app:client_list')

@method_decorator(staff_required, name='dispatch')
class PessoaFisicaDeleteView(DeleteView):
    model = PessoaFisica
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('app:client_list')

@method_decorator(staff_required, name='dispatch')
class PessoaJuridicaDeleteView(DeleteView):
    model = PessoaJuridica
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('app:client_list')


# ==========================
#  PRODUTOS (STAFF)
# ==========================

@method_decorator(staff_required, name='dispatch')
class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "loja/produto_form.html"
    success_url = reverse_lazy('app:loja_home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context


# ==========================
#  CARRINHO & UTILS
# ==========================

def carrinho_view(request):
    cart = Cart(request)
    return render(request, "loja/carrinho.html", {
        "cart": list(cart),
        "total": cart.get_total(),
        "qtd_total": cart.count_items(),
    })

def add_carrinho(request):
    if request.method == "POST":
        produto_id = request.POST.get("produto_id")
        quantidade = int(request.POST.get("quantidade", 1))
        cart = Cart(request)
        cart.add(produto_id, quantidade)
        return redirect("app:carrinho")
    return redirect("app:loja_home")

def remove_carrinho(request, id):
    cart = Cart(request)
    cart.remove(id)
    return redirect("app:carrinho")

def update_carrinho(request):
    if request.method == "POST":
        produto_id = request.POST["produto_id"]
        quantidade = int(request.POST["quantidade"])
        cart = Cart(request)
        cart.update(produto_id, quantidade)
        return redirect("app:carrinho")
    return redirect("app:carrinho")

def clear_carrinho(request):
    cart = Cart(request)
    cart.clear()
    return redirect("app:carrinho")

def pagamento_sucesso(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "loja/pagamento_sucesso.html")

def pagamento_cancelado(request):
    return render(request, "loja/pagamento_cancelado.html")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        pedido_id = session.get('client_reference_id')
        if pedido_id:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                pedido.pago = True 
                pedido.save()
            except Pedido.DoesNotExist:
                pass
    return HttpResponse(status=200)