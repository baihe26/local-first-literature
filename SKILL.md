---
name: local-first-literature
description: Local-first literature radar that first indexes a user's existing papers, infers their research profile and evidence gaps, then searches new literature, deduplicates against the local library, scores papers across multiple axes, and renders Word/Excel-ready reading priorities. Use when users ask to scan or monitor literature from a local paper library, avoid papers they already have, identify missing evidence for a project design, rank new papers, or build a reusable literature radar for any research field.
---

# Local-First Literature

Run a literature workflow that starts from the user's own paper library before searching the web. The default output should be an actionable evidence matrix and reading-priority report, not a loose keyword list.

## Workflow

1. **Index local papers first**
   - Run `python -X utf8 scripts/local_first_literature.py index --roots <folder...> --output outputs/local_library.jsonl`.
   - Extract DOI, title, year, text snippets, abstract-like sections, methods-like sections, figure legend cues, and evidence-read status.
   - Never move, rename, or edit the user's original literature files during indexing.

2. **Infer the research profile**
   - Run `python -X utf8 scripts/local_first_literature.py infer-profile --index outputs/local_library.jsonl --output outputs/profile.json`.
   - If the user provides core papers, a project design, proposal, or manuscript draft, include it with `--design <file...>`.
   - Treat the inferred profile as a draft: it guides search and scoring, but explicit user instructions override it.

3. **Build a gap map**
   - Run `python -X utf8 scripts/local_first_literature.py gap-map --profile outputs/profile.json --design <file...> --output outputs/gap_map.json`.
   - If no design is available, create a profile-derived gap map covering background, mechanism, methods, controls, benchmarks, and writing/figure needs.
   - Mark each gap with the type of literature needed: background, mechanism, method, benchmark, control, or synthesis.

4. **Search after understanding the library**
   - Run `python -X utf8 scripts/local_first_literature.py search --profile outputs/profile.json --gap-map outputs/gap_map.json --years 3 --output outputs/candidates.jsonl`.
   - Prefer public metadata APIs that do not require keys. Record query strings and exact date windows.
   - Use journal watchlists only as filters or boosts; do not make top-journal scanning the whole method.

5. **Deduplicate and score**
   - Run `python -X utf8 scripts/local_first_literature.py score --index outputs/local_library.jsonl --candidates outputs/candidates.jsonl --profile outputs/profile.json --gap-map outputs/gap_map.json --output outputs/scored.jsonl`.
   - Label each candidate as `already`, `near_duplicate`, `genuinely_new`, `worth_adding`, or `low_priority_duplicate`.
   - Score each paper separately on topic relevance, mechanism value, experiment reusability, gap filling, novelty against local library, journal/year signal, and evidence richness.
   - Avoid flat scores. Use the rubric in `references/scoring-rubric.md`, then sort by calibrated total score.

6. **Render outputs**
   - Run `python -X utf8 scripts/local_first_literature.py render --scored outputs/scored.jsonl --output-dir outputs/report`.
   - Prefer Excel evidence matrices and Word reports when `openpyxl` and `python-docx` are available. Always also write CSV/HTML fallbacks.
   - Include evidence boundaries: title/abstract only, full text available, methods seen, figure legends seen, extraction failed, or manual verification needed.

## Modes

- **`quick`**: index local files and score a short external candidate list.
- **`gap`**: focus on project-design evidence gaps and search targeted method/mechanism papers.
- **`weekly`**: maintain a reading queue and mark already-seen items.
- **`audit`**: re-check an existing literature folder for duplicates, weak categories, or missing evidence.
- **`open-source`**: keep private paths, local indexes, and user-specific profiles out of committed files.

## Privacy Rules

- Keep local paths, private project profiles, local indexes, scan states, and generated outputs under `state/`, `outputs/`, or user-selected external folders.
- Do not commit real local-library indexes or user paper text to public repositories.
- Use `references/research-profile-template.yaml` for public examples and put personal profiles in ignored paths.

## Scoring Rules

- Read `references/scoring-rubric.md` before changing scoring logic or explaining scores.
- Give a one-sentence rationale for high-priority items.
- Penalize duplicates even if they are highly relevant.
- Boost papers that fill a named gap, provide reusable methods, or clarify a mechanism the project depends on.
- Do not invent impact factors, rankings, methods, or evidence from inaccessible files.

## Useful Commands

```bash
python -X utf8 scripts/local_first_literature.py run \
  --roots "D:\path\to\papers" \
  --design "D:\path\to\project_design.docx" \
  --years 3 \
  --output-dir outputs/local_first_run
```

```bash
python -X utf8 scripts/local_first_literature.py render \
  --scored outputs/local_first_run/scored.jsonl \
  --output-dir outputs/local_first_run/report
```
