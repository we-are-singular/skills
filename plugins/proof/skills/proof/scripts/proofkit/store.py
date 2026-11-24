"""A proof on disk: .proof/<stamp>-<slug>/proof.json, its captured files, and the `current` pointer."""
import json
import re
import time

from .errors import ProofError

PHASES = ("before", "after")
MANIFEST = "proof.json"
POINTER = "current"
FILES = "files"
REPORT = "PROOF.md"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "proof"


class Proof:
    def __init__(self, folder, data):
        self.folder = folder
        self.data = data

    @property
    def title(self):
        return self.data["title"]

    @property
    def before(self):
        return self.data["before"]

    @property
    def items(self):
        return self.data["items"]

    @property
    def unproven(self):
        return self.data["unproven"]

    @property
    def summary(self):
        return self.data.get("summary")

    @property
    def built(self):
        return self.data.get("built") is not None

    def items_in(self, phase):
        return [i for i in self.items if i["phase"] == phase]

    @classmethod
    def start(cls, home, title, before):
        home.mkdir(parents=True, exist_ok=True)
        ignore = home / ".gitignore"
        if not ignore.exists():
            ignore.write_text("*\n")
        base = f"{time.strftime('%Y%m%d-%H%M%S')}-{slug(title)}"
        folder, n = home / base, 1
        while folder.exists():
            n += 1
            folder = home / f"{base}-{n}"
        (folder / FILES).mkdir(parents=True)
        proof = cls(folder, {"title": title, "created": time.time(), "before": before,
                             "items": [], "unproven": [], "summary": None, "built": None})
        proof.save()
        (home / POINTER).write_text(folder.name + "\n")
        return proof

    @classmethod
    def current(cls, home):
        pointer = home / POINTER
        if not pointer.is_file():
            return None
        folder = home / pointer.read_text().strip()
        manifest = folder / MANIFEST
        if not manifest.is_file():
            return None
        return cls(folder, json.loads(manifest.read_text()))

    @classmethod
    def require_current(cls, home):
        proof = cls.current(home)
        if proof is None:
            raise ProofError("No open proof here. Start one with `proof start \"<title>\"`.")
        return proof

    @staticmethod
    def close(home):
        (home / POINTER).unlink(missing_ok=True)

    def save(self):
        (self.folder / MANIFEST).write_text(json.dumps(self.data, indent=2) + "\n")

    def touch(self):
        """Any new evidence or note reopens a built proof, so PROOF.md is never stale."""
        self.data["built"] = None
        self.save()

    def add_item(self, item):
        self.items.append(item)
        self.touch()

    def add_unproven(self, text):
        self.unproven.append(text)
        self.touch()

    def mark_built(self, summary):
        self.data["summary"] = summary
        self.data["built"] = time.time()
        self.save()
