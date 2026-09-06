/**
 * Interatividade do Comparador Institucional
 * Impede seleção duplicada da mesma universidade e valida submissão.
 */

document.addEventListener('DOMContentLoaded', () => {
    const selUni1 = document.getElementById('uni1');
    const selUni2 = document.getElementById('uni2');
    const formComparador = document.querySelector('.form-comparador');

    if (!selUni1 || !selUni2) return;

    function ajustarOpcoes() {
        const val1 = selUni1.value;
        const val2 = selUni2.value;

        Array.from(selUni2.options).forEach(opt => {
            opt.disabled = (opt.value && opt.value === val1);
        });

        Array.from(selUni1.options).forEach(opt => {
            opt.disabled = (opt.value && opt.value === val2);
        });
    }

    selUni1.addEventListener('change', ajustarOpcoes);
    selUni2.addEventListener('change', ajustarOpcoes);
    ajustarOpcoes();

    if (formComparador) {
        formComparador.addEventListener('submit', (e) => {
            if (selUni1.value === selUni2.value && selUni1.value !== '') {
                e.preventDefault();
                alert('Selecione duas universidades diferentes para realizar a comparação.');
            }
        });
    }
});