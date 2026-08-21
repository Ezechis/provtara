# Phase 0 — product in miniature

CLI only. No website. No Submit.

One confirmed profile. Three jobs (yes / no / near-miss). A gap table. A gate. A pack that **will not write** if the résumé would contain a skill not in the profile.

Fixture candidate **Jordan Hale** is fictional. Not a real person.

## Run tests

From this directory:

```
py -3 -m pytest -q
```

Expect 18 passed.

## Run the three jobs

```
set PYTHONPATH=src

py -3 -m phase0 qualify fixtures\profile.yaml fixtures\jobs\yes-django-backend.yaml
py -3 -m phase0 qualify fixtures\profile.yaml fixtures\jobs\no-k8s-sre.yaml
py -3 -m phase0 qualify fixtures\profile.yaml fixtures\jobs\near-miss-k8s.yaml

py -3 -m phase0 pack fixtures\profile.yaml fixtures\jobs\yes-django-backend.yaml --out demos\yes
py -3 -m phase0 pack fixtures\profile.yaml fixtures\jobs\no-k8s-sre.yaml --out demos\no
# exits 1 — no files

py -3 -m phase0 pack fixtures\profile.yaml fixtures\jobs\near-miss-k8s.yaml --exception Kubernetes --out demos\near-miss
```

On PowerShell use `$env:PYTHONPATH = "src"` first.

## What you should see

| Job | Gate | Pack |
|---|---|---|
| Harbor Ledger backend (Python/Django/Postgres/Docker) | PASS | resume + letter, no invented stack |
| Northpeak SRE (K8s, Go, 5+ years, US on-site) | FAIL | nothing written |
| Quayline backend (Python/Docker + Kubernetes) | FAIL unless `--exception Kubernetes` | résumé still has **no** Kubernetes; letter names the gap |

## The rule this proves

If generation stuffed Kubernetes onto a passing job’s résumé, `prepare_pack` raises `TruthFailed` and writes nothing. Fix the claim. Never the checker.
