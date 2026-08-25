"""Shared helper for loading and cross-referencing the site's _data/*.yml files."""

from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "_data"

_COLLECTIONS = [
    "skills",
    "education",
    "experience",
    "teaching",
    "publications",
    "projects",
    "datasets",
]


def load_data():
    """Return a dict of {collection_name: [entries]} for every _data collection."""
    data = {}
    for name in _COLLECTIONS:
        path = DATA_DIR / f"{name}.yml"
        with path.open(encoding="utf-8") as f:
            data[name] = yaml.safe_load(f) or []
    return data


def index_by_id(entries):
    """Return {entry['id']: entry} for a list of data entries."""
    return {entry["id"]: entry for entry in entries}


def skill_names(data, skill_ids):
    """Resolve a list of skill ids to their display names."""
    skills_by_id = index_by_id(data["skills"])
    return [skills_by_id[s]["name"] for s in skill_ids if s in skills_by_id]


def matches_audience(entry, audience):
    return audience in (entry.get("audience") or [])


def matches_any_skill(entry, skill_ids):
    if not skill_ids:
        return True
    return bool(set(entry.get("skills") or []) & set(skill_ids))
