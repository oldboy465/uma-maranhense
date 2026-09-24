/**
 * Navegação, Higienização Estrita e Persistência de Células
 * Regras estritas:
 * 1. Proibido letras, espaços, pontos e caracteres especiais.
 * 2. Máximo permitido: números e no máximo UMA vírgula.
 * 3. Atalhos de navegação: Enter desce indicador, Tab anda ano.
 */

document.addEventListener('DOMContentLoaded', () => {
    const celulas = Array.from(document.querySelectorAll('.celula-rapida'));

    celulas.forEach((celula) => {
        // Bloqueia teclas proibidas diretamente no evento keydown
        celula.addEventListener('keydown', (e) => {
            // Teclas de controle permitidas
            const teclasPermitidas = [
                'Backspace', 'Delete', 'Tab', 'Escape', 'Enter', 
                'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'
            ];

            if (teclasPermitidas.includes(e.key) || e.ctrlKey || e.metaKey) {
                // Navegação com Enter
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const anoAtual = celula.getAttribute('data-ano');
                    const currentIndex = celulas.indexOf(celula);

                    for (let i = currentIndex + 1; i < celulas.length; i++) {
                        if (celulas[i].getAttribute('data-ano') === anoAtual && !celulas[i].disabled) {
                            celulas[i].focus();
                            celulas[i].select();
                            break;
                        }
                    }
                }
                return;
            }

            // Permite somente números de 0 a 9 e no máximo uma vírgula
            const ehNumero = (e.key >= '0' && e.key <= '9');
            const ehVirgula = (e.key === ',');

            if (!ehNumero && !ehVirgula) {
                e.preventDefault();
                return;
            }

            // Impede mais de uma vírgula
            if (ehVirgula && celula.value.includes(',')) {
                e.preventDefault();
            }
        });

        // Limpeza reativa contra colagens ou inserções espúrias (remove letras, espaços, pontos)
        celula.addEventListener('input', (e) => {
            let val = e.target.value;

            // Remove pontos, letras, espaços e símbolos
            val = val.replace(/[^0-9,]/g, '');

            // Garante apenas a primeira vírgula caso o usuário cole texto com múltiplas
            const partes = val.split(',');
            if (partes.length > 2) {
                val = partes[0] + ',' + partes.slice(1).join('');
            }

            if (e.target.value !== val) {
                e.target.value = val;
            }
        });

        // Gravação assíncrona ao sair do campo (blur / change)
        celula.addEventListener('change', async () => {
            if (celula.disabled || celula.readOnly) return;

            const uniId = celula.getAttribute('data-uni');
            const indId = celula.getAttribute('data-ind');
            const ano = celula.getAttribute('data-ano');
            const valor = celula.value.trim();

            const formData = new FormData();
            formData.append('universidade_id', uniId);
            formData.append('indicador_id', indId);
            formData.append('ano_referencia', ano);
            formData.append('valor', valor);

            try {
                const response = await fetch('/minha-universidade/salvar-celula', {
                    method: 'POST',
                    body: formData
                });
                
                const json = await response.json();

                if (response.ok && json.sucesso) {
                    celula.classList.remove('border-rose-500');
                    celula.classList.add('border-emerald-500');
                    setTimeout(() => celula.classList.remove('border-emerald-500'), 1000);
                } else {
                    celula.classList.add('border-rose-500');
                    alert(json.erro || 'Erro ao salvar valor.');
                }
            } catch (err) {
                console.error("Falha ao salvar célula:", err);
                celula.classList.add('border-rose-500');
            }
        });
    });
});