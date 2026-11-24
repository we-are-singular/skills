"""The Stop hook: while a proof is open and unbuilt, the agent can't end its turn without finishing it."""
import json

from . import config, rules
from .store import Proof


def stop(stdin):
    raw = stdin.read()
    event = json.loads(raw) if raw.strip() else {}
    # Claude Code sets stop_hook_active when this hook already blocked once: let the turn end then.
    if event.get("stop_hook_active"):
        return 0
    proof = Proof.current(config.proof_home(event.get("cwd")))
    if proof is None or proof.built:
        return 0
    steps = rules.problems(proof) or ["The evidence is complete. Run `proof build --summary \"...\"`."]
    reason = (f"The proof \"{proof.title}\" is open and not built.\n- " + "\n- ".join(steps) +
              "\nIf this work needs no proof after all, run `proof drop`.")
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0
