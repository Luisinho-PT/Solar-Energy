from django.core.management.base import BaseCommand
from app.models import Categoria

class Command(BaseCommand):
    help = "Cria automaticamente as 5 categorias fixas"

    def handle(self, *args, **kwargs):
        categorias = [
            ("inversores", "Inversores"),
            ("cabos", "Cabos"),
            ("estruturas", "Estruturas Inox"),
            ("parafusos", "Parafusos"),
            ("baterias", "Baterias"),
        ]

        for slug, nome in categorias:
            obj, created = Categoria.objects.get_or_create(slug=slug, defaults={"nome": nome})
            status = "Criada" if created else "Já existe"
            self.stdout.write(self.style.SUCCESS(f"{status}: {nome}"))
