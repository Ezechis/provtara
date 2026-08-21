from __future__ import annotations

import argparse
import sys
from pathlib import Path

from phase0.models import GateFailed, TruthFailed
from phase0.pack import prepare_pack, write_pack
from phase0.qualify import load_job, load_profile, qualify


def _print_gaps(gaps) -> None:
    print(f"{'Requirement':<32} {'Verdict':<10} Evidence")
    print("-" * 72)
    for row in gaps:
        ev = ", ".join(row.evidence) if row.evidence else "—"
        print(f"{row.requirement:<32} {row.verdict:<10} {ev}")


def cmd_qualify(profile_path: Path, job_path: Path, exception_for: list[str]) -> int:
    profile = load_profile(profile_path)
    job = load_job(job_path)
    result = qualify(profile, job, exception_for=exception_for or None)
    print(f"job: {job.id}  {job.title} @ {job.company}")
    print(f"candidate: {profile.name}  ({profile.years_experience} years since {profile.career_start})")
    print()
    _print_gaps(result.gaps)
    print()
    if result.passed:
        extra = f" (exceptions: {', '.join(result.exceptions)})" if result.exceptions else ""
        print(f"GATE: PASS{extra}")
        return 0
    print("GATE: FAIL  " + ", ".join(result.failed_must_haves))
    print("No pack will be written. The system does not invent missing skills.")
    return 1


def cmd_pack(profile_path: Path, job_path: Path, exception_for: list[str], out: Path) -> int:
    profile = load_profile(profile_path)
    job = load_job(job_path)
    try:
        pack = prepare_pack(profile, job, exception_for=exception_for or None)
    except GateFailed as exc:
        print(f"GATE FAILED: {exc}", file=sys.stderr)
        print("No pack written.", file=sys.stderr)
        return 1
    except TruthFailed as exc:
        print(f"TRUTH FAILED: {exc}", file=sys.stderr)
        print("No pack written. Fix the claim, never the checker.", file=sys.stderr)
        return 2
    write_pack(pack, out)
    _print_gaps(pack.gaps)
    print()
    print(f"Wrote {out / 'resume.md'}")
    print(f"Wrote {out / 'cover_letter.md'}")
    print(f"Wrote {out / 'gap_table.md'}")
    print("Hand this pack to the candidate. Do not submit it for them.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="phase0",
        description="IT job workshop Phase 0: gap table, gate, honest pack. Never submits.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("qualify", help="Print the gap table and gate result")
    q.add_argument("profile")
    q.add_argument("job")
    q.add_argument("--exception", action="append", default=[], help="Must-have the candidate accepts as a named gap")

    p = sub.add_parser("pack", help="Write resume + letter if the gate and truth check pass")
    p.add_argument("profile")
    p.add_argument("job")
    p.add_argument("--exception", action="append", default=[], help="Must-have the candidate accepts as a named gap")
    p.add_argument("--out", default="out", help="Output directory")

    args = parser.parse_args(argv)
    profile = Path(args.profile)
    job = Path(args.job)
    if args.cmd == "qualify":
        return cmd_qualify(profile, job, args.exception)
    if args.cmd == "pack":
        return cmd_pack(profile, job, args.exception, Path(args.out))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
