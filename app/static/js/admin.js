/**
 * Módulos de Operação da Câmara — Decisões de Validação e Auditoria
 */

document.addEventListener('DOMContentLoaded', () => {
    const formsDecisao = document.querySelectorAll('.form-decisao');

    formsDecisao.forEach(form => {
        form.addEventListener('submit', (e) => {
            const btn = e.submitter;
            if (!btn) return;

            const decisao = btn.value;
            const parecerInput = form.querySelector('input[name="parecer"]');
            const parecer = parecerInput ? parecerInput.value.trim() : '';

            if (decisao === 'DEVOLVER') {
                if (!parecer) {
                    e.preventDefault();
                    alert('Para devolver uma submissão, você deve preencher o parecer analítico apontando o motivo.');
                    if (parecerInput) parecerInput.focus();
                    return;
                }

                if (!confirm('Confirma a devolução desta submissão para correção da universidade?')) {
                    e.preventDefault();
                }
            } else if (decisao === 'VALIDAR') {
                if (!confirm('Confirma a homologação e validação deste registro? Ele entrará imediatamente nos painéis públicos.')) {
                    e.preventDefault();
                }
            }
        });
    });
});