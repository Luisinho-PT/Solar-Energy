/* loja.js – interações da loja solar */

/* ============================================
   ANIMAÇÃO DE ADICIONAR AO CARRINHO (Frontend)
   ============================================ */
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("btn-buy")) {
        e.target.classList.add("clicked");
        setTimeout(() => {
            e.target.classList.remove("clicked");
        }, 700);
    }
});

/* ============================================
   TROCA DE IMAGEM DO PRODUTO (Detalhes)
   ============================================ */
const mainImg = document.getElementById("mainImg");
if (mainImg) {
    document.querySelectorAll(".detail-thumb").forEach(thumb => {
        thumb.addEventListener("click", () => {
            const img = thumb.querySelector("img");
            mainImg.style.opacity = 0;

            setTimeout(() => {
                mainImg.src = img.src;
                mainImg.style.opacity = 1;
            }, 150);
        });
    });
}

/* ============================================
   SCROLL ANIMATION – Navbar flutuante solar
   ============================================ */
let lastScroll = 0;
const navbar = document.querySelector(".navbar");

if (navbar) {
    window.addEventListener("scroll", () => {
        const current = window.scrollY;

        if (current > lastScroll && current > 30) {
            navbar.classList.add("navbar-hide");
        } else {
            navbar.classList.remove("navbar-hide");
        }
        lastScroll = current;
    });
}

/* ============================================
   CARRINHO LOCAL (caso backend ainda não pronto)
   ============================================ */
function adicionarLocalCarrinho(produtoId, quantidade = 1) {
    const carrinho = JSON.parse(localStorage.getItem("solarCart") || "{}");

    if (!carrinho[produtoId]) {
        carrinho[produtoId] = 0;
    }
    carrinho[produtoId] += parseInt(quantidade);

    localStorage.setItem("solarCart", JSON.stringify(carrinho));
    console.log("Carrinho atualizado:", carrinho);

    mostrarToast("Produto adicionado ao carrinho!");
}

/* intercepta forms quando backend ainda não existe */
document.querySelectorAll("form[action*='adicionar_carrinho']").forEach(form => {
    form.addEventListener("submit", function(e) {
        if (!window.backendCarrinhoAtivo) {
            e.preventDefault();
            const id = this.querySelector("input[name='produto_id']").value;
            const qtd = this.querySelector("input[name='quantidade']")?.value || 1;
            adicionarLocalCarrinho(id, qtd);
        }
    });
});

/* ============================================
   Toast elegante solar
   ============================================ */
function mostrarToast(msg) {
    let toast = document.createElement("div");
    toast.className = "solar-toast";
    toast.innerText = msg;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 100);
    setTimeout(() => toast.classList.remove("show"), 2000);
    setTimeout(() => toast.remove(), 2600);
}
