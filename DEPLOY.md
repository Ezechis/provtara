# Put Provtara on a phone (free)

Vercel is built for static sites and serverless Node/Next. This app is **Flask + SQLite + live job pulls** (requests that can take several seconds). Vercel’s Python functions are short-lived, have no durable disk, and would drop the vacancy database on every cold start. Same idea as Vercel — git push, HTTPS URL, test on a phone — lives on **Render free** (or Railway / Fly).

**Do not share a tunnel.** `localhost.run`, localtunnel, and Cloudflare quick tunnels die when this PC sleeps, and many phones block them.

**Share this:** https://provtara.onrender.com

Hosted on Render free (Frankfurt). Dashboard: https://dashboard.render.com/web/srv-da4ai97qj5pc73blfs6g  
Repo: https://github.com/Ezechis/provtara

First visit after 15 minutes idle can take about a minute (spin-up). Uploaded résumés live in SQLite on an ephemeral disk, so they reset when the service sleeps.

## Lasting: Render free

Already live. Push to `main` on `Ezechis/provtara` deploys automatically.

GitHub Actions (`.github/workflows/deploy-render.yml`) runs tests, then tells Render to build that commit. That is the reliable trigger: Render’s own GitHub auto-deploy flag is on, but GitHub never delivered push events to this service (every prior deploy was a manual API call). Do not turn Auto-Deploy off in the dashboard unless you also keep this workflow.

Secret required on the repo: `RENDER_API_KEY` (Render Account API key, not a short-lived CLI login). Set or rotate with:

```
gh secret set RENDER_API_KEY --repo Ezechis/provtara
```

Create a long-lived key at https://dashboard.render.com/u/settings#api-keys if the secret ever 401s.

Blueprint is `render.yaml`. `run.py` listens on `0.0.0.0` and `$PORT`.

Job listings auto-refresh every **4 hours**: a visitor hitting a stale catalog triggers a background pull, the app also loops on that interval while it is awake, and GitHub Actions (`refresh-boards.yml`) POSTs `/jobs/refresh` on `0 */4 * * *` UTC so Render still updates after the free service sleeps. Manual Refresh on Vacancies uses the same 4-hour gate.

## Job sources (no API keys)

| Board | What we pull |
|---|---|
| [Remotive](https://remotive.com) | `/api/remote-jobs?category=software-dev` |
| [Arbeitnow](https://www.arbeitnow.com) | job-board API |
| [RemoteOK](https://remoteok.com) | `/api` |
| [Jobicy](https://jobicy.com) | `/api/v2/remote-jobs` |
| [Himalayas](https://himalayas.app) | jobs API |
| [Hacker News Jobs](https://news.ycombinator.com/jobs) | `hnrss.org/jobs` |
| [Working Nomads](https://www.workingnomads.com) | `/api/exposed_jobs/` |
| [The Muse](https://www.themuse.com) | public jobs API, Software Engineering |
| [Python.org Jobs](https://www.python.org/jobs/) | RSS |
| [Fossjobs](https://www.fossjobs.net) | RSS |
| [LaraJobs](https://larajobs.com) | RSS |
| [Berlin Startup Jobs](https://berlinstartupjobs.com) | RSS |

We Work Remotely and 4dayweek.io are not sources. They sell JobCopilot auto-apply, and “Open employer form” must not dump the candidate onto another auto-apply board. Listings whose apply URL still points at weworkremotely.com, jobcopilot.com, or 4dayweek.io are dropped.

IT-only filter. Dedupe by apply URL. **Apply directly** goes to that official URL. **Auto-apply** prepares a true pack for gate-pass jobs, then you open the same URL. Provtara does not log into an ATS or press Submit.
