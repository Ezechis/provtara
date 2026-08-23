# Provtara — Phase 1 workshop

IT jobs from **free boards** + honest tailoring. You submit. We never invent skills.

## Local

```
cd C:\Users\Ezeking\Grok\Job_Portal\phase1
py -3 -m pip install -r requirements.txt
$env:PYTHONPATH = "src;..\phase0\src"
py -3 run.py
```

http://127.0.0.1:5055

1. Open **Vacancies** (public) — listings from Remotive, Arbeitnow, RemoteOK, Jobicy, Himalayas, Hacker News Jobs, Working Nomads, The Muse, Python.org, Fossjobs, LaraJobs, and Berlin Startup Jobs, plus curated IT jobs. Boards that already sell auto-apply (We Work Remotely, 4dayweek.io) are excluded.  
2. **Apply directly** on the official board URL, or **Auto-apply** (account + confirmed résumé; gate must pass)  
3. Register → upload PDF/DOCX or paste or sample profile → confirm (unevidenced skills are struck)  
4. Auto-apply prepares a true pack (max 10). You open the official listing. Provtara never clicks Submit.  

## Tests

```
py -3 -m pytest -q
```

## Free hosting

No paid VPS required.

- **Render free:** connect this folder as a repo and use `render.yaml` at `Job_Portal/`.  
- **PythonAnywhere / Railway / Fly.io free tiers** also work: `PYTHONPATH=phase1/src:phase0/src` and `python phase1/run.py`.  
- Bind `0.0.0.0` and `$PORT` (already in `run.py`).

SQLite lives in `phase1/instance/` (ephemeral on some free hosts — fine for the workshop).
