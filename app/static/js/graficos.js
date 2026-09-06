/**
 * Renderizador de Visualizações SVG Nativas — Padrão Visual ABRUEM
 * Gera barras e marcadores de quartis/medianas sem bibliotecas externas pesadas.
 */

const GraficosABRUEM = {
    /**
     * Gera uma barra horizontal proporcional de benchmark
     * @param {string} containerId ID do elemento alvo
     * @param {number} valor Valor apurado
     * @param {number} maximo Valor máximo da escala
     * @param {string} rotulo Rótulo formatado (ex: R$ 1.500,00)
     */
    criarBarraHorizontal(containerId, valor, maximo, rotulo) {
        const container = document.getElementById(containerId);
        if (!container || !maximo) return;

        const porcentagem = Math.min(100, Math.max(0, (valor / maximo) * 100));

        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px; font-family: var(--font-sans);">
                <div style="flex: 1; background: #e2e8f0; border-radius: 6px; height: 16px; overflow: hidden;">
                    <div style="width: ${porcentagem}%; background: var(--primary); height: 100%; transition: width 0.6s ease;"></div>
                </div>
                <span style="font-size: 0.85rem; font-weight: bold; color: var(--secondary); min-width: 90px; text-align: right;">
                    ${rotulo}
                </span>
            </div>
        `;
    }
};

window.GraficosABRUEM = GraficosABRUEM;