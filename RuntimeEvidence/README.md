# RuntimeEvidence

Persisted runtime evidence ingested from `RuntimeInbox/Current/`.

Each run is stored under:

`RuntimeEvidence/<build_id>/<UTC timestamp>/`

with:
- `raw/` — byte-identical uploaded files;
- `extracted/` — safely extracted ZIP/R2Z content when applicable;
- `INDEX.json` — filenames, sizes, SHA-256 values, and extraction inventory.

Chronologically newer runtime evidence overrides untested assumptions when evaluating behavior.
