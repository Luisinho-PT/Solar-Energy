from django.db import migrations
from django.core.files import File
from django.conf import settings
import os

def criar_produtos(apps, schema_editor):
    Categoria = apps.get_model("app", "Categoria")
    Produto = apps.get_model("app", "Produto")

    base = os.path.join(settings.BASE_DIR, "static", "images", "produtos")

    produtos = [
        # categoria_nome, nome, descricao, preco, imagem_filename
        ("Inversores", "Inversor Fronius 5.0", "Inversor solar premium, eficiência 97.8%, ideal para residências.", 5200, "inversor-fronius-5kw-ai.jpg"),
        ("Inversores", "Growatt 3000W", "Modelo econômico e eficiente para uso residencial.", 2990, "inversor-growatt-3kw-ai.jpg"),
        ("Inversores", "Deye 8kW Híbrido", "Compatível com baterias, ideal para sistemas híbridos.", 8990, "inversor-deye-8kw-ai.jpg"),

        ("Cabos", "Cabo Solar 6mm Vermelho", "Cabo para sistemas fotovoltaicos certificado.", 5.90, "cabo-6mm-vermelho-ai.jpg"),
        ("Cabos", "Cabo Solar 6mm Preto", "Alta isolação e durabilidade UV.", 5.80, "cabo-6mm-preto-ai.jpg"),
        ("Cabos", "Cabo Solar 10mm Vermelho", "Indicado para longas distâncias e maior corrente.", 9.50, "cabo-10mm-vermelho-ai.jpg"),

        ("Estruturas Inox", "Suporte Inox p/ Telha", "Alta durabilidade e resistência à corrosão.", 39.90, "suporte-inox-telha-ai.jpg"),
        ("Estruturas Inox", "Gancho Inox Universal", "Compatível com todos os tipos de trilho.", 29.90, "gancho-inox-ai.jpg"),
        ("Estruturas Inox", "Trilho Inox 1.5m", "Estrutura resistente para fixação de módulos.", 79.90, "trilho-inox-1-5m-ai.jpg"),

        ("Parafusos", "Parafuso Sextavado M10", "Parafuso para fixações estruturais de alto torque.", 1.20, "parafuso-m10-ai.jpg"),
        ("Parafusos", "Parafuso Auto Brocante 8mm", "Ideal para telhas metálicas.", 0.90, "parafuso-auto-8mm-ai.jpg"),
        ("Parafusos", "Parafuso c/ Arruela EPDM", "Vedação superior contra infiltração.", 1.50, "parafuso-epdm-ai.jpg"),

        ("Baterias", "Bateria Lithium 48V 100Ah", "Alta durabilidade, mais de 6000 ciclos.", 12990, "bateria-lithium-48v-100ah-ai.jpg"),
        ("Baterias", "Bateria VRLA 12V 150Ah", "Para backup em sistemas off-grid simples.", 1290, "bateria-vrla-12v-150ah-ai.jpg"),
        ("Baterias", "Bateria Gel 12V 200Ah", "Ideal para aplicações industriais.", 1890, "bateria-gel-12v-200ah-ai.jpg"),

        ("Estruturas Galvanizadas", "Trilho Galvanizado 2m", "Estrutura para painéis solares.", 69.90, "trilho-galv-2m-ai.jpg"),
        ("Estruturas Galvanizadas", "Suporte Galv. p/ Módulo", "Suporte reforçado de alto desempenho.", 49.90, "suporte-galv-modulo-ai.jpg"),
        ("Estruturas Galvanizadas", "Fixador Galv. Ajustável", "Compatível com diversos tipos de telha.", 19.90, "fixador-galv-ajustavel-ai.jpg"),

        ("Módulos", "Módulo Jinko 550W", "Painel solar monocristalino de alta eficiência.", 1190, "modulo-jinko-550w-ai.jpg"),
        ("Módulos", "Módulo Canadian Solar 450W", "Excelente desempenho em baixa irradiação.", 980, "modulo-canadian-450w-ai.jpg"),
        ("Módulos", "Módulo Trina 500W", "Construção robusta e alta durabilidade.", 1090, "modulo-trina-500w-ai.jpg"),

        ("Componentes Elétricos", "Disjuntor CC 600V 32A", "Proteção essencial em sistemas fotovoltaicos.", 39.90, "disjuntor-cc-600v-32a-ai.jpg"),
        ("Componentes Elétricos", "DPS 1000V Tipo 2", "Proteção contra surtos elétricos.", 79.90, "dps-1000v-ai.jpg"),
        ("Componentes Elétricos", "Chave Seccionadora 1000V 32A", "Segurança e isolamento no sistema solar.", 149.90, "chave-seccionadora-1000v-ai.jpg"),
    ]

    for categoria_nome, nome, desc, preco, imagem in produtos:
        cat, _ = Categoria.objects.get_or_create(nome=categoria_nome)
        p, created = Produto.objects.get_or_create(
            nome=nome,
            defaults={
                'descricao': desc,
                'preco': preco,
                'categoria': cat,
                'estoque': 10,
            }
        )
        # se arquivo existe localmente, anexa a imagem
        img_path = os.path.join(base, imagem)
        if os.path.exists(img_path):
            # reabre e salva no campo imagem
            with open(img_path, "rb") as f:
                p.imagem.save(imagem, File(f), save=True)

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),  # ajuste conforme necessário
    ]

    operations = [
        migrations.RunPython(criar_produtos),
    ]
