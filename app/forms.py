from django import forms
from django.contrib.auth.models import User
from .models import PessoaFisica, PessoaJuridica, Produto

# --- 1. CONFIGURAÇÃO DE ESTILO (DARK MODE) ---
# Dicionário com as classes CSS para todos os campos
# bg-dark: Fundo escuro | text-light: Texto claro | border-secondary: Borda cinza
style_attrs = {
    'class': 'form-control bg-dark text-light border-secondary',
}

# --- 2. FORMULÁRIO BASE (Endereço e Contato) ---
# Usado como base para PF e PJ para não repetir código
class ClientBaseForm(forms.ModelForm):
    class Meta:
        # Define campos comuns a ambos
        fields = [
            'email', 'phone', 'phone2',
            'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado', 'pais',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={**style_attrs, 'placeholder': 'ex: nome@email.com'}),
            'phone': forms.TextInput(attrs={**style_attrs, 'placeholder': '(00) 00000-0000'}),
            'phone2': forms.TextInput(attrs={**style_attrs, 'placeholder': 'Opcional'}),
            'cep': forms.TextInput(attrs={**style_attrs, 'placeholder': '00000-000'}),
            'logradouro': forms.TextInput(attrs=style_attrs),
            'numero': forms.TextInput(attrs=style_attrs),
            'bairro': forms.TextInput(attrs=style_attrs),
            'cidade': forms.TextInput(attrs=style_attrs),
            'estado': forms.TextInput(attrs={**style_attrs, 'placeholder': 'UF'}),
            'pais': forms.TextInput(attrs=style_attrs),
        }

# --- 3. FORMULÁRIOS DE CADASTRO (SIGN UP) ---

class ClientePFRegisterForm(ClientBaseForm):
    # Campos extras para criar o Usuário (Login)
    username = forms.CharField(label="Usuário", widget=forms.TextInput(attrs=style_attrs))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs=style_attrs))
    password_confirm = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput(attrs=style_attrs))

    class Meta(ClientBaseForm.Meta):
        model = PessoaFisica
        # Junta os campos específicos de PF com os de Base
        fields = ['username', 'password', 'password_confirm', 'name', 'cpf', 'rg', 'birth_date'] + ClientBaseForm.Meta.fields
        widgets = {
            **ClientBaseForm.Meta.widgets, # Herda widgets de endereço
            'name': forms.TextInput(attrs={**style_attrs, 'placeholder': 'Nome Completo'}),
            'cpf': forms.TextInput(attrs={**style_attrs, 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs=style_attrs),
            'birth_date': forms.DateInput(attrs={**style_attrs, 'type': 'date'}),
        }

    # Validação: Usuário único
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    # Validação: Senhas iguais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não conferem.")
        return cleaned_data

    # Save: Cria User e PessoaFisica juntos
    def save(self, commit=True):
        pessoa = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data['password']
        )
        pessoa.user = user
        if commit:
            pessoa.save()
        return pessoa


class ClientePJRegisterForm(ClientBaseForm):
    # Campos extras para criar o Usuário (Login)
    username = forms.CharField(label="Usuário", widget=forms.TextInput(attrs=style_attrs))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs=style_attrs))
    password_confirm = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput(attrs=style_attrs))

    class Meta(ClientBaseForm.Meta):
        model = PessoaJuridica
        fields = ['username', 'password', 'password_confirm', 'company_name', 'fantasy_name', 'cnpj', 'inscricao_estadual'] + ClientBaseForm.Meta.fields
        widgets = {
            **ClientBaseForm.Meta.widgets,
            'company_name': forms.TextInput(attrs={**style_attrs, 'placeholder': 'Razão Social'}),
            'fantasy_name': forms.TextInput(attrs={**style_attrs, 'placeholder': 'Nome Fantasia'}),
            'cnpj': forms.TextInput(attrs={**style_attrs, 'placeholder': '00.000.000/0001-00'}),
            'inscricao_estadual': forms.TextInput(attrs=style_attrs),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não conferem.")
        return cleaned_data

    def save(self, commit=True):
        pessoa = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data['password']
        )
        pessoa.user = user
        if commit:
            pessoa.save()
        return pessoa

# --- 4. FORMULÁRIOS ADMINISTRATIVOS (EDIÇÃO) ---
# Usados pelo Admin/Staff para editar dados depois (sem mexer em senha/user aqui)

class PessoaFisicaForm(ClientBaseForm):
    class Meta(ClientBaseForm.Meta):
        model = PessoaFisica
        fields = ['name', 'cpf', 'rg', 'birth_date'] + ClientBaseForm.Meta.fields
        widgets = {
            **ClientBaseForm.Meta.widgets,
            'name': forms.TextInput(attrs=style_attrs),
            'cpf': forms.TextInput(attrs=style_attrs),
            'rg': forms.TextInput(attrs=style_attrs),
            'birth_date': forms.DateInput(attrs={**style_attrs, 'type': 'date'}),
        }

class PessoaJuridicaForm(ClientBaseForm):
    class Meta(ClientBaseForm.Meta):
        model = PessoaJuridica
        fields = ['company_name', 'fantasy_name', 'cnpj', 'inscricao_estadual'] + ClientBaseForm.Meta.fields
        widgets = {
            **ClientBaseForm.Meta.widgets,
            'company_name': forms.TextInput(attrs=style_attrs),
            'fantasy_name': forms.TextInput(attrs=style_attrs),
            'cnpj': forms.TextInput(attrs=style_attrs),
            'inscricao_estadual': forms.TextInput(attrs=style_attrs),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs=style_attrs),
            'descricao': forms.Textarea(attrs={**style_attrs, 'rows': 3}),
            'preco': forms.NumberInput(attrs=style_attrs),
            'estoque': forms.NumberInput(attrs=style_attrs),
            'categoria': forms.Select(attrs=style_attrs),
            'imagem': forms.FileInput(attrs={'class': 'form-control bg-dark text-light'}),
        }