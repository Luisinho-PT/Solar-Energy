document.addEventListener("DOMContentLoaded", () => {
    const btnPF = document.getElementById("btnFisica");
    const btnPJ = document.getElementById("btnJuridica");
    const formPF = document.getElementById("formPF");
    const formPJ = document.getElementById("formPJ");

    // Alternar PF e PJ
    btnPF.addEventListener("click", () => {
        btnPF.classList.add("active");
        btnPJ.classList.remove("active");
        formPF.classList.remove("hidden");
        formPJ.classList.add("hidden");
    });

    btnPJ.addEventListener("click", () => {
        btnPJ.classList.add("active");
        btnPF.classList.remove("active");
        formPJ.classList.remove("hidden");
        formPF.classList.add("hidden");
    });

    // Máscara CPF
    const cpf = document.getElementById("id_cpf");
    if (cpf) cpf.addEventListener("input", () => {
        cpf.value = cpf.value.replace(/\D/g, "")
            .replace(/(\d{3})(\d)/, "$1.$2")
            .replace(/(\d{3})(\d)/, "$1.$2")
            .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    });

    // Máscara CNPJ
    const cnpj = document.getElementById("id_cnpj");
    if (cnpj) cnpj.addEventListener("input", () => {
        cnpj.value = cnpj.value.replace(/\D/g, "")
            .replace(/^(\d{2})(\d)/, "$1.$2")
            .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
            .replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3/$4")
            .replace(/(\d{4})(\d)/, "$1-$2");
    });

    // Máscara CEP
    const cep = document.getElementById("id_cep");
    if (cep) cep.addEventListener("input", () => {
        cep.value = cep.value.replace(/\D/g, "")
            .replace(/^(\d{5})(\d)/, "$1-$2");
    });

    /* --- BLOCO ATUALIZADO --- */
    // Máscara telefone (IDs corrigidos)
    const tels = ["id_phone", "id_phone2"]; // <--- CORRIGIDO
    
    tels.forEach(id => {
        let tel = document.getElementById(id);
        if (tel) tel.addEventListener("input", () => {
            let value = tel.value.replace(/\D/g, "");
            value = value.replace(/^(\d{2})(\d)/, "($1) $2");
            value = value.replace(/(\d{5})(\d)/, "$1-$2"); 
            tel.value = value.slice(0, 15); 
        });
    });
});