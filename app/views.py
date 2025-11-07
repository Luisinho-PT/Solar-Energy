from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import (
    PessoaFisica, PessoaJuridica,
    Product, Category, Brand
)
from .forms import PessoaFisicaForm, PessoaJuridicaForm

# --- Importações de Segurança ---
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

# --- Define a regra: "Usuário deve ser staff (admin)" ---
def is_staff_check(user):
    return user.is_staff

# --- 1. VIEWS DA LOJA (PÚBLICAS) ---
# (Estas views NÃO têm o decorador)

class ProductListView(ListView):
    """
    View para listar todos os produtos ou
    filtrar produtos por categoria. (Homepage)
    """
    model = Product
    template_name = 'store/product_list.html' # Caminho: app/templates/store/product_list.html
    context_object_name = 'products'
    paginate_by = 12 

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = Product.objects.filter(category__slug=category_slug, available=True)
        else:
            queryset = Product.objects.filter(available=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_slug'] = self.kwargs.get('category_slug')
        return context

class ProductDetailView(DetailView):
    """
    View para mostrar a página de detalhes de um 
    único produto.
    """
    model = Product
    template_name = 'store/product_detail.html' # Caminho: app/templates/store/product_detail.html
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs.get('id'), 
                                      slug=self.kwargs.get('slug'), 
                                      available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category, available=True
        ).exclude(id=self.object.id)[:4]
        return context

# --- 2. VIEWS DE CLIENTES (PROTEGIDAS POR ADMIN) ---

# --- ESTA É A SINTAXE CORRIGIDA ---
# Aplicamos o decorador diretamente na classe, especificando o método 'dispatch'
@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class ClientListView(ListView):
    model = PessoaFisica
    template_name = 'clients/client_list.html' # Caminho: app/templates/clients/client_list.html
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pf_clients'] = PessoaFisica.objects.all()
        context['pj_clients'] = PessoaJuridica.objects.all()
        return context

@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class PessoaFisicaCreateView(CreateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    template_name = 'clients/client_form_pf.html' # Caminho: app/templates/clients/client_form_pf.html
    success_url = reverse_lazy('app:client_list')

@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class PessoaJuridicaCreateView(CreateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    template_name = 'clients/client_form_pj.html' # Caminho: app/templates/clients/client_form_pj.html
    success_url = reverse_lazy('app:client_list')

@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class PessoaFisicaUpdateView(UpdateView):
    model = PessoaFisica
    form_class = PessoaFisicaForm
    template_name = 'clients/client_form_pf.html' # Reutiliza o template
    success_url = reverse_lazy('app:client_list')

@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class PessoaJuridicaUpdateView(UpdateView):
    model = PessoaJuridica
    form_class = PessoaJuridicaForm
    template_name = 'clients/client_form_pj.html' # Reutiliza o template
    success_url = reverse_lazy('app:client_list')

@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class PessoaFisicaDeleteView(DeleteView):
    model = PessoaFisica
    template_name = 'clients/client_confirm_delete.html' # Caminho: app/templates/clients/client_confirm_delete.html
    success_url = reverse_lazy('app:client_list')

@method_decorator(user_passes_test(is_staff_check, login_url='login'), name='dispatch')
class PessoaJuridicaDeleteView(DeleteView):
    model = PessoaJuridica
    template_name = 'clients/client_confirm_delete.html' # Reutiliza o template
    success_url = reverse_lazy('app:client_list')