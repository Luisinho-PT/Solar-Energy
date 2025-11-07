# app/forms.py
from django import forms
from .models import PessoaFisica, PessoaJuridica

# Widget para o calendário
class DateInput(forms.DateInput):
    input_type = 'date'

# --- 1. FORMULÁRIO PARA PESSOA FÍSICA ---
class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        # Lista de campos do PessoaFisica + ClientBase
        fields = [
            'name', 'cpf', 'rg', 'birth_date',
            'email', 'phone', 'phone2',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'pais',
        ]
        widgets = {
            'birth_date': DateInput(),
        }

# --- 2. FORMULÁRIO PARA PESSOA JURÍDICA ---
class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        # Lista de campos do PessoaJuridica + ClientBase
        fields = [
            'company_name', 'fantasy_name', 'cnpj', 'inscricao_estadual',
            'email', 'phone', 'phone2',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'pais',
        ]
        # Não precisamos de widgets especiais aqui (por enquanto)