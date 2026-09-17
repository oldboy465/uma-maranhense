/**
 * Navegação e Persistência de Células da Central de Atualização
 * Suporte a atalhos: Tab (anda exercícios) e Enter (desce indicadores).
 */

document.addEventListener('DOMContentLoaded', () => {
    const celulas = Array.from(document.querySelectorAll('.celula-rapida'));

    // Agrupa células por indicador para calcular a navegação bidimensional
    celulas.forEach((celula) => {
        // Gravação automática ao perder o foco (blur)
        celula.addEventListener('change', async () => {
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
                if (response.ok) {
                    celula.classList.add('border-emerald-500');
                    setTimeout(() => celula.classList.remove('border-emerald-500'), 1000);
                } else {
                    celula.classList.add('border-rose-500');
                }
            } catch (err) {
                console.error("Falha ao salvar célula:", err);
                celula.classList.add('border-rose-500');
            }
        });

        // Tratamento de Teclas: Enter desce para o mesmo ano do próximo indicador
        celula.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const anoAtual = celula.getAttribute('data-ano');
                const currentIndex = celulas.indexOf(celula);

                // Procura a próxima célula com o mesmo ano
                for (let i = currentIndex + 1; i < celulas.length; i++) {
                    if (celulas[i].getAttribute('data-ano') === anoAtual) {
                        celulas[i].focus();
                        celulas[i].select();
                        break;
                    }
                }
            }
        });
    });
});