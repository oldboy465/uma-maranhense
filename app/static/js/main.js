/**
 * Scripts Gerais e Máscaras de Formatação — Plataforma Maria Firmina
 */

document.addEventListener('DOMContentLoaded', () => {
    // Máscara dinâmica para valores no padrão brasileiro (1.234.567,89)
    const inputsMonetarios = document.querySelectorAll('.input-valor');

    inputsMonetarios.forEach(input => {
        input.addEventListener('input', (e) => {
            let valor = e.target.value.replace(/\D/g, '');
            if (!valor) {
                e.target.value = '';
                return;
            }

            // Garante ao menos centavos
            valor = (parseInt(valor, 10) / 100).toFixed(2);

            // Substitui separadores para padrao BR
            let partes = valor.split('.');
            partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            e.target.value = partes.join(',');
        });
    });

    // Auto-fechamento de alertas flash após 6 segundos
    const alertas = document.querySelectorAll('.alert');
    alertas.forEach(alerta => {
        setTimeout(() => {
            if (alerta && alerta.parentElement) {
                alerta.style.opacity = '0';
                alerta.style.transition = 'opacity 0.5s ease';
                setTimeout(() => alerta.remove(), 500);
            }
        }, 6000);
    });
});