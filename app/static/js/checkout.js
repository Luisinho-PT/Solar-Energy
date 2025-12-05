// app/static/js/checkout.js

// ==========================================================
// MÁSCARAS
// ==========================================================

// Máscara para CPF
document.getElementById("cpf").addEventListener("input", e => {
    e.target.value = e.target.value
        .replace(/\D/g, "")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
});

// Máscara para CNPJ
document.getElementById("cnpj").addEventListener("input", e => {
    e.target.value = e.target.value
        .replace(/\D/g, "")
        .replace(/^(\d{2})(\d)/, "$1.$2")
        .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3/")
        .replace(/\.(\d{3})(\d)/, "$1/$2")
        .replace(/(\d{4})(\d)/, "$1-$2");
});

// Máscara para Telefone (Se o campo estiver no checkout)
const inputTelefone = document.getElementById("telefone");
if (inputTelefone) {
    inputTelefone.addEventListener("input", e => {
        e.target.value = e.target.value
            .replace(/\D/g, "")
            .replace(/(\d{2})(\d)/, "($1) $2")
            .replace(/(\d{5})(\d{4})$/, "$1-$2");
    });
}

// Máscara para CEP (Se o campo estiver no checkout)
const inputCep = document.getElementById("cep");
if (inputCep) {
    inputCep.addEventListener("input", e => {
        e.target.value = e.target.value
            .replace(/\D/g, "")
            .replace(/(\d{5})(\d)/, "$1-$2");
    });
}


// ==========================================================
// AUTOPREENCHER ENDEREÇO VIA VIACEP (Se for o caso)
// ==========================================================

if (inputCep) {
    inputCep.addEventListener("blur", async e => {
        const cep = e.target.value.replace("-", "");
        if (cep.length !== 8) return;

        try {
            const r = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const dados = await r.json();

            if (!dados.erro) {
                // Supondo que você tem esses IDs no seu HTML
                const logradouro = document.getElementById("logradouro") || document.getElementById("rua");
                if (logradouro) logradouro.value = dados.logradouro;
                
                const bairro = document.getElementById("bairro");
                if (bairro) bairro.value = dados.bairro;
                
                const cidade = document.getElementById("cidade");
                if (cidade) cidade.value = dados.localidade;
                
                const estado = document.getElementById("estado");
                if (estado) estado.value = dados.uf;
            }
        } catch (error) {
            console.error("Erro ao buscar CEP:", error);
        }
    });
}


// ==========================================================
// LÓGICA DE VISIBILIDADE E OBRIGATORIEDADE (PF/PJ)
// ESTA É A CORREÇÃO CRÍTICA
// ==========================================================

const tipoClienteSelect = document.getElementById("tipo_cliente");
const pfBox = document.getElementById("pf-box");
const pjBox = document.getElementById("pj-box");
const inputCpf = document.getElementById("cpf");
const inputCnpj = document.getElementById("cnpj");

function toggleClientFields() {
    const tipo = tipoClienteSelect.value;

    // 1. Ocultar, remover required e limpar tudo por padrão
    if (pfBox) pfBox.classList.add("hidden");
    if (pjBox) pjBox.classList.add("hidden");
    
    if (inputCpf) {
        inputCpf.removeAttribute("required");
    }
    if (inputCnpj) {
        inputCnpj.removeAttribute("required");
    }

    // 2. Aplicar regras com base na seleção
    if (tipo === "PF") {
        if (pfBox) pfBox.classList.remove("hidden");
        if (inputCpf) {
            inputCpf.setAttribute("required", "required");
            inputCpf.focus();
        }
        if (inputCnpj) inputCnpj.value = ""; // Limpa o valor do CNPJ
        
    } else if (tipo === "PJ") {
        if (pjBox) pjBox.classList.remove("hidden");
        if (inputCnpj) {
            inputCnpj.setAttribute("required", "required");
            inputCnpj.focus();
        }
        if (inputCpf) inputCpf.value = ""; // Limpa o valor do CPF
    }
}

// Aplica a lógica quando o valor do select muda
tipoClienteSelect.addEventListener("change", toggleClientFields);

// Executa uma vez ao carregar a página
window.addEventListener("load", toggleClientFields);