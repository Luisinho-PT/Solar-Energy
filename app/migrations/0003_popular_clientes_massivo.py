from django.db import migrations
import random


# ----------------------------
# GERADORES DE CPF E CNPJ
# ----------------------------

def gerar_cpf(mask=True):
    def dv(num):
        soma = sum([int(num[i]) * (len(num)+1-i) for i in range(len(num))])
        dig = (soma * 10) % 11
        return dig if dig < 10 else 0

    n = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    d1 = dv(n)
    d2 = dv(n + str(d1))
    cpf = n + str(d1) + str(d2)

    if not mask:
        return cpf

    return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"


def gerar_cnpj(mask=True):
    def dv(num):
        pesos = [6,5,4,3,2,9,8,7,6,5,4,3,2]
        soma = sum(int(num[i]) * pesos[i+len(pesos)-len(num)] for i in range(len(num)))
        dig = soma % 11
        return 0 if dig < 2 else 11 - dig

    n = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    d1 = dv(n)
    d2 = dv(n + str(d1))
    cnpj = n + str(d1) + str(d2)

    if not mask:
        return cnpj

    return f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"


# ----------------------------
# POPULAÇÃO DE CLIENTES
# ----------------------------

def gerar_pf():
    nomes = [
        "Ana Paula Gomes", "João Ricardo Mendes", "Mariana Alves Costa", "Carlos Eduardo Silva",
        "Fernanda Monteiro", "Lucas Andrade", "Gabriel Sousa", "Bruna Carvalho", "Rafael Martins",
        "Patrícia Correia", "Hugo Farias", "Larissa Gonçalves", "Felipe Moura", "Tatiane Rocha",
        "Diogo Almeida", "Natália Duarte", "Vinícius Azevedo", "Juliana Pires", "Rodrigo Mattos",
        "Amanda Ferreira"
    ]

    cidades = [
        ("São Paulo", "SP"), ("Campinas", "SP"), ("Belo Horizonte", "MG"),
        ("Rio de Janeiro", "RJ"), ("Curitiba", "PR"), ("Porto Alegre", "RS"),
        ("Salvador", "BA"), ("Fortaleza", "CE"), ("Recife", "PE"), ("Goiânia", "GO")
    ]

    pf_list = []
    for nome in nomes:
        cidade, uf = random.choice(cidades)
        pf_list.append({
            "name": nome,
            "cpf": gerar_cpf(mask=True),
            "email": f"{nome.split()[0].lower()}@exemplo.com",
            "phone": f"11 9{random.randint(6000,9999)}-{random.randint(1000,9999)}",
            "logradouro": "Rua Solar",
            "numero": str(random.randint(10, 500)),
            "bairro": "Centro",
            "cidade": cidade,
            "estado": uf,
            "cep": f"{random.randint(10000,99999)}-{random.randint(100,999)}",
            "pais": "Brasil",
        })
    return pf_list


def gerar_pj():
    empresas = [
        "SolarPrime Brasil", "Energiza Solar Systems", "SunPower Solutions",
        "HelioTech Equipamentos", "EcoSun Instalações", "PhotonMax Brasil",
        "Solaris Energy Group", "GreenVolt Energia", "BlueSky Solar",
        "MaxSolar Distribuidora", "SolarCenter Importadora", "Energia Forte LTDA",
        "SolEnergia Engenharia", "SunHouse Brasil", "Helios Comercial",
        "PowerSun Distribuição", "SolarMais BR", "InfinitySolar",
        "Solarequip LTDA", "SolarBright Comercial"
    ]

    cidades = [
        ("São Paulo", "SP"), ("Campinas", "SP"), ("Ribeirão Preto", "SP"),
        ("Florianópolis", "SC"), ("Joinville", "SC"), ("Curitiba", "PR"),
        ("Brasília", "DF"), ("Uberlândia", "MG"), ("Contagem", "MG"), ("Cuiabá", "MT")
    ]

    pj_list = []
    for empresa in empresas:
        cidade, uf = random.choice(cidades)
        pj_list.append({
            "company_name": empresa,
            "fantasy_name": empresa.split()[0],
            "cnpj": gerar_cnpj(mask=True),
            "email": f"contato@{empresa.replace(' ', '').lower()}.com",
            "phone": f"11 3{random.randint(2000,5999)}-{random.randint(1000,9999)}",
            "logradouro": "Avenida Energia Solar",
            "numero": str(random.randint(50, 800)),
            "bairro": "Industrial",
            "cidade": cidade,
            "estado": uf,
            "cep": f"{random.randint(10000,99999)}-{random.randint(100,999)}",
            "pais": "Brasil",
        })
    return pj_list


def popular(apps, schema_editor):
    PessoaFisica = apps.get_model("app", "PessoaFisica")
    PessoaJuridica = apps.get_model("app", "PessoaJuridica")

    for data in gerar_pf():
        PessoaFisica.objects.get_or_create(cpf=data["cpf"], defaults=data)

    for data in gerar_pj():
        PessoaJuridica.objects.get_or_create(cnpj=data["cnpj"], defaults=data)


def remover(apps, schema_editor):
    PessoaFisica = apps.get_model("app", "PessoaFisica")
    PessoaJuridica = apps.get_model("app", "PessoaJuridica")
    PessoaFisica.objects.all().delete()
    PessoaJuridica.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_popular"),
    ]

    operations = [
        migrations.RunPython(popular, remover),
    ]
