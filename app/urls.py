from django.urls import path
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views # Importante para Login/Logout
from .views import *

app_name = "app"

urlpatterns = [
    # --- AUTENTICAÇÃO E CADASTRO (NOVO) ---
    
    # Login e Logout
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='app:loja_home'), name='logout'),

    # Cadastro Público (Cliente se cadastra)
    path('cadastro/', cadastro_selector, name='cadastro_selector'), # Tela de escolha: PF ou PJ?
    path('cadastro/pf/', cadastro_pf, name='cadastro_pf'),
    path('cadastro/pj/', cadastro_pj, name='cadastro_pj'),


    # --- ROTAS DE CLIENTES (ADMINISTRAÇÃO) ---
    # Estas rotas continuam existindo para o Staff gerenciar clientes se necessário
    
    path('clientes/', ClientListView.as_view(), name='client_list'),
    path('clientes/novo/', TemplateView.as_view(template_name='clients/client_select_type.html'), name='client_select_type'),
    path('clientes/novo/pf/', PessoaFisicaCreateView.as_view(), name='client_create_pf'),
    path('clientes/novo/pj/', PessoaJuridicaCreateView.as_view(), name='client_create_pj'),
    path('clientes/pf/<int:pk>/editar/', PessoaFisicaUpdateView.as_view(), name='client_update_pf'),
    path('clientes/pj/<int:pk>/editar/', PessoaJuridicaUpdateView.as_view(), name='client_update_pj'),
    path('clientes/pf/<int:pk>/excluir/', PessoaFisicaDeleteView.as_view(), name='client_delete_pf'),
    path('clientes/pj/<int:pk>/excluir/', PessoaJuridicaDeleteView.as_view(), name='client_delete_pj'),


    # --- ROTAS DE LOJA / PRODUTOS ---

    # Adicionei a home aqui, assumindo que existe uma view 'loja_home'
    path('', loja_home, name='loja_home'), 

    path("categoria/<slug:slug>/", produtos_por_categoria, name="categoria"),
    path("produto/<int:id>/", produto_detalhes, name="produto_detalhes"),
    path("produtos/novo/", ProdutoCreateView.as_view(), name="produto_novo"),
    
    # Perfil do Usuário
    path("perfil/", profile_view, name="profile_view"),

    # --- CARRINHO ---
    path("carrinho/", carrinho_view, name="carrinho"),
    path("carrinho/add/", add_carrinho, name="add_carrinho"),
    path("carrinho/remove/<int:id>/", remove_carrinho, name="remove_carrinho"),
    path("carrinho/update/", update_carrinho, name="update_carrinho"),
    path("carrinho/clear/", clear_carrinho, name="clear_carrinho"),

    # --- CHECKOUT E PAGAMENTO (STRIPE) ---
    path("checkout/", checkout, name="checkout"),
    path("pagamento/sucesso/", pagamento_sucesso, name="pagamento_sucesso"),
    path("pagamento/cancelado/", pagamento_cancelado, name="pagamento_cancelado"),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
]