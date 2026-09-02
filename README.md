# Lethal Company AI Modding Project

Current canonical project state: **S1.31**

Current gameplay profile:

`Profiles/LC V1 S1.31 Indoor Power Trim -4.r2z`

## ChatGPT — read first

A new ChatGPT conversation should use the machine-readable repository content in this order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/03_PROJECT_CHRONOLOGY.md`
8. `Current/Projektstatus_S1.31.json`
9. `Current/Aktive_Modliste_S1.31.txt`

Then inspect `Profiles/`, `Logs/`, and `References/` according to the task.

## Markdown-first rule

`.md`, `.txt`, and `.json` files are the **primary machine-readable handover sources**.

`Current/HumanReadable/` contains PDF/DOCX versions for human reading, visual layout verification, and archival reference. A GitHub PDF viewer failure must **not** block project takeover if the corresponding machine-readable sources are available.

For GitHub text files, ChatGPT should prefer the raw file content when useful. A repository URL of the form:

`https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/blob/main/PATH`

can usually be read directly as raw content at:

`https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/PATH`

## Repository structure

- `Current/` — current machine-readable state and metadata
- `Current/HumanReadable/` — current DOCX/PDF secondary documents
- `Profiles/` — Gale/r2modman `.r2z` profiles
- `Logs/` — runtime logs and diagnostic summaries
- `References/` — binding screenshots and reference values
- `Archive/` — older primary sources retained for historical diagnosis

## Priority rule

The chronologically newest confirmed information overrides older assumptions.

Files under `Archive/` are historical references and must not override a newer confirmed project state unless current documentation explicitly points back to them.

Do not repeat solutions documented as failed or obsolete without new evidence.

## Repository-update rule

At the end of a work phase, update both:

1. machine-readable Markdown/TXT/JSON primary documentation, and
2. human-readable PDF/DOCX secondary documentation when useful.

Do not make the repository dependent on ZIP-only handovers.
