"""
paths.py — data paths shared by the annotation scripts in this folder.

All scripts read the already-published corpus in ../data/ (see the top-level
README) and, by default, write their output alongside it under a distinct
`_reannotated` name so that running them locally never overwrites the
citable reference data.
"""

from pathlib import Path

_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE.parent
DATA_DIR = REPO_ROOT / "data"

# Source corpus — both scripts only need rapport_titel / vergaderjaar / vraag /
# antwoord, all present in the published, already-annotated files. Any
# existing llm_label / llm_confidence / llm_reasoning columns are ignored on
# read and overwritten fresh in the output.
QUESTIONS_SOURCE = DATA_DIR / "questions_llm_annotated.csv"
ANSWERS_SOURCE = DATA_DIR / "answers_llm_annotated.csv"

# Default output paths for a fresh annotation run (see note above).
QUESTIONS_OUTPUT = DATA_DIR / "questions_llm_reannotated.csv"
ANSWERS_OUTPUT = DATA_DIR / "answers_llm_reannotated.csv"

# Manual annotation UI: same source corpus; output for a fresh manual pass.
QUESTIONS_MANUAL_OUTPUT = DATA_DIR / "questions_manual_reannotated.csv"
ANSWERS_MANUAL_OUTPUT = DATA_DIR / "answers_manual_reannotated.csv"

# Optional raw source-document text, keyed by src_id, used only for an
# in-app document preview. Not part of the published data — the preview is
# skipped automatically if this file is absent.
RAW_CSV = DATA_DIR / "kamervragen-raw.csv"

# Per-run state (batch IDs, manual-annotation progress) — local scratch,
# not published.
STATE_DIR = _HERE / "state"
STATE_DIR.mkdir(exist_ok=True)
