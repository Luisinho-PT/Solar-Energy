document.addEventListener("DOMContentLoaded", () => {
    
    // O CÓDIGO DO TOGGLE QUE CAUSOU O ERRO FOI REMOVIDO DESTA ÁREA
    
    // --- MANTENHA TODO O CÓDIGO DAS MÁSCARAS ---
    
    // Máscara CPF
    const cpf = document.getElementById("id_cpf");
    if (cpf) cpf.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        e.target.value = value.slice(0, 14);
    });

    // Máscara CNPJ
    const cnpj = document.getElementById("id_cnpj");
    if (cnpj) cnpj.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        value = value.replace(/^(\d{2})(\d)/, "$1.$2");
        value = value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        value = value.replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3/$4");
        value = value.replace(/(\d{4})(\d)/, "$1-$2");
        e.target.value = value.slice(0, 18);
    });

    // Máscara CEP
    const cep = document.getElementById("id_cep");
    if (cep) cep.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "");
        value = value.replace(/^(\d{5})(\d)/, "$1-$2");
        e.target.value = value.slice(0, 9);
    });

    // Máscara telefone (IDs corrigidos para id_phone e id_phone2)
    const tels = ["id_phone", "id_phone2"]; 
    
    tels.forEach(id => {
        let tel = document.getElementById(id);
        if (tel) tel.addEventListener("input", (e) => {
            let value = e.target.value.replace(/\D/g, "");
            value = value.replace(/^(\d{2})(\d)/, "($1) $2");
            value = value.replace(/(\d{5})(\d)/, "$1-$2"); 
            e.target.value = value.slice(0, 15); 
        });
    });
});