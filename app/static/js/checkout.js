// MÁSCARAS
document.getElementById("cpf").addEventListener("input", e => {
    e.target.value = e.target.value
        .replace(/\D/g, "")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
});

document.getElementById("telefone").addEventListener("input", e => {
    e.target.value = e.target.value
        .replace(/\D/g, "")
        .replace(/(\d{2})(\d)/, "($1) $2")
        .replace(/(\d{5})(\d{4})$/, "$1-$2");
});

document.getElementById("cep").addEventListener("input", e => {
    e.target.value = e.target.value
        .replace(/\D/g, "")
        .replace(/(\d{5})(\d)/, "$1-$2");
});

// AUTOPREENCHER ENDEREÇO VIA VIACEP
document.getElementById("cep").addEventListener("blur", async e => {
    const cep = e.target.value.replace("-", "");
    if (cep.length !== 8) return;

    const r = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    const dados = await r.json();

    if (!dados.erro) {
        document.getElementById("rua").value = dados.logradouro;
        document.getElementById("bairro").value = dados.bairro;
        document.getElementById("cidade").value = dados.localidade;
        document.getElementById("estado").value = dados.uf;
    }
});

// CARTÃO DE CRÉDITO – Luhn Algorithm
function validateCard(number) {
    number = number.replace(/\D/g, "");
    let sum = 0;
    let alt = false;
    for (let i = number.length - 1; i >= 0; i--) {
        let n = parseInt(number[i]);
        if (alt) {
            n *= 2;
            if (n > 9) n -= 9;
        }
        sum += n;
        alt = !alt;
    }
    return sum % 10 === 0;
}

document.getElementById("cartao").addEventListener("blur", e => {
    if (!validateCard(e.target.value)) {
        alert("Número do cartão inválido!");
        e.target.focus();
    }
});

// Validade MM/AA
document.getElementById("validade").addEventListener("input", e => {
    e.target.value = e.target.value
        .replace(/\D/g, "")
        .replace(/(\d{2})(\d)/, "$1/$2");
});
