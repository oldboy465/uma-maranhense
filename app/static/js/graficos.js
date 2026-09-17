/**
 * Renderizador de Visualizações SVG Nativas — Padrão Visual ABRUEM
 * Gera barras horizontais, barras duplas emparelhadas e séries de linhas
 * com cálculos automáticos de coordenadas sem dependências externas.
 */

const GraficosABRUEM = {
    /**
     * Renderiza barra horizontal proporcional com rótulos
     */
    criarBarraHorizontal(containerId, valor, maximo, rotulo, cor = '#0284c7') {
        const container = document.getElementById(containerId);
        if (!container || !maximo) return;

        const porcentagem = Math.min(100, Math.max(0, (valor / maximo) * 100));

        container.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px; font-family: var(--font-sans); width: 100%;">
                <div style="flex: 1; background: #f1f5f9; border-radius: 6px; height: 16px; overflow: hidden;">
                    <div style="width: ${porcentagem}%; background: ${cor}; height: 100%; transition: width 0.6s ease;"></div>
                </div>
                <span style="font-size: 0.8rem; font-weight: bold; color: #0f172a; min-width: 90px; text-align: right;">
                    ${rotulo}
                </span>
            </div>
        `;
    },

    /**
     * Renderiza gráfico de barras duplas emparelhadas (ex: Docentes x Técnicos)
     */
    criarBarrasDuplas(containerId, v1, v2, maximo, rotulo1, rotulo2, cor1 = '#1e3a8a', cor2 = '#0284c7') {
        const container = document.getElementById(containerId);
        if (!container || !maximo) return;

        const p1 = Math.min(100, Math.max(0, (v1 / maximo) * 100));
        const p2 = Math.min(100, Math.max(0, (v2 / maximo) * 100));

        container.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 4px; width: 100%; font-family: var(--font-sans);">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="flex: 1; background: #f1f5f9; border-radius: 4px; height: 10px; overflow: hidden;">
                        <div style="width: ${p1}%; background: ${cor1}; height: 100%; transition: width 0.5s ease;"></div>
                    </div>
                    <span style="font-size: 0.75rem; font-weight: 600; color: #334155; min-width: 70px; text-align: right;">${rotulo1}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="flex: 1; background: #f1f5f9; border-radius: 4px; height: 10px; overflow: hidden;">
                        <div style="width: ${p2}%; background: ${cor2}; height: 100%; transition: width 0.5s ease;"></div>
                    </div>
                    <span style="font-size: 0.75rem; font-weight: 600; color: #334155; min-width: 70px; text-align: right;">${rotulo2}</span>
                </div>
            </div>
        `;
    },

    /**
     * Gera gráfico de linha SVG completo com escala proporcional e marcadores circulares
     */
    gerarLinhaSVG(pontos, largura = 800, altura = 240, corLinha = '#0f172a') {
        if (!pontos || pontos.length === 0) return '';

        const valores = pontos.map(p => p.valor);
        const minVal = Math.min(...valores);
        const maxVal = Math.max(...valores);
        const margemX = 80;
        const margemY = 40;
        const deltaX = (largura - 2 * margemX) / (pontos.length - 1 || 1);
        const deltaVal = (maxVal - minVal) || 1;

        const coords = pontos.map((p, idx) => {
            const x = margemX + idx * deltaX;
            const y = (altura - margemY) - ((p.valor - minVal) / deltaVal) * (altura - 2 * margemY);
            return { x, y, ano: p.ano, valor: p.valor };
        });

        const pointsAttr = coords.map(c => `${c.x},${c.y}`).join(' ');

        let circulosSvg = '';
        coords.forEach(c => {
            circulosSvg += `
                <circle cx="${c.x}" cy="${c.y}" r="4" fill="${corLinha}" />
                <text x="${c.x}" y="${c.y - 12}" text-anchor="middle" font-size="11" font-weight="bold" fill="${corLinha}">${c.valor.toLocaleString('pt-BR')}</text>
                <text x="${c.x}" y="${altura - 15}" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b">${c.ano}</text>
            `;
        });

        return `
            <svg viewBox="0 0 ${largura} ${altura}" class="w-full h-auto font-sans">
                <line x1="${margemX - 20}" y1="${altura - margemY}" x2="${largura - margemX + 20}" y2="${altura - margemY}" stroke="#cbd5e1" stroke-width="1.5" />
                <polyline fill="none" stroke="${corLinha}" stroke-width="2.5" points="${pointsAttr}" />
                ${circulosSvg}
            </svg>
        `;
    }
};

window.GraficosABRUEM = GraficosABRUEM;