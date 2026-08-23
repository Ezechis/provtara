from __future__ import annotations

from pathlib import Path

from phase0.qualify import load_job
from phase1.ingest import keep_listing, merge_jobs


def load_jobs(jobs_dir: Path | str) -> list:
    directory = Path(jobs_dir)
    jobs = []
    if directory.is_dir():
        for path in sorted(directory.glob("*.yaml")):
            jobs.append(load_job(path))
    return jobs


def all_jobs(jobs_dir: Path | str, ingested: list | None = None) -> list:
    return merge_jobs(load_jobs(jobs_dir), [j for j in (ingested or []) if keep_listing(j)])


def get_job(jobs_dir: Path | str, job_id: str, ingested: list | None = None):
    for job in all_jobs(jobs_dir, ingested):
        if job.id == job_id:
            return job
    return None
