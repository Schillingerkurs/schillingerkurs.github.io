#!/usr/bin/env python3
"""Generate an editable Markdown draft of a deliverable (CV, dataset doc) from
the site's structured _data/*.yml content.

Output is a DRAFT, not a finished document — always read it and edit the
wording before sending it anywhere. See ../README.md for usage examples.
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

from data_loader import DATA_DIR, index_by_id, load_data, matches_any_skill, matches_audience

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = REPO_ROOT / "_generated"


def load_author():
    config_path = REPO_ROOT / "_config.yml"
    with config_path.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("author", {})


def slugify(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")


def cmd_cv(args, data):
    audiences = [a.strip() for a in args.audience.split(",")] if args.audience else ["recruiter"]
    skill_ids = [s.strip() for s in args.skills.split(",")] if args.skills else []

    def aud_ok(entry):
        return any(matches_audience(entry, a) for a in audiences)

    education = [e for e in data["education"] if aud_ok(e)]
    experience = [e for e in data["experience"] if aud_ok(e) and matches_any_skill(e, skill_ids)]
    projects = [p for p in data["projects"] if aud_ok(p) and matches_any_skill(p, skill_ids)]
    publications = []
    if "academic" in audiences:
        publications = [p for p in data["publications"] if aud_ok(p) and matches_any_skill(p, skill_ids)]

    if skill_ids:
        skills = [s for s in data["skills"] if s["id"] in skill_ids]
    else:
        skills = data["skills"]
    skills_by_category = {}
    for s in skills:
        skills_by_category.setdefault(s["category"], []).append(s["name"])

    author = load_author()
    lines = []
    header = author.get("name", "")
    if args.role:
        header += f" — {args.role}"
    if args.employer:
        header += f" (draft for {args.employer})"
    lines.append(f"# {header}")
    if author.get("email"):
        lines.append(f"\n{author['email']}")
    lines.append("\n<!-- TODO: write a summary tailored to this role -->")

    if skills_by_category:
        lines.append("\n## Skills")
        for category, names in skills_by_category.items():
            lines.append(f"\n**{category.replace('-', ' ').title()}:** {', '.join(names)}")

    if experience:
        lines.append("\n## Experience")
        for e in experience:
            span = e["end"] if e["end"] == e.get("start") else f"{e.get('start', '')}–{e['end']}"
            lines.append(f"\n### {e['role']}, {e['employer']} ({span})")
            for b in e.get("bullets", []):
                lines.append(f"- {b}")

    if education:
        lines.append("\n## Education")
        for e in education:
            lines.append(f"- {e['degree']} in {e['field']}, {e['institution']}, {e['end']}")

    if projects:
        lines.append("\n## Selected Projects")
        for p in projects:
            lines.append(f"\n**{p['title']}**: {p['summary'].strip()}")

    if publications:
        lines.append("\n## Selected Publications")
        for p in publications:
            lines.append(f"\n**{p['title']}**")

    return "\n".join(lines) + "\n"


def cmd_dataset(args, data):
    datasets_by_id = index_by_id(data["datasets"])
    projects_by_id = index_by_id(data["projects"])

    dataset = datasets_by_id.get(args.project)
    if dataset is None:
        project = projects_by_id.get(args.project)
        if project is None:
            sys.exit(f"error: no dataset or project found with id '{args.project}'")
        dataset = next(
            (d for d in data["datasets"] if d.get("related_project_id") == project["id"]),
            None,
        )
        if dataset is None:
            sys.exit(
                f"error: project '{args.project}' has no associated dataset in _data/datasets.yml"
            )

    related_project = projects_by_id.get(dataset.get("related_project_id"))

    lines = [f"# {dataset['name']}", f"\n{dataset['description'].strip()}"]
    lines.append(f"\n**Geographic coverage:** {dataset.get('geographic_coverage', '')}")
    lines.append(f"\n**Time coverage:** {dataset.get('time_coverage', '')}")

    if dataset.get("sources"):
        lines.append("\n## Sources")
        for s in dataset["sources"]:
            lines.append(f"- {s}")

    lines.append("\n## Variables")
    if dataset.get("variables"):
        lines.append("\n| Name | Description |")
        lines.append("| --- | --- |")
        for v in dataset["variables"]:
            lines.append(f"| {v.get('name', '')} | {v.get('description', '')} |")
    else:
        lines.append("\n<!-- TODO: list variables/fields -->")

    lines.append(f"\n**Format:** {dataset.get('format', '')}")
    lines.append(f"\n**Access:** {dataset.get('access', '')}")
    lines.append(f"\n**License:** {dataset.get('license', '')}")
    lines.append(f"\n**Contact:** {dataset.get('contact', '')}")

    related_pubs = [
        p
        for p in data["publications"]
        if related_project and set(p.get("skills") or []) & set(related_project.get("skills") or [])
    ]
    if related_pubs:
        lines.append("\n## Related publications")
        for p in related_pubs:
            lines.append(f"- {p['title']}")

    lines.append("\n<!-- TODO: confirm suggested citation -->")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    cv = sub.add_parser("cv", help="Draft a CV tailored to an audience/skill set")
    cv.add_argument("--audience", default="recruiter", help="Comma-separated audience tags")
    cv.add_argument("--skills", default="", help="Comma-separated skill ids to filter by")
    cv.add_argument("--role", default="", help="Target role title")
    cv.add_argument("--employer", default="", help="Target employer name")
    cv.add_argument("--out", default="", help="Output path (default: auto-named under _generated/)")

    ds = sub.add_parser("dataset", help="Draft dataset documentation for a project/dataset id")
    ds.add_argument("--project", required=True, help="A projects.yml or datasets.yml id")
    ds.add_argument("--audience", default="public", help="Comma-separated audience tags (informational)")
    ds.add_argument("--out", default="", help="Output path (default: auto-named under _generated/)")

    args = parser.parse_args()
    data = load_data()

    if args.command == "cv":
        content = cmd_cv(args, data)
        default_name = f"cv_{slugify(args.employer or args.role or 'draft')}_{date.today()}.md"
    elif args.command == "dataset":
        content = cmd_dataset(args, data)
        default_name = f"dataset_{slugify(args.project)}_{date.today()}.md"
    else:
        parser.error("unknown command")
        return

    out_path = Path(args.out) if args.out else GENERATED_DIR / default_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
