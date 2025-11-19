from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import PessoaFisica, PessoaJuridica, Categoria, Produto, Pedido, ItemPedido
from .forms import PessoaFisicaForm, PessoaJuridicaForm, ProdutoForm   # ← IMPORT CORRIGIDO
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .cart import Cart
# IMPORTS de usuário/cadastro
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# ==========================
#  DECORATORS
# ==========================

def is_staff_check(user):
    return user.is_staff

# Decorator direto (facilita)
staff_required = user_passes_test(lambda u: u.is_staff, login_url='login')


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
        "request": request,
    })


def produtos_por_categoria(request, slug):
    categorias = Categoria.objects.all()
    categoria = get_object_or_404(Categoria, slug=slug)
    produtos_qs = Produto.objects.filter(categoria=categoria).order_by('-id')

    paginator = Paginator(produtos_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, "loja/home.html", {
        "categorias": categorias,
        "produtos": page_obj.object_list,
        "categoria_ativa": slug,
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "request": request,
    })


def produto_detalhes(request, id):
    produto = get_object_or_404(Produto, id=id)
    relacionados = Produto.objects.filter(categoria=produto.categoria).exclude(id=produto.id)[:8]

    return render(request, "loja/produto_detalhes.html", {
        "produto": produto,
        "relacionados": relacionados,
    })


# ==========================
#  PERFIL
# ==========================

@login_required
def profile_view(request):
    return render(request, "users/profile.html")


# ==========================
#  CADASTRO DE USUÁRIO
# ==========================

@method_decorator(staff_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        # user.is_staff = True  # Ative se quiser liberar staff direto
        user.save()
        return super().form_valid(form)


# ==========================
#  CLIENTES
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
#  PRODUTOS (CADASTRO)
# ==========================

@method_decorator(staff_required, name='dispatch')
class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "loja/produto_form.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        return context


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

def clear_carrinho(request):
    cart = Cart(request)
    cart.clear()
    return redirect("app:carrinho")

def checkout(request):
    carrinho = request.session.get("carrinho", {})

    if not carrinho:
        messages.error(request, "Seu carrinho está vazio!")
        return redirect("app:carrinho")

    total = sum(item["preco"] * item["qtd"] for item in carrinho.values())

    if request.method == "POST":

        tipo = request.POST.get("tipo_cliente")

        pessoa_pf = None
        pessoa_pj = None

        # 🔍 Identificar PF
        if tipo == "PF":
            cpf = request.POST.get("cpf").replace(".", "").replace("-", "")
            try:
                pessoa_pf = PessoaFisica.objects.get(cpf=cpf)
            except PessoaFisica.DoesNotExist:
                return render(request, "checkout.html", {
                    "total": total,
                    "error": "CPF não encontrado no sistema. Cadastre a pessoa física primeiro."
                })

        # 🔍 Identificar PJ
        if tipo == "PJ":
            cnpj = request.POST.get("cnpj").replace(".", "").replace("/", "").replace("-", "")
            try:
                pessoa_pj = PessoaJuridica.objects.get(cnpj=cnpj)
            except PessoaJuridica.DoesNotExist:
                return render(request, "checkout.html", {
                    "total": total,
                    "error": "CNPJ não encontrado no sistema. Cadastre a empresa primeiro."
                })

        # Criar o Pedido no banco
        pedido = Pedido.objects.create(
            tipo_cliente=tipo,
            pessoa_fisica=pessoa_pf,
            pessoa_juridica=pessoa_pj,
            vendedor=request.user,
            total=total
        )

        # Criar itens
        for id_prod, item in carrinho.items():
            produto = Produto.objects.get(id=id_prod)
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=item["qtd"],
                preco_unitario=item["preco"]
            )

        # Limpar carrinho
        request.session["carrinho"] = {}
        messages.success(request, "Compra concluída com sucesso!")

        return redirect("home")

    return render(request, "checkout.html", { "total": total })