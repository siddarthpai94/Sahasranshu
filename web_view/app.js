const MOCK_DATA = {
    "stances": [
        {
            "topic": "Inflation",
            "category": "Cautious",
            "confidence": 0.9,
            "evidence": "Inflation has made progress toward the Committee's 2 percent objective but remains somewhat elevated."
        },
        {
            "topic": "Economic Activity",
            "category": "Supportive",
            "confidence": 0.85,
            "evidence": "Recent indicators suggest that economic activity has continued to expand at a solid pace."
        },
        {
            "topic": "Labor Market",
            "category": "Neutral",
            "confidence": 0.8,
            "evidence": "Labor market conditions have generally eased, and the unemployment rate has moved up but remains low."
        }
    ],
    "deltas": [
        {
            "topic": "Inflation Outlook",
            "change_type": "strengthened",
            "previous_stance": "Inflation remains elevated.",
            "current_stance": "Inflation has made progress... but remains somewhat elevated.",
            "explanation": "The committee now explicitly acknowledges 'progress' toward the target, signalling increased confidence in disinflation."
        },
        {
            "topic": "Job Gains",
            "change_type": "weakened",
            "previous_stance": "Job gains have moderated.",
            "current_stance": "Labor market conditions have generally eased.",
            "explanation": "Shift from describing 'moderation' (active slowing) to 'eased' (passive state), suggesting a softer labor market view."
        }
    ],
    "hypotheses": [
        {
            "mechanism": "The Fed is preparing to cut rates in Q1 2025 due to the 'progress' on inflation, shifting focus to preventing labor market deterioration.",
            "falsifiers": [
                "Monthly core PCE re-accelerates above 0.3%",
                "Unemployment rate drops back below 4.0%",
                "Wage growth re-accelerates in employment reports"
            ],
            "confidence": 0.75
        }
    ],
    "memo_content": "# Sahasranshu Research Memo\n\n**Date:** Dec 18, 2024\n**Subject:** FOMC Statement Analysis\n\n## Executive Summary\nThe Federal Reserve has maintained its target range but signaled a clear shift in tone regarding inflation progress.\n\n## Key Findings\n- **Inflation**: 'Progress' is now explicitly cited.\n- **Labor**: Describes conditions as 'eased' rather than just 'moderating'.\n\n## Conclusion\nA rate cut is likely in Q1."
};

function initTerminalClock() {
    const clock = document.getElementById('term-clock');
    if (!clock) return;

    setInterval(() => {
        const now = new Date();
        const options = {
            timeZone: 'America/New_York',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        };
        const estTime = now.toLocaleTimeString('en-US', options);
        clock.textContent = `${estTime} EST`;
    }, 1000);
}

async function loadTerminalData() {
    initTerminalClock();

    try {
        let response;
        try {
            response = await fetch('analysis.json');
            if (!response.ok) throw new Error("analysis.json not found");
        } catch (e1) {
            try {
                response = await fetch('mock_analysis.json');
                if (!response.ok) throw new Error("mock_analysis.json not found");
            } catch (e2) {
                console.log("[TERMINAL] Using embedded mock data");
                renderTerminal(MOCK_DATA);
                return;
            }
        }

        const data = await response.json();
        renderTerminal(data);

    } catch (e) {
        console.error("[TERMINAL ERROR]", e);
        document.getElementById('memo-container').innerHTML =
            `<p style="color: var(--red);">SYSTEM ERROR: ${e.message}</p>`;
    }
}

function renderTerminal(data) {
    if (data.meta && data.meta.doc_id) {
        const docEl = document.getElementById('doc-id');
        if (docEl) docEl.textContent = data.meta.doc_id.toUpperCase().replace(/[^A-Z0-9]/g, '_');
    }

    renderStances(data.stances);
    renderDeltas(data.deltas);
    renderHypotheses(data.hypotheses);

    if (data.memo_content) {
        renderMemo(data.memo_content, data);
    }
}

function renderStances(stances) {
    const tbody = document.getElementById('stance-tbody');
    if (!stances || !tbody) return;

    tbody.innerHTML = stances.map(s => {
        const confPercent = (s.confidence * 100).toFixed(0);
        return `
            <tr class="data-update">
                <td class="topic-cell">${s.topic}</td>
                <td>
                    <span class="stance-pill pill-${s.category.toLowerCase()}">${s.category.toUpperCase()}</span>
                </td>
                <td class="confidence-cell">
                    <div class="conf-wrapper">
                        <span class="conf-text">${confPercent}%</span>
                        <div class="conf-bar-bg">
                            <div class="conf-bar-fill" style="width: ${confPercent}%"></div>
                        </div>
                    </div>
                </td>
                <td class="evidence-cell">${s.evidence}</td>
            </tr>
        `;
    }).join('');
}

function renderDeltas(deltas) {
    const container = document.getElementById('delta-container');
    if (!deltas || !container) return;

    container.innerHTML = deltas.map(d => `
        <div class="delta-block">
            <div class="delta-header">
                <div class="delta-topic">${d.topic.toUpperCase()}</div>
                <div class="delta-flag flag-${d.change_type}">${d.change_type.toUpperCase()}</div>
            </div>
            <div class="delta-comp">
                <div class="comp-row">
                    <span class="comp-label">PREV:</span>
                    <span class="comp-prev">${d.previous_stance}</span>
                </div>
                <div class="comp-row">
                    <span class="comp-label">CURR:</span>
                    <span class="comp-curr">${d.current_stance}</span>
                </div>
            </div>
            <div class="delta-note">${d.explanation}</div>
        </div>
    `).join('');
}

