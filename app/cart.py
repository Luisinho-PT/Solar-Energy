from decimal import Decimal
from app.models import Produto

class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, produto_id, quantidade=1):
        produto = Produto.objects.get(id=produto_id)
        pid = str(produto.id)

        if pid not in self.cart:
            self.cart[pid] = {
                "nome": produto.nome,
                "preco": str(produto.preco),
                "quantidade": quantidade,
                "imagem": produto.imagem.url if produto.imagem else "",
            }
        else:
            self.cart[pid]["quantidade"] += quantidade

        self.save()

    def remove(self, produto_id):
        pid = str(produto_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def update(self, produto_id, quantidade):
        pid = str(produto_id)
        if pid in self.cart:
            self.cart[pid]["quantidade"] = quantidade
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def __iter__(self):
        for pid, item in self.cart.items():
            item["total"] = Decimal(item["preco"]) * item["quantidade"]
            yield {
                "id": pid,
                **item
            }

    def get_total(self):
        return sum(Decimal(item["preco"]) * item["quantidade"] for item in self.cart.values())

    def count_items(self):
        return sum(item["quantidade"] for item in self.cart.values())

    def save(self):
        self.session.modified = True
