// Atualiza nome
document.getElementById("nomeInput").addEventListener("input", () => {
    const value = nomeInput.value.trim();
    previewNome.textContent = value || "Nome do Produto";
});

// Atualiza descrição
document.getElementById("descricaoInput").addEventListener("input", () => {
    const value = descricaoInput.value.trim();
    previewDesc.textContent = value || "A descrição do produto aparecerá aqui...";
});

// Atualiza categoria
document.getElementById("categoriaInput").addEventListener("change", () => {
    const selected = categoriaInput.options[categoriaInput.selectedIndex];
    previewCategoria.textContent = selected.text || "Categoria";
});

// Atualiza preço com formatação
document.getElementById("precoInput").addEventListener("input", () => {
    let num = Number(precoInput.value);
    previewPreco.textContent = "R$ " + (num ? num.toFixed(2).replace(".", ",") : "0,00");
});

// Atualiza imagem
document.getElementById("imagemInput").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => previewImg.src = reader.result;
    reader.readAsDataURL(file);
});
