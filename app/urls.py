# app/urls.py
from django.urls import path
from django.views.generic import TemplateView 
from .views import *

app_name = "app" # Vamos usar 'app' para consistência com o reverse_lazy nas views

urlpatterns = [
    # --- ROTAS DE CLIENTES ---
    
    # 1. Lista de Clientes (Página Principal)
    path('clientes/', ClientListView.as_view(), name='client_list'),

    # 2. Página para escolher entre PF ou PJ antes de criar um novo cliente
    path('clientes/novo/', 
         TemplateView.as_view(template_name='clients/client_select_type.html'), 
         name='client_select_type'),

    # 3. Rotas de Criação
    path('clientes/novo/pf/', PessoaFisicaCreateView.as_view(), name='client_create_pf'),
    path('clientes/novo/pj/', PessoaJuridicaCreateView.as_view(), name='client_create_pj'),
    
    # 4. Rotas de Edição (Update)
    #    <int:pk> é um parâmetro dinâmico que captura o ID do cliente
    path('clientes/pf/<int:pk>/editar/', PessoaFisicaUpdateView.as_view(), name='client_update_pf'),
    path('clientes/pj/<int:pk>/editar/', PessoaJuridicaUpdateView.as_view(), name='client_update_pj'),

    # 5. Rotas de Exclusão (Delete)
    path('clientes/pf/<int:pk>/excluir/', PessoaFisicaDeleteView.as_view(), name='client_delete_pf'),
    path('clientes/pj/<int:pk>/excluir/', PessoaJuridicaDeleteView.as_view(), name='client_delete_pj'),

    # 6. Produtos

    path("categoria/<slug:slug>/", produtos_por_categoria, name="categoria"),

    # DETALHES DO PRODUTO
    path("produto/<int:id>/", produto_detalhes, name="produto_detalhes"),
    path("produtos/novo/", ProdutoCreateView.as_view(), name="produto_novo"),

    # --- CARRINHO ---
    path("carrinho/", carrinho_view, name="carrinho"),
    path("carrinho/add/", add_carrinho, name="add_carrinho"),
    path("carrinho/remove/<int:id>/", remove_carrinho, name="remove_carrinho"),
    path("carrinho/update/", update_carrinho, name="update_carrinho"),
    path("carrinho/clear/", clear_carrinho, name="clear_carrinho"),

    path("checkout/", checkout, name="checkout"),

]