# Put Provtara on a phone (free)

Vercel is built for static sites and serverless Node/Next. This app is **Flask + SQLite + live job pulls** (requests that can take several seconds). Vercel’s Python functions are short-lived, have no durable disk, and would drop the vacancy database on every cold start. Same idea as Vercel — git push, HTTPS URL, test on a phone — lives on **Render free** (or Railway / Fly).

**Do not share a tunnel.** `localhost.run`, localtunnel, and Cloudflare quick tunnels die when this PC sleeps, and many phones block them. Share the `onrender.com` URL instead.

## Lasting: Render free

1. Push `C:\Users\Ezeking\Grok\Job_Portal` to GitHub.
2. [render.com](https://render.com) → New → Blueprint → this repo (`render.yaml`).
3. Free web service. Open the `onrender.com` URL on your phone.

`run.py` already listens on `0.0.0.0` and `$PORT`.

## Job sources (no API keys)

| Board | What we pull |
|---|---|
| [Remotive](https://remotive.com) | `/api/remote-jobs?category=software-dev` |
| [Arbeitnow](https://www.arbeitnow.com) | job-board API |
| [RemoteOK](https://remoteok.com) | `/api` |
| [Jobicy](https://jobicy.com) | `/api/v2/remote-jobs` |

IT-only filter. Dedupe by apply URL. **Apply directly** goes to that official URL. **Auto-apply** prepares a true pack for gate-pass jobs, then you open the same URL. Provtara does not log into an ATS or press Submit.
