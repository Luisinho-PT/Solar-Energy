from django.db import models
from django_cpf_cnpj.fields import CPFField, CNPJField
from django.utils.translation import gettext_lazy as _

# 1. O MODELO BASE (Não cria uma tabela)
class ClientBase(models.Model):
    # Campos comuns
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    phone = models.CharField(_('Telefone Principal'), max_length=15, blank=True, null=True)
    phone2 = models.CharField(_('Telefone Secundário'), max_length=15, blank=True, null=True)
    cep = models.CharField(_('CEP'), max_length=9, blank=True, null=True)
    logradouro = models.CharField(_('Logradouro'), max_length=150, blank=True, null=True)
    numero = models.CharField(_('Número'), max_length=10, blank=True, null=True)
    bairro = models.CharField(_('Bairro'), max_length=80, blank=True, null=True)
    cidade = models.CharField(_('Cidade'), max_length=100, blank=True, null=True)
    estado = models.CharField(_('Estado'), max_length=2, blank=True, null=True)
    pais = models.CharField(_('País'), max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True # Isso é o que faz ser um modelo abstrato!

# 2. TABELA SEPARADA PARA PESSOA FÍSICA
class PessoaFisica(ClientBase):
    name = models.CharField(_('Nome'), max_length=150)
    cpf = CPFField(masked=True, unique=True) # Agora é obrigatório
    rg = models.CharField(_('RG'), max_length=20, blank=True, null=True)
    birth_date = models.DateField(_('Data de Nascimento'), blank=True, null=True)

    class Meta:
        verbose_name = 'Cliente (PF)'
        verbose_name_plural = 'Clientes (PF)'
    
    def __str__(self):
        return self.name

# 3. TABELA SEPARADA PARA PESSOA JURÍDICA
class PessoaJuridica(ClientBase):
    company_name = models.CharField(_('Razão Social'), max_length=150)
    fantasy_name = models.CharField(_('Nome de Fantasia'), max_length=150, blank=True, null=True)
    cnpj = CNPJField(masked=True, unique=True) # Agora é obrigatório
    inscricao_estadual = models.CharField(_('Inscrição Estadual'), max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Cliente (PJ)'
        verbose_name_plural = 'Clientes (PJ)'

    def __str__(self):
        return self.company_name
    
class Categoria(models.Model):
    categorias = [
        ("inversores", "Inversores"),
        ("cabos", "Cabos"),
        ("estruturas", "Estruturas Inox"),
        ("parafusos", "Parafusos"),
        ("baterias", "Baterias"),
    ]

    slug = models.CharField(max_length=50, choices=categorias, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to="static/img/produtos")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="produtos")
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

    def em_estoque(self):
        return self.estoque > 0
