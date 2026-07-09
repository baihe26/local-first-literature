# Literature Gap Radar

**中文简介**  
Literature Gap Radar 是一个“本地来源优先”的文献雷达。它不是先让用户反复调关键词，而是先读取用户已经拥有的文献、文献管理器导出、笔记库和项目设计，理解研究方向、已有证据和缺口，再去查找真正值得补的新文献。

它会把新结果和本地已有文献去重，标注 `already`、`near_duplicate`、`genuinely_new`、`worth_adding` 或 `low_priority_duplicate`，并分别评分：课题相关性、机制价值、实验可借鉴度、缺口填补度、本地新颖性、期刊/年份信号和证据完整度。最终输出可行动的阅读优先级报告和证据矩阵。

相比普通文献搜索工具，它的优势是：**先理解你的已有文献和项目设计，再进行查漏补缺式检索**。这更适合长期课题维护、论文写作、实验方案设计、组会准备和文献库迭代。

---

Literature Gap Radar is a local-source-first literature radar.

Most literature tools start with keywords and return a long list of papers. This project reverses the order:

1. Index your existing literature sources.
2. Infer your research profile from papers, notes, exports, and optional project designs.
3. Build a gap map covering background, mechanism, methods, controls, benchmarks, and writing or figure needs.
4. Search new literature only after the local context is understood.
5. Deduplicate candidates against your local library.
6. Score each candidate across multiple axes.
7. Export an evidence matrix and reading-priority report.

The result is not just "papers matching a keyword"; it is a ranked list of what is already covered, what is near-duplicate, what is genuinely new, and what is worth adding because it fills a specific research gap.

## Skill Or Script?

It is both:

- As a **Codex skill**, `SKILL.md` teaches an AI agent when and how to run the literature-radar workflow.
- As a **Python CLI script**, `scripts/local_first_literature.py` performs the deterministic work: indexing, profile inference, gap mapping, OpenAlex search, deduplication, scoring, triage, and report rendering.

If you use Codex, ask it to use `$literature-gap-radar`. If you prefer the command line, run the Python script directly.

## Why It Is Different

- **Local-source-first, not keyword-first**  
  It starts from what you already have before searching the web.

- **Works beyond PDF folders**  
  It accepts ordinary folders, loose PDFs/DOCX/TXT/Markdown notes, Zotero data directories or `zotero.sqlite`, RIS/NBIB/BibTeX exports, EndNote XML exports, and Obsidian vaults.

- **Research-gap aware**  
  It can use a project design, proposal, manuscript draft, or inferred profile to identify missing background, mechanism, methods, controls, and benchmark papers.

- **Deduplication built in**  
  New candidates are labeled as `already`, `near_duplicate`, `genuinely_new`, `worth_adding`, or `low_priority_duplicate`.

- **Multi-axis scoring**  
  Every candidate gets separate scores for topic relevance, mechanism value, experiment reusability, gap filling, novelty against the local library, journal/year signal, and evidence richness.

- **Evidence boundaries are visible**  
  The workflow distinguishes metadata-only hits, abstract-level evidence, local full text, methods-like text, figure captions, extraction failures, and items needing manual verification.

- **Actionable outputs**  
  It writes CSV/HTML by default and produces Excel/Word reports when `openpyxl` and `python-docx` are installed.

- **Manual triage layer**  
  It can add a second-pass, profile-driven bucket (`direct_priority`, `method_or_figure_reference`, `watchlist`, `duplicate_or_seen`, `low_priority_manual_check`) so broad searches do not become a messy reading pile.

## Supported Local Sources