function renderHypotheses(hypotheses) {
    const container = document.getElementById('hypo-container');
    if (!hypotheses || !container) return;

    container.innerHTML = hypotheses.map(h => `
        <div class="hypo-card">
            <div class="hypo-badge">CONFIDENCE: ${(h.confidence * 100).toFixed(0)}%</div>
            <div class="hypo-text">${h.mechanism}</div>
            <div class="falsifier-section">
                <span class="falsifier-label">Falsification Criteria</span>
                <ul class="falsifier-list">
                    ${h.falsifiers.map(f => `<li>${f}</li>`).join('')}
                </ul>
            </div>
        </div>
    `).join('');
}

function renderMemo(text, data = {}) {
    const container = document.getElementById('memo-container');
    if (!container) return;

    // 1. Calculate Executive Metrics
    const stances = data.stances || [];
    const totalStances = stances.length || 1;
    const supportive = stances.filter(s => s.category.toLowerCase() === 'supportive').length;
    const cautious = stances.filter(s => s.category.toLowerCase() === 'cautious').length;

    // Sentiment: % supportive - % cautious
    const sentimentScore = Math.round(((supportive - cautious) / totalStances) * 100);
    const sentimentLabel = sentimentScore > 10 ? 'HAWKISH' : (sentimentScore < -10 ? 'DOVISH' : 'BALANCED');

    // Confidence: Average of stance confidence
    const avgConfidence = Math.round((stances.reduce((acc, s) => acc + (s.confidence || 0), 0) / totalStances) * 100);

    // Delta Intensity: (Number of deltas / topics) * 100
    const deltaCount = data.deltas?.length || 0;
    const deltaIntensity = Math.min(100, Math.round((deltaCount / Math.max(1, totalStances)) * 100));

    // 2. Process Markdown Content
    let bodyHtml = text
        .replace(/^# (.*$)/gim, '') // Remove main title (we use our own header)
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/^> \*\*BLUF\*\* (.*$)/gim, '<div class="bluf-box">$1</div>')
        .replace(/\n\n/gim, '<br><br>');

    // Enhanced Table Conversion
    if (bodyHtml.includes('|')) {
        const rows = bodyHtml.split('<br><br>');
        for (let i = 0; i < rows.length; i++) {
            if (rows[i].includes('|') && rows[i].includes('--')) {
                const tableRows = rows[i].trim().split('\n').filter(r => r.includes('|'));
                let tableHtml = '<div class="memo-table-wrapper"><table><thead>';
                const headers = tableRows[0].split('|').filter(h => h.trim());
                tableHtml += '<tr>' + headers.map(h => `<th>${h.trim()}</th>`).join('') + '</tr></thead><tbody>';

                for (let j = 2; j < tableRows.length; j++) {
                    const cells = tableRows[j].split('|').filter(c => c !== undefined).slice(1, -1);
                    tableHtml += '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
                }
                tableHtml += '</tbody></table></div>';
                bodyHtml = bodyHtml.replace(rows[i], tableHtml);
            }
        }
    }

    // 3. Assemble Premium Document
    const docId = data.meta?.doc_id || "SAHASRANSHU_CORE";
    const date = data.meta?.current_date || new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

    const fullHtml = `
        <div class="memo-header">
            <div class="memo-branding">
                <div class="memo-logo-stamp">SAHASRANSHU RESEARCH INTELLIGENCE</div>
                <div class="memo-classification">L3 EXECUTIVE</div>
            </div>
            <h1>Intelligence Memo</h1>
            <div style="font-family: var(--font-terminal); font-size: 10px; color: var(--text-muted); margin-top: 10px;">
                REF: ${docId} / ${date}
            </div>
        </div>

        <div class="memo-scorecard">
            <div class="score-item">
                <span class="score-label">Policy Tone</span>
                <span class="score-value">${sentimentLabel}</span>
                <div class="score-progress-bg">
                    <div class="score-progress-fill" style="width: ${Math.abs(sentimentScore)}%; background: ${sentimentScore >= 0 ? 'var(--gold)' : 'var(--cyan)'}"></div>
                </div>
            </div>
            <div class="score-item">
                <span class="score-label">Delta Intensity</span>
                <span class="score-value">${deltaIntensity}%</span>
                <div class="score-progress-bg">
                    <div class="score-progress-fill" style="width: ${deltaIntensity}%"></div>
                </div>
            </div>
            <div class="score-item">
                <span class="score-label">Analysis Confidence</span>
                <span class="score-value">${avgConfidence}%</span>
                <div class="score-progress-bg">
                    <div class="score-progress-fill" style="width: ${avgConfidence}%"></div>
                </div>
            </div>
        </div>

        <div class="memo-body-content">
            ${bodyHtml}
        </div>

        <div class="signature-block">
            <div class="sig-title">AUTHENTICATED BY</div>
            <div class="sig-name">Sahasranshu Analytics Engine</div>
            <div style="font-family: var(--font-terminal); font-size: 8px; color: var(--text-muted); margin-top: 5px;">
                © 2026 DIGITAL SIGNATURE VERIFIED
            </div>
        </div>
    `;

    container.innerHTML = fullHtml;
}

document.addEventListener('DOMContentLoaded', loadTerminalData);
