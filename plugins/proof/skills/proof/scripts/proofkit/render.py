"""Render a proof as Markdown that reads on its own and pastes into a pull request."""
from pathlib import Path

from .store import PHASES

TAIL_LINES = 40
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def _grouped(items):
    groups = {}
    for item in items:
        groups.setdefault(item["key"], []).append(item)
    return groups


def _where(item):
    state = item.get("git")
    if not state:
        return ""
    return f" at `{state['commit']}`" + (" with uncommitted changes" if state["dirty"] else "")


def _evidence(folder, item):
    path = item["file"]
    if item["kind"] == "command":
        lines = (folder / path).read_text().splitlines()
        cut = lines[-TAIL_LINES:]
        note = f"exit {item['exit']}" + (f", last {TAIL_LINES} lines, full output in `{path}`" if len(lines) > TAIL_LINES else "")
        return "```\n" + "\n".join(cut) + f"\n```\n_{note}_"
    if Path(path).suffix.lower() in IMAGE_SUFFIXES:
        return f"![{item['caption']}]({path})"
    return f"[{Path(path).name}]({path})"


def render(proof):
    out = [f"# {proof.title} · Proof", ""]
    if proof.summary:
        out += [proof.summary, ""]
    for group in _grouped(proof.items).values():
        caption = next((i["caption"] for i in group if i["phase"] == "after"), group[0]["caption"])
        out += [f"### {caption}", ""]
        for phase in PHASES:
            for item in (i for i in group if i["phase"] == phase):
                if proof.before:
                    out += [f"**{phase.title()}**{_where(item)}", ""]
                out += [_evidence(proof.folder, item), ""]
    out += ["## Not proven", ""]
    out += [f"- {text}" for text in proof.unproven] or ["- Nothing listed."]
    return "\n".join(out) + "\n"