| Source | How to provide it | What the radar does |
| --- | --- | --- |
| Folder of PDFs/DOCX/TXT/Markdown | `--roots "/path/to/papers"` | Extracts text, DOI, title, year, abstract/method/figure cues |
| Zotero data directory | `--roots "/path/to/Zotero"` | Reads `zotero.sqlite` metadata when accessible and scans `storage/` PDFs |
| Zotero/EndNote/Mendeley exports | `--roots export.ris export.bib export.nbib` | Parses each record separately instead of treating the export as one text blob |
| EndNote XML export | `--roots export.xml` | Parses record-level title, DOI, year, journal, abstract, authors when present |
| EndNote `.enl`/`.enlx` library | `--roots "/path/to/EndNote Library"` | Detects the proprietary library and scans attached PDFs under the path; export RIS/BibTeX/XML for full metadata |
| Obsidian vault | `--roots "/path/to/vault"` | Indexes Markdown literature notes and PDFs stored under the vault |
| Project design or manuscript | `--design design.docx proposal.md` | Uses it to infer gaps and tune search/scoring |

## Repository Layout

```text
literature-gap-radar/
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

```bash
git clone https://github.com/<your-user>/literature-gap-radar.git
cd literature-gap-radar
python -m pip install -r requirements.txt
```

The core workflow uses the Python standard library. Optional packages enable PDF extraction and Word/Excel output.

## Quick Start

Run the full pipeline:

```bash
python -X utf8 scripts/local_first_literature.py run \
  --roots "/path/to/papers" "/path/to/Zotero" "/path/to/obsidian-vault" \
  --design "/path/to/project_design.docx" \
  --years 3 \
  --max-pages 5 \
  --max-chars 20000 \
  --output-dir outputs/gap_radar_run
```

Or run step by step.

Index local sources:

```bash
python -X utf8 scripts/local_first_literature.py index \
  --roots "/path/to/papers" "/path/to/zotero.sqlite" export.ris \
  --output outputs/local_library.jsonl \
  --source-manifest outputs/source_manifest.json
```

Infer a profile:

```bash
python -X utf8 scripts/local_first_literature.py infer-profile \
  --index outputs/local_library.jsonl \
  --design "/path/to/project_design.docx" \
  --output outputs/profile.json
```

Build a gap map:

```bash
python -X utf8 scripts/local_first_literature.py gap-map \
  --profile outputs/profile.json \
  --design "/path/to/project_design.docx" \
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

Create manual triage outputs:

```bash
python -X utf8 scripts/local_first_literature.py triage \
  --scored outputs/scored.jsonl \
  --profile outputs/profile.json \
  --output-dir outputs/triage
```

## Practical Lessons

- Start large libraries with a light scan: `--max-pages 5 --max-chars 20000`. Deep full-text extraction can be rerun later on selected folders.
- Put broad but intentional `search_queries` in the profile. Avoid one over-constrained query that combines every term in the project.
- The scoring model uses title/abstract/journal evidence, not the query string, so a paper does not get a free relevance boost merely because a broad query found it.
- Use triage terms to separate direct reads from method-only or low-priority references.

## Output Files

Typical outputs include:

- `source_manifest.json`: how each supplied local source was recognized and what limitations apply.
- `local_library_index.jsonl`: local paper metadata, source adapter, attachment paths, and extraction status.
- `inferred_profile.json`: inferred research profile.
- `gap_map.json`: literature needs split by background, mechanism, methods, controls, benchmarks, and writing/figure needs.
- `candidates.jsonl`: newly searched candidates.
- `scored.jsonl`: deduplicated and scored candidates.
- `triage/manual_triage.csv`
- `triage/manual_triage.html`
- `triage/manual_triage.docx` if `python-docx` is installed.
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

The scoring goal is calibrated prioritization, not fake precision. A highly relevant duplicate should not outrank a new paper that fills an important missing method or mechanism gap.

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

```bash
python -X utf8 scripts/smoke_test.py
```

The smoke test creates a temporary mini-library, indexes loose files plus a RIS export and an Obsidian-like vault, infers a profile, builds a gap map, scores two candidates, and renders CSV/HTML plus optional Word/Excel outputs.

## Codex Skill Usage

This repository is also a Codex skill. To install it as a skill, clone it into your Codex skills folder:

```bash
git clone https://github.com/<your-user>/literature-gap-radar.git ~/.codex/skills/literature-gap-radar
```

Then ask Codex to use `$literature-gap-radar`.

## License

MIT License.
