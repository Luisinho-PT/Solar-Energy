from django.urls import path
from .views import (
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView
)

app_name = "clients"

urlpatterns = [
    path('clientes/', ClientListView.as_view(), name='client_list'),
    path('clientes/novo/', ClientCreateView.as_view(), name='client_create'),
    path('clientes/<int:pk>/editar/', ClientUpdateView.as_view(), name='client_edit'),
    path('clientes/<int:pk>/excluir/', ClientDeleteView.as_view(), name='client_delete'),
]

