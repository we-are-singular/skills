"""What makes a proof complete. `proof build` and the Stop hook both ask here, so they never disagree."""
from .errors import ProofError


def check_add(proof, phase):
    if phase != "before":
        return
    if not proof.before:
        raise ProofError("This proof skips the before step. Add after evidence only.")
    if proof.items_in("after"):
        raise ProofError("Before evidence has to come before any after evidence. "
                         "Start a new proof if the baseline was missed.")


def problems(proof):
    found = []
    after_keys = {i["key"] for i in proof.items_in("after")}
    if proof.before and not proof.items_in("before"):
        found.append("No before evidence. Capture the baseline with `proof add before` before changing code, "
                     "or start the proof with --no-before.")
    if not after_keys:
        found.append("No after evidence. Capture it with `proof add after`.")
    for key in dict.fromkeys(i["key"] for i in proof.items_in("before")):
        if key not in after_keys:
            found.append(f"\"{key}\" has before evidence but no after evidence.")
    return found
