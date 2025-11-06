from django.urls import path
from django.views.generic import TemplateView 
from .views import (
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView
)

app_name = "clients"

urlpatterns = [
    # Nova Rota: A página que pergunta "Pessoa Física ou Jurídica?"
    path('clientes/novo/selecionar/', TemplateView.as_view(template_name='clients/client_select_type.html'), name='client_select_type'),

    # Rota Existente: A página do formulário (agora receberá ?tipo=pf ou ?tipo=pj)
    path('clientes/novo/', ClientCreateView.as_view(), name='client_create'),
    
    path('clientes/', ClientListView.as_view(), name='client_list'),
    path('clientes/<int:pk>/editar/', ClientUpdateView.as_view(), name='client_edit'),
    path('clientes/<int:pk>/excluir/', ClientDeleteView.as_view(), name='client_delete'),
]