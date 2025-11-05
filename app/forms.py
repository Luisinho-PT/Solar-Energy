from django import forms
from .models import Client

# Widget para forçar o input de data
class DateInput(forms.DateInput):
    input_type = 'date'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        
        # Lista explícita dos campos que seu HTML usa
        fields = [
            # PF
            'name', 'cpf', 'rg', 'birth_date',
            
            # PJ
            'company_name', 'fantasy_name', 'cnpj', 'inscricao_estadual',
            
            # Contato & Endereço
            'email', 'phone', 'phone2',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'pais',
        ]
        
        # Adiciona o widget de calendário ao campo de data
        widgets = {
            'birth_date': DateInput(),
            
            # Definindo 'required=False' aqui para todos os campos
            # A validação real de "obrigatório" será feita pelo 
            # método clean() do seu models.py, com base no tipo de cliente.
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