# Privacy And Open Source Boundary

`local-first-literature` is designed to be open-source friendly. Keep the public skill reusable and keep personal research data out of the repository.

## Safe To Commit

- `SKILL.md`
- generic scripts
- profile templates
- scoring rubric
- anonymized examples
- empty `outputs/.gitkeep` and `state/.gitkeep`

## Do Not Commit

- local paper indexes containing titles from a private library
- extracted paper text
- private project designs or manuscripts
- private folder paths
- generated Word/Excel reports for a user's real project
- API cache files that include private query intent

## Recommended Layout

```text
local-first-literature/
  references/research-profile-template.yaml
  scripts/local_first_literature.py
  state/        # ignored
  outputs/      # ignored

private/
  profiles/my-project.yaml
  local_library_index.jsonl
  gap_map.json
```

Personal wrapper skills can depend on this generic skill while storing their own profiles and paths separately.
