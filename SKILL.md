---
name: literature-gap-radar
description: "Literature Gap Radar: local-source-first literature radar that indexes a user's existing papers and citation managers (folders, Zotero sqlite/storage, EndNote RIS/BibTeX/XML exports, Obsidian/Markdown notes), infers their research profile and evidence gaps, then searches new literature, deduplicates against the local library, scores papers across multiple axes, and renders Word/Excel-ready reading priorities. Use when users ask to scan or monitor literature, avoid papers they already have, identify missing evidence for a project design, rank new papers, or build a reusable literature radar for any research field."
---

# Literature Gap Radar

Run a literature workflow that starts from the user's own literature sources before searching the web. The default output should be an actionable evidence matrix and reading-priority report, not a loose keyword list.

## Workflow

1. **Index local sources first**
   - Run `python -X utf8 scripts/local_first_literature.py index --roots <source...> --output outputs/local_library.jsonl --source-manifest outputs/source_manifest.json`.
   - Accept ordinary folders/files, Zotero data directories or `zotero.sqlite`, EndNote/Zotero/Mendeley RIS or BibTeX exports, EndNote XML exports, and Obsidian/Markdown vaults.
   - Extract DOI, title, year, journal, authors, attachment paths, text snippets, abstract-like sections, methods-like sections, figure legend cues, and evidence-read status.
   - Never move, rename, or edit the user's original literature files during indexing.
   - If an EndNote `.enl`/`.enlx` binary is supplied, index any attached PDFs under the path and record in the source manifest that RIS/BibTeX/XML export is needed for record-level metadata.

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
   - If inferred gap queries are too narrow or return no candidates, add profile-level `search_queries` and rerun search. Use 3-6 term queries that each represent one project facet instead of one over-constrained mega-query.
   - Prefer public metadata APIs that do not require keys. Record query strings and exact date windows.
   - Use journal watchlists only as filters or boosts; do not make top-journal scanning the whole method.

5. **Deduplicate and score**
   - Run `python -X utf8 scripts/local_first_literature.py score --index outputs/local_library.jsonl --candidates outputs/candidates.jsonl --profile outputs/profile.json --gap-map outputs/gap_map.json --output outputs/scored.jsonl`.
   - Label each candidate as `already`, `near_duplicate`, `genuinely_new`, `worth_adding`, or `low_priority_duplicate`.
   - Score each paper separately on topic relevance, mechanism value, experiment reusability, gap filling, novelty against local library, journal/year signal, and evidence richness.
   - Do not let the search query itself contribute to relevance scores; use query only for provenance.
   - Avoid flat scores. Use the rubric in `references/scoring-rubric.md`, then sort by calibrated total score.

6. **Manual triage layer**
   - Run `python -X utf8 scripts/local_first_literature.py triage --scored outputs/scored.jsonl --profile outputs/profile.json --output-dir outputs/triage`.
   - Use `direct_priority_terms`, `method_priority_terms`, and `deprioritize_terms` in the profile to bucket papers into `direct_priority`, `method_or_figure_reference`, `watchlist`, `duplicate_or_seen`, and `low_priority_manual_check`.
   - Treat triage as a reading-priority aid, not as a substitute for full-text judgment.

7. **Render outputs**
   - Run `python -X utf8 scripts/local_first_literature.py render --scored outputs/scored.jsonl --output-dir outputs/report`.
   - Prefer Excel evidence matrices and Word reports when `openpyxl` and `python-docx` are available. Always also write CSV/HTML fallbacks.
   - Include evidence boundaries: title/abstract only, full text available, methods seen, figure legends seen, extraction failed, or manual verification needed.

## Large Library Rule

- For a first run on a large folder, start with `--max-pages 5 --max-chars 20000`; this usually captures title/DOI/abstract/method cues without stalling on hundreds of PDFs.
- After the radar identifies top candidates or local clusters, rerun a deeper index only for selected folders or papers.
- If a run appears stuck during PDF extraction, stop it and rerun with lighter limits rather than launching duplicate jobs.

## Source Adapters

- **Folders and loose files**: index PDFs, DOCX, TXT, Markdown, and CSV notes as local full-text or note evidence.
- **Zotero**: pass a Zotero data directory or `zotero.sqlite`; the script reads article metadata when the database is accessible and also scans `storage/` PDFs.
- **EndNote**: prefer RIS, BibTeX, or XML exports; proprietary `.enl`/`.enlx` files are detected but not parsed directly.
- **Obsidian**: pass the vault folder; Markdown literature notes are indexed, and PDFs under the vault are scanned.
- **Reference exports**: RIS, NBIB, BibTeX, and EndNote XML are parsed record by record instead of as one undifferentiated text file.

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
  --roots "/path/to/papers" "/path/to/Zotero" "/path/to/obsidian-vault" \
  --design "/path/to/project_design.docx" \
  --years 3 \
  --output-dir outputs/gap_radar_run
```

```bash
python -X utf8 scripts/local_first_literature.py render \
  --scored outputs/gap_radar_run/scored.jsonl \
  --output-dir outputs/gap_radar_run/report
```

```bash
python -X utf8 scripts/local_first_literature.py triage \
  --scored outputs/gap_radar_run/scored.jsonl \
  --profile outputs/gap_radar_run/inferred_profile.json \
  --output-dir outputs/gap_radar_run/triage
```
