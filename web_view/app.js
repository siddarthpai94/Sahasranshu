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
                "Unemployment rate drops back below 4.0%"
            ],
            "confidence": 0.75
        }
    ]
};

async function loadAnalysis() {
    try {
        let response;
        try {
            // Priority 1: Local copy (if script copied it)
            response = await fetch('analysis.json');
            if (!response.ok) throw new Error("Local analysis not found");
        } catch (e1) {
            try {
                // Priority 2: Direct link to processed folder (Demo specific path)
                console.log("Checking relative processed path...");
                response = await fetch('../data/US/FED/2024/Dec/processed/US_FED_2024-12-18_FOMC_Statement.analysis.json');
                if (!response.ok) throw new Error("Processed analysis not found");
            } catch (e2) {
                // Priority 3: Mock data via FETCH (might fail on file://)
                try {
                    console.log("Falling back to mock file...");
                    response = await fetch('mock_analysis.json');
                    if (!response.ok) throw new Error("Mock file failed");
                } catch (e3) {
                    // FINAL FALLBACK: Embedded data (Always works)
                    console.log("All fetches failed (likely CORS). Using embedded mock data.");

                    // Mock Meta for Demo
                    const mockMeta = {
                        "current_date": "2024-12-18",
                        "previous_date": "2024-11-07"
                    };

                    renderStances(MOCK_DATA.stances);
                    renderDeltas(MOCK_DATA.deltas, mockMeta);
                    renderHypotheses(MOCK_DATA.hypotheses);
                    return;
                }
            }
        }

        const data = await response.json();
        renderStances(data.stances);
        renderDeltas(data.deltas);
        renderHypotheses(data.hypotheses);

    } catch (e) {
        console.error("Error parsing analysis data", e);
    }
}

function renderStances(stances) {
    const container = document.getElementById('stance-container');
    if (!stances) return;

    container.innerHTML = stances.map(s => `
        <div class="stance-item">
            <span class="topic">${s.topic}</span>
            <div class="category" style="color: ${getColorForCategory(s.category)}">${s.category}</div>
            <span class="evidence">"${s.evidence}"</span>
        </div>
    `).join('');
}

function getColorForCategory(cat) {
    cat = cat.toLowerCase();
    if (cat.includes('support') || cat.includes('eas')) return 'var(--accent-green)';
    if (cat.includes('cautious') || cat.includes('tight')) return 'var(--accent-red)';
    return 'var(--text-primary)';
}

function renderDeltas(deltas, meta) {
    const container = document.getElementById('delta-container');
    const header = document.getElementById('delta-header-text');

    if (!deltas) return;

    // Update Header with Dates if available
    let prevLabel = "WAS";
    let currLabel = "NOW";

    if (meta) {
        if (meta.previous_date) {
            const d = new Date(meta.previous_date);
            const month = d.toLocaleString('default', { month: 'short' }).toUpperCase(); // NOV
            prevLabel = `${month} READ`;
            header.innerHTML = `Delta Analysis <span class="highlight">vs ${month} ${d.getDate()}</span>`;
        }
        if (meta.current_date) {
            const d = new Date(meta.current_date);
            const month = d.toLocaleString('default', { month: 'short' }).toUpperCase(); // DEC
            currLabel = `${month} READ`;
        }
    }

    container.innerHTML = deltas.map(d => `
        <div class="delta-item">
            <div class="delta-header">
                <h3>${d.topic}</h3>
                <span class="change-type ${d.change_type}">${d.change_type}</span>
            </div>
            <div class="diff-box">
                <div class="diff-line">
                    <span class="diff-label">${prevLabel}:</span>
                    <span class="diff-val previous">${d.previous_stance}</span>
                </div>
                <div class="diff-line">
                    <span class="diff-label">${currLabel}:</span>
                    <span class="diff-val current">${d.current_stance}</span>
                </div>
            </div>
            <div class="explanation">
                ${d.explanation}
            </div>
        </div>
    `).join('');
}

function renderHypotheses(hyps) {
    const container = document.getElementById('hypothesis-container');
    if (!hyps) return;

    container.innerHTML = hyps.map(h => `
        <div class="hypothesis-item">
            <strong class="mech">${h.mechanism}</strong>
            <div class="falsifiers">
                <strong>FALSIFIERS:</strong>
                <ul>
                    ${h.falsifiers.map(f => `<li>${f}</li>`).join('')}
                </ul>
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', loadAnalysis);
