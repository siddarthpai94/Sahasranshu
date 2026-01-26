# Prompt Contracts

## Stance Extraction

**Input**: Document text
**Output**: JSON list of stances with:
- `topic`: Policy area
- `category`: Supportive/Cautious/Opposed/Neutral
- `confidence`: 0.0-1.0
- `evidence`: Supporting quote or paraphrase

## Delta Detection

**Input**: Previous and current document text
**Output**: JSON list of changes with:
- `topic`: Policy area
- `change_type`: Strengthened/Weakened/Reversed/New/Removed
- `previous_stance`: Previous category
- `current_stance`: Current category
- `explanation`: Why the change occurred

## Hypothesis Generation

**Input**: List of deltas
**Output**: JSON list of hypotheses with:
- `mechanism`: Proposed causal mechanism
- `falsifiers`: Ways the hypothesis could be wrong
- `confidence`: 0.0-1.0
