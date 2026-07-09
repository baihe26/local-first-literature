# Local-First Literature

Local-First Literature is a literature radar that starts from your own paper library before searching the web.

Most literature tools begin with keywords and return a long list of papers. This project reverses the order:

1. Index your existing PDFs, DOCX files, notes, RIS/BibTeX records, and local literature folders.
2. Infer what your research direction is from the papers you already keep.
3. Build a gap map for the project: background, mechanism, methods, controls, benchmarks, and writing or figure needs.
4. Search new literature only after the local context is understood.
5. Deduplicate against your local library.
6. Score each candidate across multiple axes.
7. Export an evidence matrix and reading-priority report.

The result is not just "papers matching a keyword"; it is a ranked list of what is already covered, what is near-duplicate, what is genuinely new, and what is worth adding because it fills a specific research gap.

## Why It Is Different

- **Local-first, not keyword-first**  
  It reads your existing literature folders before searching, so recommendations are anchored in what you already have.

- **Research-gap aware**  
  It can use a project design, proposal, manuscript draft, or inferred profile to identify missing background, mechanism, methods, controls, and benchmark papers.

- **Deduplication built in**  
  New candidates are labeled as `already`, `near_duplicate`, `genuinely_new`, `worth_adding`, or `low_priority_duplicate`.

- **Multi-axis scoring**  
  Every candidate gets separate scores for topic relevance, mechanism value, experiment reusability, gap filling, novelty against the local library, journal/year signal, and evidence richness.

- **Evidence boundaries are visible**  
  The workflow distinguishes metadata-only hits, abstract-level evidence, local full text, methods-like text, figure captions, and extraction failures.

- **Actionable outputs**  
  It writes CSV/HTML by default and produces Excel/Word reports when `openpyxl` and `python-docx` are installed.

## Repository Layout

```text
local-first-literature/
  SKILL.md
  README.md
  LICENSE
  requirements.txt
  scripts/
    local_first_literature.py
    smoke_test.py
  references/
    research-profile-template.yaml
    scoring-rubric.md
    privacy-and-open-source.md
  examples/
    profiles/
      biomaterials-hydrogel-example.yaml
      environmental-photocatalysis-example.yaml
  outputs/        # ignored, generated reports
  state/          # ignored, persistent local state
```

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-user>/local-first-literature.git
cd local-first-literature
```

Optional dependencies for richer file and report support:

```bash
python -m pip install -r requirements.txt
```

The core workflow uses the Python standard library. Optional packages enable PDF extraction and Word/Excel output.

## Quick Start

Index a local paper library:

```bash
python -X utf8 scripts/local_first_literature.py index \
  --roots "D:\path\to\papers" \
  --output outputs/local_library.jsonl
```

Infer a profile from the local library:

```bash
python -X utf8 scripts/local_first_literature.py infer-profile \
  --index outputs/local_library.jsonl \
  --output outputs/profile.json
```

Build a gap map from the inferred profile and, optionally, a project design:

```bash
python -X utf8 scripts/local_first_literature.py gap-map \
  --profile outputs/profile.json \
  --design "D:\path\to\project_design.docx" \
  --output outputs/gap_map.json
```

Search recent literature through OpenAlex:

```bash
python -X utf8 scripts/local_first_literature.py search \
  --profile outputs/profile.json \
  --gap-map outputs/gap_map.json \
  --years 3 \
  --output outputs/candidates.jsonl
```

Deduplicate and score:

```bash
python -X utf8 scripts/local_first_literature.py score \
  --index outputs/local_library.jsonl \
  --candidates outputs/candidates.jsonl \
  --profile outputs/profile.json \
  --gap-map outputs/gap_map.json \
  --output outputs/scored.jsonl
```

Render reports:

```bash
python -X utf8 scripts/local_first_literature.py render \
  --scored outputs/scored.jsonl \
  --output-dir outputs/report
```

Or run the full pipeline:

```bash
python -X utf8 scripts/local_first_literature.py run \
  --roots "D:\path\to\papers" \
  --design "D:\path\to\project_design.docx" \
  --years 3 \
  --output-dir outputs/local_first_run
```

## Output Files

Typical outputs include:

- `local_library_index.jsonl`: local paper metadata and extraction status.
- `inferred_profile.json`: inferred research profile.
- `gap_map.json`: literature needs split by background, mechanism, methods, controls, benchmarks, and writing/figure needs.
- `candidates.jsonl`: newly searched candidates.
- `scored.jsonl`: deduplicated and scored candidates.
- `report/literature_evidence_matrix.csv`
- `report/reading_priority_report.html`
- `report/literature_evidence_matrix.xlsx` if `openpyxl` is installed.
- `report/reading_priority_report.docx` if `python-docx` is installed.

## Scoring Model

Each candidate is scored on:

- `topic_relevance`
- `mechanism_value`
- `experiment_reusability`
- `gap_fill`
- `novelty_against_local`
- `journal_year_signal`
- `evidence_richness`

The scoring goal is calibrated prioritization, not a fake precision metric. A highly relevant duplicate should not outrank a new paper that fills an important missing method or mechanism gap.

See [references/scoring-rubric.md](references/scoring-rubric.md).

## Privacy

The public repository is designed to avoid leaking personal research data.

Do not commit:

- local library indexes
- extracted paper text
- private project profiles
- manuscript drafts
- real output reports
- personal folder paths

Use ignored folders such as `state/`, `outputs/`, or `private/` for real projects.

See [references/privacy-and-open-source.md](references/privacy-and-open-source.md).

## Smoke Test

Run:

```bash
python -X utf8 scripts/smoke_test.py
```

The smoke test creates a temporary mini-library, indexes it, infers a profile, builds a gap map, scores two candidates, and renders CSV/HTML plus optional Word/Excel outputs.

## Skill Usage

This repository is also a Codex skill. To install it as a skill, clone it into your Codex skills folder:

```bash
git clone https://github.com/<your-user>/local-first-literature.git ~/.codex/skills/local-first-literature
```

Then ask Codex to use `$local-first-literature`.

## License

MIT License.
