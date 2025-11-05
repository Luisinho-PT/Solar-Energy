# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

class Client(models.Model):
    TYPE_PF = 'PF'
    TYPE_PJ = 'PJ'
    CLIENT_TYPE_CHOICES = [
        (TYPE_PF, 'Pessoa Física'),
        (TYPE_PJ, 'Pessoa Jurídica'),
    ]

    client_type = models.CharField(max_length=2, choices=CLIENT_TYPE_CHOICES, default=TYPE_PF)
    # Campos comuns
    name = models.CharField(_('Nome'), max_length=150)  # para PF = nome, para PJ = contato/responsável ou nome fantasia
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    phone = models.CharField(_('Telefone Principal'), max_length=15, blank=True, null=True)
    phone2 = models.CharField(_('Telefone Secundário'), max_length=15, blank=True, null=True) #Opcional
    cep = models.CharField(_('CEP'), max_length=9, blank=True, null=True)
    logradouro = models.CharField(_('Logradouro'), max_length=150, blank=True, null=True)
    numero = models.CharField(_('Número'), max_length=10, blank=True, null=True)
    complement = models.CharField(_('Complemento'), max_length=50, blank=True, null=True) # Opcional
    bairro = models.CharField(_('Bairro'), max_length=80, blank=True, null=True)
    cidade = models.CharField(_('Cidade'), max_length=100, blank=True, null=True)
    estado = models.CharField(_('Estado'), max_length=2, blank=True, null=True)
    pais = models.CharField(_('País'), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # PF-specific
    cpf = models.CharField(_('CPF'), max_length=14, blank=True, null=True, unique=True)
    rg = models.CharField(_('RG'), max_length=20, blank=True, null=True) # Opcional
    birth_date = models.DateField(_('Data de Nascimento'), blank=True, null=True)

    # PJ-specific
    company_name = models.CharField(_('Razão Social / Nome da Empresa'), max_length=150, blank=True, null=True)
    fantasy_name = models.CharField(_('Nome de Fantasia'), max_length=150, blank=True, null=True) # Opcional
    cnpj = models.CharField(_('CNPJ'), max_length=18, blank=True, null=True, unique=True)
    opening_date = models.DateField(_('Data de Abertura'), blank=True, null=True)
    inscricao_estadual = models.CharField(_('Inscrição Estadual'), max_length=20, blank=True, null=True) # Opcional
    contact_person = models.CharField(_('Contato (nome)'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']

    def __str__(self):
        if self.client_type == self.TYPE_PF:
            return f"{self.name} (PF)"
        return f"{self.company_name or self.name} (PJ)"

    def clean(self):
        # validações condicionais
        errors = {}
        if self.client_type == self.TYPE_PF:
            if not self.cpf:
                errors['cpf'] = ValidationError(_('CPF é obrigatório para Pessoa Física.'))
            # here you could add regex/formal CPF validation
            elif not _is_valid_cpf_format(self.cpf):
                errors['cpf'] = ValidationError(_('Formato de CPF inválido. Use apenas números ou 000.000.000-00.'))
        else:  # PJ
            if not self.cnpj:
                errors['cnpj'] = ValidationError(_('CNPJ é obrigatório para Pessoa Jurídica.'))
            elif not _is_valid_cnpj_format(self.cnpj):
                errors['cnpj'] = ValidationError(_('Formato de CNPJ inválido. Use apenas números ou 00.000.000/0000-00.'))
            if not self.company_name:
                errors['company_name'] = ValidationError(_('Razão social é obrigatória para Pessoa Jurídica.'))

        if errors:
            raise ValidationError(errors)

# helpers simples para validar formato - não substituem validação oficial de dígitos verificadores
def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', value or '')

def _is_valid_cpf_format(cpf: str) -> bool:
    digits = _only_digits(cpf)
    return len(digits) == 11

def _is_valid_cnpj_format(cnpj: str) -> bool:
    digits = _only_digits(cnpj)
    return len(digits) == 14
