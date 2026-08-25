# schillingerkurs.github.io

Felix Schilling's personal/academic site: research, projects, teaching, and a CV. Built with Jekyll on the [academicpages](https://academicpages.github.io/)/[Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme, deployed via GitHub Pages' native Jekyll build (push to the default branch, no custom CI).

## Content model

The underlying facts — skills, education, work experience, teaching, publications, projects, datasets — live as structured data in `_data/*.yml`, not as hand-written prose on each page. Every entry has a stable `id`, a `type`, and (where relevant) `audience` tags (`recruiter`, `academic`, `public`) and `skills` tags referencing `_data/skills.yml`.

Pages under `_pages/` are thin Liquid templates that loop over this data through small includes in `_includes/data/` (`education-item.html`, `experience-item.html`, `teaching-item.html`, `publication-item.html`, `project-item.html`, `skill-list.html`). This means the same facts can be reused elsewhere — the website, a tailored CV draft, a dataset documentation page — without re-typing them.

| Data file | Rendered on |
| --- | --- |
| `_data/education.yml`, `_data/experience.yml`, `_data/skills.yml` | `/` (about) |
| `_data/publications.yml` | `/research/` |
| `_data/projects.yml` (all but `rare-earth-africa`) | `/projects/` |
| `_data/projects.yml` (`rare-earth-africa`) | `/portfolio/` |
| `_data/teaching.yml` | `/teaching_ta/` |
| `_data/datasets.yml` | not rendered on the site directly — used by the dataset-draft generator (below) |

### Adding content

- **New publication**: append an entry to `_data/publications.yml` with a unique `id`. No page edit needed — `/research/` picks it up automatically based on its `status` (`working_paper` / `under_review`).
- **New project**: append an entry to `_data/projects.yml`; add an `_data/datasets.yml` entry too if it has an associated dataset worth documenting separately. Drop any images under `_pages/image/<something>/` and reference them with a root-relative path (`/image/<something>/file.png`).
- **New skill tag**: append to `_data/skills.yml`, then reference its `id` from any `skills:` list elsewhere.
- **Nav item**: edit `_data/navigation.yml`.

## Generating tailored drafts

`_tools/generate_draft.py` reads the same `_data/*.yml` files and writes an editable Markdown **draft** — not a finished, ready-to-send document — into `_generated/` (git-ignored). Always read and hand-edit the draft before using it.

Setup:
```
python3 -m venv .venv && source .venv/bin/activate
pip install -r _tools/requirements.txt
```

Draft a CV tailored to a role, filtered by audience and skills:
```
python3 _tools/generate_draft.py cv \
  --audience recruiter --skills python,geospatial-analysis,econometrics \
  --role "Data Scientist" --employer "Acme Corp"
```

Draft dataset documentation for a project:
```
python3 _tools/generate_draft.py dataset --project mining-licenses-africa --audience public
```

## Local development

```
bundle exec jekyll serve
```
`_config.dev.yml` supplies local overrides (localhost URL, etc.) layered on top of `_config.yml`.

## Privacy

This site uses no analytics or tracking scripts. See `/terms/` for details — don't reintroduce Google Analytics or a similar tracker without revisiting that decision (it was removed deliberately; see git history).

## Credits

Built on the [academicpages](https://academicpages.github.io/) template (forked, then detached, by [Stuart Geiger](https://github.com/staeiou)), itself based on the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/), © 2016 Michael Rose, MIT License (see `LICENSE.md`).
