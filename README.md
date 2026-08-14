# Asking the Auditor

Code and data accompanying *Asking the Auditor: How Members of Parliament Use
Questions about Audits to Control the Executive*.

The paper studies 1,778 formal written questions and 1,703 answers exchanged
between the Dutch House of Representatives and the Netherlands Court of Audit
(*Algemene Rekenkamer*) between 2011 and 2025, in response to the Court's
published performance audits. Each question and answer is classified along a
four/five-point taxonomy of cognitive demand — factual retrieval, causal
explanation, evaluative judgment, and prescriptive recommendation (plus
deflection for answers) — using a large language model (Claude Opus 4.6),
validated against a manually coded reference sample.

## Contents

```
analysis.ipynb   single notebook reproducing every table and figure in the paper
metrics.py       Cohen's kappa, weighted kappa, and confusion-matrix helpers
data/            annotated corpus (see below)
docs/            annotation codebook (schema definitions and decision rules)
figures/         output directory for generated figures (populated on run)
```

## Data (`data/`)

| File | Rows | Description |
|---|---|---|
| `questions_llm_annotated.csv` | 1,778 | All questions, LLM-annotated (schema A: FEIT/CAU/OOR/ADV) |
| `answers_llm_annotated.csv` | 1,703 | All answers, LLM-annotated (schema B: FEIT/CAU/OOR/ADV/DEFL) |
| `questions_manual_annotated.csv` | 1,778 | Same corpus; `label` populated for the manually coded reference sample (n=250) |
| `answers_manual_annotated.csv` | 1,703 | Same corpus; `label` populated for the manually coded reference sample (n=251) |
| `deflection_taxonomy.csv` | 459 | Every deflected (DEFL) answer, manually sub-coded into five deflection types |
| `committees.csv` | 187 | Maps each source document to its submitting parliamentary committee (used to infer policy domain) |

Each row is one parliamentary question–answer pair, joined by `src_id` +
`vraag_nr`. Source files use the original Dutch schema labels
(`FEIT`/`CAU`/`OOR`/`ADV`/`DEFL`); the notebook maps these to the English
labels used in the paper (`FACT`/`CAU`/`EVAL`/`PRES`/`DEFL`).

Text columns (`vraag`, `antwoord`) are in Dutch, the original language of the
source documents.

## Codebook (`docs/annotation-guidelines.md`)

The full annotation schema (Dutch, v0.7 for questions / v0.3 for answers)
used both as the LLM system prompt and by the human annotators who produced
the reference sample, including label definitions, decision rules, and
worked examples.

## Reproducing the paper

```bash
pip install -r requirements.txt
jupyter execute analysis.ipynb --output=analysis.ipynb   # or open and run interactively
```

`analysis.ipynb` reproduces, in order:

- **Table 1 / Figure 3** — validation of LLM coding against the manual reference sample (Cohen's κ, weighted κ, F1, confusion matrices)
- **Table 2 / Table 3** — question and answer label distributions
- **Figure 1** — question × answer cross-tabulation
- **Figure 2** — breakdown of deflection types by question label
- **Table 4** — question label distribution by policy domain
- Chi-square / Cramér's V association tests reported in the discussion

No API key is required to reproduce the paper's tables and figures — all
annotation has already been produced and is included in `data/`.
