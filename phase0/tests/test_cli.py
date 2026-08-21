from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
FIXTURES = ROOT / "fixtures"
PROFILE = FIXTURES / "profile.yaml"
YES = FIXTURES / "jobs" / "yes-django-backend.yaml"
NO = FIXTURES / "jobs" / "no-k8s-sre.yaml"
NEAR = FIXTURES / "jobs" / "near-miss-k8s.yaml"


def _run(args: list[str], cwd=None) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    return subprocess.run(
        [sys.executable, "-m", "phase0", *args],
        cwd=cwd or ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


def test_cli_qualify_yes_exits_zero():
    r = _run(["qualify", str(PROFILE), str(YES)])
    assert r.returncode == 0, r.stderr + r.stdout
    assert "GATE: PASS" in r.stdout
    assert "Python" in r.stdout


def test_cli_qualify_no_exits_one_and_writes_nothing(tmp_path):
    r = _run(["qualify", str(PROFILE), str(NO)])
    assert r.returncode == 1
    assert "GATE: FAIL" in r.stdout
    assert "Kubernetes" in r.stdout
    assert list(tmp_path.iterdir()) == []


def test_cli_pack_yes_writes_files_without_kubernetes(tmp_path):
    out = tmp_path / "pack"
    r = _run(["pack", str(PROFILE), str(YES), "--out", str(out)])
    assert r.returncode == 0, r.stderr + r.stdout
    resume = (out / "resume.md").read_text(encoding="utf-8")
    letter = (out / "cover_letter.md").read_text(encoding="utf-8")
    assert "Kubernetes" not in resume
    assert "Django" in resume
    assert "Harbor Ledger" in letter
    assert (out / "gap_table.md").exists()


def test_cli_pack_no_job_does_not_write(tmp_path):
    out = tmp_path / "pack"
    r = _run(["pack", str(PROFILE), str(NO), "--out", str(out)])
    assert r.returncode == 1
    assert not out.exists()


def test_cli_pack_near_miss_needs_exception(tmp_path):
    out = tmp_path / "denied"
    r = _run(["pack", str(PROFILE), str(NEAR), "--out", str(out)])
    assert r.returncode == 1
    assert not out.exists()

    out2 = tmp_path / "allowed"
    r2 = _run(
        ["pack", str(PROFILE), str(NEAR), "--exception", "Kubernetes", "--out", str(out2)]
    )
    assert r2.returncode == 0, r2.stderr + r2.stdout
    resume = (out2 / "resume.md").read_text(encoding="utf-8")
    letter = (out2 / "cover_letter.md").read_text(encoding="utf-8")
    assert "kubernetes" not in resume.lower()
    assert "kubernetes" in letter.lower()
    assert "gap" in letter.lower()
