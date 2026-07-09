# Scoring Rubric

Use this rubric when ranking literature after local-library deduplication.

## Axes

- `topic_relevance`: Does the paper directly match the user's research object, core topics, and constraints?
- `mechanism_value`: Does it clarify a causal mechanism, pathway, physical principle, or theory needed by the project?
- `experiment_reusability`: Are the methods, controls, readouts, timing, models, or figure designs directly reusable?
- `gap_fill`: Does it fill a named gap from the project design, manuscript, proposal, or inferred profile?
- `novelty_against_local`: Is it absent from the local library, not just a duplicate of what the user already has?
- `journal_year_signal`: Is it recent, influential, or from a target journal without making rankings a hard gate?
- `evidence_richness`: How much evidence was available to the agent: title only, abstract, full text, methods, figures, supplements?

## Labels

- `already`: DOI or near-exact title already exists locally.
- `near_duplicate`: Very similar title/topic exists locally, but DOI or metadata differs.
- `genuinely_new`: Not found locally and relevant enough to inspect.
- `worth_adding`: New and fills a named gap or provides a reusable method.
- `low_priority_duplicate`: Relevant but largely redundant with the local library.

## Calibration

Avoid assigning identical scores to many papers. Strong papers should differ because one may be mechanism-rich, another method-rich, another only background-useful, and another mostly redundant.

Use a stable deterministic tie-breaker only for sorting papers with otherwise similar evidence; never let the tie-breaker override scientific reasoning.

## Evidence Boundary

Always distinguish these situations:

- metadata only
- title and abstract available
- local full text extracted
- methods-like text found
- figure legends or captions found
- extraction failed or manual verification needed

Do not infer impact factor, experimental details, or causal evidence when the source text does not support it.
