# Annotation code

The scripts that produced the corpus in `../data/`, published for
methodological transparency. **None of this is needed to reproduce the
paper's tables and figures** — that's `../analysis.ipynb`, which runs
entirely on the already-annotated data. Run these only to inspect the
exact annotation procedure or to re-annotate the corpus yourself.

| Script | What it does |
|---|---|
| `llm_annotate_questions.py` | LLM batch annotation of questions (schema A v0.7), via the Claude Batches API |
| `llm_annotate_answers.py` | LLM batch annotation of answers (schema B v0.3), via the Claude Batches API |
| `annotate_ui.py` | Streamlit app used for the manual reference-sample coding |
| `paths.py` | Shared path config — reads `../data/`, writes to `*_reannotated` files so the published data is never overwritten |

Both LLM scripts embed their full system prompt (the same taxonomy
documented in `../docs/annotation-guidelines.md`) and call
`claude-opus-4-6` via the Batches API.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then add your own ANTHROPIC_API_KEY
```

No key is included in this repository. Running `llm_annotate_questions.py`
or `llm_annotate_answers.py` will make billed API calls.

## Usage

```bash
# LLM annotation (questions)
python llm_annotate_questions.py submit --limit 20   # test on 20 rows
python llm_annotate_questions.py status               # poll batch status
python llm_annotate_questions.py retrieve              # download + save
python llm_annotate_questions.py run                   # submit + poll + save in one go

# LLM annotation (answers) — same interface
python llm_annotate_answers.py run

# Manual annotation UI
streamlit run annotate_ui.py
```

Output is written to `../data/questions_llm_reannotated.csv` /
`../data/answers_llm_reannotated.csv` (LLM scripts) and
`../data/questions_manual_reannotated.csv` /
`../data/answers_manual_reannotated.csv` (manual UI export). Batch IDs and
manual-annotation progress are kept in `state/` (created on first run, not
committed).
