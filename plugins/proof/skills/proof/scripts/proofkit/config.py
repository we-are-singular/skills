"""Where proofs live and whether the before step runs.

The before step is decided once, at `proof start`, in this order:
the --before / --no-before flag, then PROOF_BEFORE, then .proof/config.json's "before", then on.
"""
import json
import os
from pathlib import Path

from . import git
from .errors import ProofError

HOME_NAME = ".proof"
CONFIG_NAME = "config.json"
BEFORE_ENV = "PROOF_BEFORE"
_ON = {"1", "on", "true", "yes"}
_OFF = {"0", "off", "false", "no"}


def project_root(cwd=None):
    cwd = Path(cwd or Path.cwd())
    return git.toplevel(cwd) or cwd


def proof_home(cwd=None):
    return project_root(cwd) / HOME_NAME


def _on_off(value, source):
    if isinstance(value, bool):
        return value
    word = str(value).strip().lower()
    if word in _ON:
        return True
    if word in _OFF:
        return False
    raise ProofError(f"{source} must be on or off, not {value!r}.")


def _file_setting(home, key):
    path = home / CONFIG_NAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text()).get(key)
    except json.JSONDecodeError as e:
        raise ProofError(f"{path} is not valid JSON: {e}") from e


def before_enabled(flag, home):
    if flag is not None:
        return flag
    env = os.environ.get(BEFORE_ENV)
    if env:
        return _on_off(env, BEFORE_ENV)
    setting = _file_setting(home, "before")
    if setting is not None:
        return _on_off(setting, f"{home / CONFIG_NAME} \"before\"")
    return True
