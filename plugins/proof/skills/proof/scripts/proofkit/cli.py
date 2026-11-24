import argparse
import sys
from pathlib import Path

from . import capture, config, hook, render, rules
from .errors import ProofError
from .store import PHASES, REPORT, Proof


def _start(args, home):
    proof = Proof.start(home, args.title, config.before_enabled(args.before, home))
    step = "capture the baseline with `proof add before`" if proof.before else "the before step is off"
    print(f"Started \"{proof.title}\" in {proof.folder}: {step}.")


def _add(args, home):
    proof = Proof.require_current(home)
    rules.check_add(proof, args.phase)
    where = Path(args.in_dir) if args.in_dir else Path.cwd()
    if not where.is_dir():
        raise ProofError(f"{where} is not a folder.")
    item = capture.capture(proof, args.phase, args.caption, args.key, where, file=args.file, cmd=args.cmd)
    proof.add_item(item)
    tail = f" (exit {item['exit']})" if item["kind"] == "command" else ""
    print(f"Added {args.phase} evidence \"{item['key']}\": {item['file']}{tail}.")


def _unproven(args, home):
    Proof.require_current(home).add_unproven(args.text)
    print("Added to Not proven.")


def _build(args, home):
    proof = Proof.require_current(home)
    found = rules.problems(proof)
    if found:
        raise ProofError("Not ready to build:\n- " + "\n- ".join(found))
    proof.mark_built(args.summary)
    report = proof.folder / REPORT
    report.write_text(render.render(proof))
    print(report)


def _status(args, home):
    proof = Proof.current(home)
    if proof is None:
        print("No open proof.")
        return
    counts = ", ".join(f"{len(proof.items_in(p))} {p}" for p in PHASES)
    print(f"{proof.title}\n  folder: {proof.folder}\n  before step: {'on' if proof.before else 'off'}\n"
          f"  evidence: {counts}\n  not proven: {len(proof.unproven)}\n  built: {'yes' if proof.built else 'no'}")
    for line in rules.problems(proof):
        print(f"  - {line}")


def _drop(args, home):
    Proof.close(home)
    print("Closed the open proof. Its folder stays.")


def _parser():
    p = argparse.ArgumentParser(prog="proof", description="Collect before and after evidence and render PROOF.md.")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("start", help="open a proof for a piece of work")
    s.add_argument("title")
    s.add_argument("--before", dest="before", action="store_true", default=None, help="capture a baseline first")
    s.add_argument("--no-before", dest="before", action="store_false", help="skip the baseline, after evidence only")
    s.set_defaults(run=_start)

    a = sub.add_parser("add", help="capture one piece of evidence")
    a.add_argument("phase", choices=PHASES)
    source = a.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="a screenshot, clip, log or other file to copy in")
    source.add_argument("--cmd", help="a shell command to run now; its output and exit code are kept")
    a.add_argument("--caption", required=True, help="one line: what this shows")
    a.add_argument("--key", help="pairs a before with its after; defaults to the caption's slug")
    a.add_argument("--in", dest="in_dir", help="run --cmd and read git state in this folder, such as a temporary "
                                               "worktree at the old commit; the proof stays in this worktree")
    a.set_defaults(run=_add)

    u = sub.add_parser("unproven", help="note something this proof does not show")
    u.add_argument("text")
    u.set_defaults(run=_unproven)

    b = sub.add_parser("build", help="check the evidence and write PROOF.md")
    b.add_argument("--summary", required=True, help="what changed, in one to three plain lines")
    b.set_defaults(run=_build)

    sub.add_parser("status", help="show the open proof").set_defaults(run=_status)
    sub.add_parser("drop", help="close the open proof without building it").set_defaults(run=_drop)

    h = sub.add_parser("hook", help="Claude Code hook entry points")
    h.add_argument("event", choices=["stop"])
    return p


def main(argv=None):
    args = _parser().parse_args(argv)
    if args.command == "hook":
        return hook.stop(sys.stdin)
    try:
        args.run(args, config.proof_home())
    except ProofError as e:
        print(e, file=sys.stderr)
        return 1
    return 0
