"""Turn a file or a command run into an evidence item stored inside the proof's folder."""
import shutil
import subprocess
import time
from pathlib import Path

from . import git
from .errors import ProofError
from .store import FILES, slug


def _destination(proof, name):
    folder = proof.folder / FILES
    stem, suffix = Path(name).stem, Path(name).suffix
    dest, n = folder / name, 1
    while dest.exists():
        n += 1
        dest = folder / f"{stem}-{n}{suffix}"
    return dest


def _from_file(proof, src):
    src = Path(src)
    if not src.is_file():
        raise ProofError(f"{src} is not a file.")
    dest = _destination(proof, src.name)
    shutil.copy2(src, dest)
    return {"kind": "file", "file": f"{FILES}/{dest.name}"}


def _from_command(proof, cmd, cwd):
    run = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dest = _destination(proof, f"{slug(cmd)[:40]}.txt")
    dest.write_text(f"$ {cmd}\n{run.stdout}")
    return {"kind": "command", "cmd": cmd, "exit": run.returncode, "file": f"{FILES}/{dest.name}"}


def capture(proof, phase, caption, key, cwd, file=None, cmd=None):
    evidence = _from_file(proof, file) if file else _from_command(proof, cmd, cwd)
    return {"phase": phase, "key": key or slug(caption), "caption": caption,
            "at": time.time(), "git": git.state(cwd), **evidence}
