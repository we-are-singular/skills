"""The few git facts a proof records. Every call tolerates a folder that isn't a repo."""
import subprocess
from pathlib import Path


def _run(args, cwd):
    try:
        done = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return done.stdout.strip()


def toplevel(cwd):
    out = _run(["rev-parse", "--show-toplevel"], cwd)
    return Path(out) if out else None


def state(cwd):
    """{commit, dirty} at the moment evidence is captured, or None outside a repo."""
    commit = _run(["rev-parse", "--short", "HEAD"], cwd)
    if commit is None:
        return None
    return {"commit": commit, "dirty": bool(_run(["status", "--porcelain"], cwd))}
