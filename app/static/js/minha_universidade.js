/**
 * Central de Atualização — Validações Preventivas e Confirmação de Submissão
 */

document.addEventListener('DOMContentLoaded', () => {
    const formsInline = document.querySelectorAll('.form-inline-valor');

    formsInline.forEach(form => {
        form.addEventListener('submit', (e) => {
            const btnClicado = e.submitter;
            const acao = btnClicado ? btnClicado.value : 'salvar_rascunho';
            const inputValor = form.querySelector('.input-valor');
            const valor = inputValor ? inputValor.value.trim() : '';

            // Regra metodológica: zero exige confirmação explícita
            if (valor === '0,00' || valor === '0') {
                const confirmaZero = confirm(
                    'Atenção Metodológica: Você informou o valor ZERO. ' +
                    'Confirma que o dado foi expressamente verificado na fonte e é efetivamente nulo?'
                );
                if (!confirmaZero) {
                    e.preventDefault();
                    return;
                }
            }

            // Confirmação para envio formal à Câmara
            if (acao === 'enviar') {
                const confirmaEnvio = confirm(
                    'Ao enviar, o dado entrará na fila de validação da Câmara da ABRUEM e ' +
                    'não poderá ser alterado até a homologação ou devolução com parecer. Deseja prosseguir?'
                );
                if (!confirmaEnvio) {
                    e.preventDefault();
                }
            }
        });
    });
});