from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria
from django.utils.text import slugify

CATS = [
    "Inversores",
    "Cabos",
    "Estruturas Inox",
    "Parafusos",
    "Baterias",
    "Estruturas Galvanizadas",
    "Módulos",
    "Componentes Elétricos",
]

@receiver(post_migrate)
def criar_categorias_default(sender, **kwargs):
    if sender.name != "app":
        return
    for nome in CATS:
        Categoria.objects.get_or_create(nome=nome, slug=slugify(nome))
