from django import forms
from .models import Client

# Widget para forçar o input de data (calendário)
class DateInput(forms.DateInput):
    input_type = 'date'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        
        #
        # --- A CORREÇÃO ESTÁ AQUI ---
        # Esta lista DEVE incluir TODOS os campos que seu HTML usa.
        #
        fields = [
            # Campo oculto que define o tipo (PF ou PJ)
            'client_type', 
            
            # Campos de Pessoa Física
            'name', 'cpf', 'rg', 'birth_date',
            
            # Campos de Pessoa Jurídica
            'company_name', 'fantasy_name', 'cnpj', 'inscricao_estadual',
            
            # Contato & Endereço (campos comuns)
            'email', 'phone', 'phone2',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'pais',
        ]
        
        # Widgets controlam a aparência dos campos
        widgets = {
            # 1. Oculta o campo 'client_type' (ele é preenchido pela URL)
            'client_type': forms.HiddenInput(),
            
            # 2. Usa o widget de calendário para o campo de data
            'birth_date': DateInput(),
            
            # 3. Define todos os campos como 'required=False' no HTML.
            #    A validação real (quais são obrigatórios) 
            #    já está sendo feita no seu models.py (método clean).
            'name': forms.TextInput(attrs={'required': False}),
            'cpf': forms.TextInput(attrs={'required': False}),
            'rg': forms.TextInput(attrs={'required': False}),
            'birth_date': DateInput(attrs={'required': False}),
            
            'company_name': forms.TextInput(attrs={'required': False}),
            'fantasy_name': forms.TextInput(attrs={'required': False}),
            'cnpj': forms.TextInput(attrs={'required': False}),
            'inscricao_estadual': forms.TextInput(attrs={'required': False}),
            
            'email': forms.EmailInput(attrs={'required': False}),
            'phone': forms.TextInput(attrs={'required': False}),
            'phone2': forms.TextInput(attrs={'required': False}),
            'cep': forms.TextInput(attrs={'required': False}),
            'logradouro': forms.TextInput(attrs={'required': False}),
            'numero': forms.TextInput(attrs={'required': False}),
            'bairro': forms.TextInput(attrs={'required': False}),
            'cidade': forms.TextInput(attrs={'required': False}),
            'estado': forms.TextInput(attrs={'required': False}),
            'pais': forms.TextInput(attrs={'required': False}),
        }