document.addEventListener("DOMContentLoaded", function () {

    // CPF
    const cpf = document.querySelector("input[name='cpf']");
    if (cpf) {
        IMask(cpf, { mask: "000.000.000-00" });
    }

    // CNPJ
    const cnpj = document.querySelector("input[name='cnpj']");
    if (cnpj) {
        IMask(cnpj, { mask: "00.000.000/0000-00" });
    }

    // Telefone principal
    const phone = document.querySelector("input[name='phone']");
    if (phone) {
        IMask(phone, { mask: "(00) 00000-0000" });
    }

    // Telefone secundário
    const phone2 = document.querySelector("input[name='phone2']");
    if (phone2) {
        IMask(phone2, { mask: "(00) 00000-0000" });
    }

    // CEP
    const cep = document.querySelector("input[name='cep']");
    if (cep) {
        IMask(cep, { mask: "00000-000" });

        // Função para bloquear/desbloquear campos
        function toggleFields(block) {
            const formFields = document.querySelectorAll("form input, form select, form textarea");
            formFields.forEach(function(field) {
                if (field !== cep) { // não bloqueia o próprio CEP
                    if (block) {
                        if (field.value) { // bloqueia apenas campos já preenchidos
                            field.readOnly = true;
                            field.disabled = field.tagName === "SELECT" ? true : false;
                        }
                    } else {
                        field.readOnly = false;
                        field.disabled = false;
                    }
                }
            });
        }

        // Busca automática no ViaCEP
        cep.addEventListener("input", function () {
            const cepValue = cep.value.replace(/\D/g, "");

            if (cepValue.length === 8) {
                fetch(`https://viacep.com.br/ws/${cepValue}/json/`)
                    .then(res => res.json())
                    .then(data => {
                        if (!data.erro) {

                            const logradouro = document.querySelector("input[name='logradouro']");
                            const bairro = document.querySelector("input[name='bairro']");
                            const cidade = document.querySelector("input[name='cidade']");
                            const estado = document.querySelector("input[name='estado']");

                            if (logradouro) logradouro.value = data.logradouro;
                            if (bairro) bairro.value = data.bairro;
                            if (cidade) cidade.value = data.localidade;
                            if (estado) estado.value = data.uf;

                            // Bloqueia os campos preenchidos após preencher o CEP
                            toggleFields(true);
                        }
                    });
            } else {
                // Desbloqueia campos se CEP incompleto
                toggleFields(false);
            }
        });
    }

    // Estado UF (somente letras, 2 caracteres)
    const estado = document.querySelector("input[name='estado']");
    if (estado) {
        IMask(estado, {
            mask: /^[A-Za-z]{0,2}$/,
            prepare: function (str) {
                return str.toUpperCase();
            }
        });
    }

    // Data de nascimento (DD/MM/AAAA)
    const birthDate = document.querySelector("input[name='birth_date']");
    if (birthDate) {
        IMask(birthDate, {
            mask: Date,
            pattern: "d/`m/`Y",
            blocks: {
                d: { mask: IMask.MaskedRange, from: 1, to: 31, maxLength: 2 },
                m: { mask: IMask.MaskedRange, from: 1, to: 12, maxLength: 2 },
                Y: { mask: IMask.MaskedRange, from: 1900, to: 2099 }
            }
        });
    }

});
