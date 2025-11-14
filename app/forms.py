# app/forms.py
from django import forms
from .models import PessoaFisica, PessoaJuridica, Produto

# --- 1. WIDGETS E ATRIBUTOS COMUNS ---
class DateInput(forms.DateInput):
    input_type = 'date'

# Atributos de CSS para facilitar a estilização (ex: com Bootstrap)
common_attrs = {'class': 'form-control'}

# --- 2. FORMULÁRIO BASE COM CAMPOS COMUNS ---
class ClientBaseForm(forms.ModelForm):
    """
    Formulário base que contém os campos comuns a Pessoa Física e Jurídica.
    """
    class Meta:
        fields = [
            'email', 'phone', 'phone2',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'pais',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={**common_attrs, 'placeholder': 'seuemail@dominio.com'}),
            'phone': forms.TextInput(attrs={**common_attrs, 'placeholder': '(XX) XXXXX-XXXX'}),
            'phone2': forms.TextInput(attrs={**common_attrs, 'placeholder': '(XX) XXXXX-XXXX'}),
            'cep': forms.TextInput(attrs={**common_attrs, 'placeholder': 'XXXXX-XXX'}),
            'logradouro': forms.TextInput(attrs=common_attrs),
            'numero': forms.TextInput(attrs=common_attrs),
            'bairro': forms.TextInput(attrs=common_attrs),
            'cidade': forms.TextInput(attrs=common_attrs),
            'estado': forms.TextInput(attrs={**common_attrs, 'placeholder': 'UF'}),
            'pais': forms.TextInput(attrs=common_attrs),
        }

# --- 3. FORMULÁRIO ESPECÍFICO PARA PESSOA FÍSICA ---
class PessoaFisicaForm(ClientBaseForm):
    """
    Herda os campos de ClientBaseForm e adiciona os campos específicos de PessoaFisica.
    """
    class Meta(ClientBaseForm.Meta):
        model = PessoaFisica
        fields = [
            'name', 'cpf', 'rg', 'birth_date',
        ] + ClientBaseForm.Meta.fields

        widgets = {
            **ClientBaseForm.Meta.widgets, # Herda widgets do base
            'name': forms.TextInput(attrs={**common_attrs, 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={**common_attrs, 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs=common_attrs),
            'birth_date': DateInput(attrs=common_attrs),
        }

# --- 4. FORMULÁRIO ESPECÍFICO PARA PESSOA JURÍDICA ---
class PessoaJuridicaForm(ClientBaseForm):
    """
    Herda os campos de ClientBaseForm e adiciona os campos específicos de PessoaJuridica.
    """
    class Meta(ClientBaseForm.Meta):
        model = PessoaJuridica
        fields = [
            'company_name', 'fantasy_name', 'cnpj', 'inscricao_estadual',
        ] + ClientBaseForm.Meta.fields

        widgets = {
            **ClientBaseForm.Meta.widgets, # Herda widgets do base
            'company_name': forms.TextInput(attrs={**common_attrs, 'placeholder': 'Razão Social da Empresa'}),
            'fantasy_name': forms.TextInput(attrs={**common_attrs, 'placeholder': 'Nome Fantasia (opcional)'}),
            'cnpj': forms.TextInput(attrs={**common_attrs, 'placeholder': '00.000.000/0001-00'}),
            'inscricao_estadual': forms.TextInput(attrs=common_attrs),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "descricao", "preco", "estoque", "categoria", "imagem"]

        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }