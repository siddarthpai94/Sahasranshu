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
        const h = String(now.getUTCHours()).padStart(2, '0');
        const m = String(now.getUTCMinutes()).padStart(2, '0');
        const s = String(now.getUTCSeconds()).padStart(2, '0');
        clock.textContent = `${h}:${m}:${s} GMT`;
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
        renderMemo(data.memo_content);
    }
}

function renderStances(stances) {
    const tbody = document.getElementById('stance-tbody');
    if (!stances || !tbody) return;

    tbody.innerHTML = stances.map(s => `
        <tr class="data-update">
            <td class="topic-cell">${s.topic.toUpperCase()}</td>
            <td>
                <span class="stance-pill pill-${s.category.toLowerCase()}">${s.category.toUpperCase()}</span>
            </td>
            <td class="confidence-cell">${(s.confidence * 100).toFixed(0)}%</td>
            <td class="evidence-cell">${s.evidence}</td>
        </tr>
    `).join('');
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

function renderMemo(text) {
    const container = document.getElementById('memo-container');
    if (!container) return;

    let html = text
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/^- (.*$)/gim, '<p style="padding-left: 16px; border-left: 2px solid var(--orange); margin: 6px 0;">$1</p>')
        .replace(/\n\n/gim, '<br><br>');

    container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', loadTerminalData);
