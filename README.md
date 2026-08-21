# Job Portal — working file

IT-only job board plus honest application tailoring.

Candidate submits a real resume first. The system particularizes that resume and a matching cover letter to jobs they are actually qualified for. **It never manufactures skills to fill a gap.**

Brand locked: **Provtara**. Phase 0 CLI + Phase 1 web workshop (PDF/DOCX parse, public vacancies from Remotive / Arbeitnow / RemoteOK / Jobicy, Apply directly + Auto-apply). Domains are **not** purchased. Vercel is the wrong runtime — Flask + SQLite belongs on Render (or Railway / Fly). Tunnels into this PC are not a shareable demo. See `DEPLOY.md`.

Code: [github.com/Ezechis/provtara](https://github.com/Ezechis/provtara)

Share the Render URL, not a tunnel. One-click deploy (GitHub login, free plan, no card):

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Ezechis/provtara)

## Read in this order

1. `BRAND.md` — locked name: **Provtara**
2. `phase1/README.md` — web workshop (PDF/DOCX, free job boards, gate, download)
3. `phase0/README.md` — CLI miniature: gap table, gate, honest pack
4. `2026-08-20-platform-plan.md` — how the product works and what it takes to build
3. `next-actions.md` — GitHub handle and other unfinished grabs
3. `2026-08-20-brand-names.md` — the five names, how to say them, why they fit
4. `domain-availability.md` — `.com` `.io` `.ai` `.dev` `.tech` registry checks
5. `collisions.md` — near-neighbors, rejects, trademark notes
6. `handle-grab-status.md` — GitHub / X / Instagram / LinkedIn / Product Hunt

## Scripts

`scripts/check_names.py` and `scripts/check_names2.py` — DNS (dns.google) then RDAP sweeps used to find free names. Re-run before buying: availability changes.

```
py -3 -u scripts\check_names2.py
```

## Product intent (do not dilute)

- Strictly IT jobs
- Resume in first
- Tailor per job the candidate chooses and is qualified for
- Matching cover letter
- Never invent experience, tools, or skills
