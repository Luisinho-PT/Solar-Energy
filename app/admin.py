# app/admin.py
from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica, Produto, Categoria # Importe os novos models

# Registre os novos models no admin
admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)
admin.site.register(Produto)
admin.site.register(Categoria)