# app/urls.py
from django.urls import path
from django.views.generic import TemplateView 
from .views import (
    ClientListView, 
    PessoaFisicaCreateView, # Nova
    PessoaJuridicaCreateView # Nova
)

app_name = "clients"

urlpatterns = [
    # Rota da Lista (agora mostra 2 tabelas)
    path('clientes/', ClientListView.as_view(), name='client_list'),

    # Rota de Seleção (continua igual)
    path('clientes/novo/selecionar/', 
         TemplateView.as_view(template_name='clients/client_select_type.html'), 
         name='client_select_type'),

    # --- NOVAS ROTAS DE CRIAÇÃO ---
    # Não há mais query parameter (?tipo=pf)
    path('clientes/novo/pf/', PessoaFisicaCreateView.as_view(), name='client_create_pf'),
    path('clientes/novo/pj/', PessoaJuridicaCreateView.as_view(), name='client_create_pj'),
    
    # ... Você precisará criar rotas de update/delete para PF e PJ ...
]