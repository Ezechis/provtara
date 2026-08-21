# Put Provtara on a phone (free)

Vercel is built for static sites and serverless Node/Next. This app is **Flask + SQLite + live job pulls** (requests that can take several seconds). Vercel’s Python functions are short-lived, have no durable disk, and would drop the vacancy database on every cold start. Same idea as Vercel — git push, HTTPS URL, test on a phone — lives on **Render free** (or Railway / Fly).

**Do not share a tunnel.** `localhost.run`, localtunnel, and Cloudflare quick tunnels die when this PC sleeps, and many phones block them.

**Share this:** https://provtara.onrender.com

Hosted on Render free (Frankfurt). Dashboard: https://dashboard.render.com/web/srv-da4ai97qj5pc73blfs6g  
Repo: https://github.com/Ezechis/provtara

First visit after 15 minutes idle can take about a minute (spin-up). Uploaded résumés live in SQLite on an ephemeral disk, so they reset when the service sleeps.

## Lasting: Render free

Already live. Git push to `main` on `Ezechis/provtara` redeploys. Blueprint is `render.yaml`. `run.py` listens on `0.0.0.0` and `$PORT`.

## Job sources (no API keys)

| Board | What we pull |
|---|---|
| [Remotive](https://remotive.com) | `/api/remote-jobs?category=software-dev` |
| [Arbeitnow](https://www.arbeitnow.com) | job-board API |
| [RemoteOK](https://remoteok.com) | `/api` |
| [Jobicy](https://jobicy.com) | `/api/v2/remote-jobs` |

IT-only filter. Dedupe by apply URL. **Apply directly** goes to that official URL. **Auto-apply** prepares a true pack for gate-pass jobs, then you open the same URL. Provtara does not log into an ATS or press Submit.
