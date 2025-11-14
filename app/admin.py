# app/admin.py
from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica # Importe os novos models

# Registre os novos models no admin
admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)