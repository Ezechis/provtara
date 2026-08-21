# How this platform works — build plan

**Date:** 20 August 2026  
**Status:** Phase 0 CLI and Phase 1 web workshop exist. No payments, no employer accounts, no Submit.  
**Folder:** `C:\Users\Ezeking\Grok\Job_Portal`  
**Working brand:** **Provtara** (locked — see `BRAND.md`)

This is the plan for an **IT-only job board plus honest application workshop**. It is not a spray-and-pray auto-apply bot. It is not a résumé mill that invents keywords.

You already run a personal version of the hard part as the `job-apply` skill: master profile, gap table, truth checker that **refuses to write a file that lies**, cover letter, stop at Submit. This plan is how that becomes a product other people can use.

---

## 1. One sentence

A candidate gives the platform a true résumé. The platform shows IT jobs they are actually qualified for, rewrites **that** résumé and a matching cover letter for a job they pick, and hands the pack back so **they** submit.

## 2. Non-negotiables

These are architecture, not marketing.

1. **Resume first.** No job matching, no tailoring, no letter until a résumé has been ingested into a structured **evidence profile**.
2. **IT jobs only.** Non-IT postings are rejected at ingest. A “marketing manager who uses Excel” is not an IT job.
3. **Qualification gate.** Tailoring runs only for jobs the candidate is **eminently qualified** for (defined in §11). Other jobs may be visible; they do not get a fake-fit pack.
4. **Never manufacture skills.** No tool, language, year, metric, employer, degree, or clearance may appear in output unless it is in the evidence profile. If the posting wants Kubernetes and the profile has none, that is a **gap**, not a bullet.
5. **Hand off. Never submit.** The product stops at download (and optional “open the employer’s apply URL”). The human clicks Submit. No passwords, no CAPTCHAs, no account creation on the employer’s site.
6. **Fix the claim, never the checker.** Generated text that fails the truth firewall is regenerated or blocked. Nobody “softens” a failed check to ship the file.
7. **Show the gap before the pretty PDF.** The candidate sees requirement vs evidence **before** a tailored résumé exists.

## 3. Who it is for

**Candidates:** software, data, infrastructure, security, IT operations, and adjacent technical roles. Especially people tired of AI tools that make them sound like someone they are not — and then fail the interview.

**Employers (phase 2):** companies that want IT applicants whose paperwork matches what they can actually discuss in a screen.

**Not for:** mass auto-apply, visa fraud, “make me a senior in 20 minutes,” non-IT career coaching, or filling every ATS keyword regardless of truth.

## 4. What we are not building in v1

Leave these out until the honest loop works.

- Auto-apply, form filling, CAPTCHA solving
- LinkedIn scraping that logs in as the candidate
- Interview coaching, salary negotiation bots
- Non-IT categories
- A social network or “candidate community”
- Recruiter CRM / ATS replacement for employers (a simple job post is enough)
- Mobile-native apps (responsive web is enough)
- Fine-tuning a custom LLM (prompt + structured profile + checker is the product)

## 5. Three ways to build it

| | Approach | Pros | Cons |
|---|---|---|---|
| **A (recommended)** | Candidate workshop first, then the board | Ships the differentiator in weeks; job listings can start as a curated feed; matches “hand them the pack” | Not a full marketplace on day one |
| B | Full two-sided marketplace from day one | Looks like “the product” | You will spend a year on employer sales before the honesty engine is trusted |
| C | Overlay only (no hosted jobs; paste a URL like Jobscan) | Fastest | You asked to **advertise** IT jobs. Overlay can be a **feature**, not the whole product |

**Recommendation: A.** Phase 1 is resume → evidence profile → qualified IT jobs → tailored pack → download. Phase 2 is employers posting on the same site. Phase 3 is optional “open apply URL with files ready” (still no Submit).

That sequence is how Teal/Jobscan grew, except those products optimize for ATS score. This one optimizes for **true fit**.

---

## 6. Candidate loop (the product)

```
Upload résumé
    → Parse to Evidence Profile (human confirms)
        → See only IT jobs that pass the qualification gate
            → Pick one job
                → Gap table (shown first)
                    → Tailored résumé (facts from profile only)
                    → Cover letter (facts from profile only)
                        → Truth firewall (must pass)
                            → Download pack
                                → Candidate submits elsewhere
```

### Screens (v1)

1. **Landing** — one promise: *IT jobs. Your real skills. Nothing invented.*
2. **Sign up** — email. No “apply as guest” that leaves an orphaned résumé sitting in object storage without an owner.
3. **Upload** — PDF / DOCX / pasted text. One current résumé. Replaces the previous file; history of **generated packs** is kept, history of **raw uploads** is versioned.
4. **Confirm profile** — the system’s reading of skills, roles, dates, tools, education. Candidate can add, edit, or strike. **Struck items never appear in output.** This screen is the last chance to stop a parser hallucination from becoming a “skill.”
5. **Jobs** — IT roles the gate says they can honestly do. Each card: title, company, location/remote, stack overlap (from **their** profile), “3 gaps” if any soft gaps remain.
6. **Job detail** — full posting, overlap, hard misses. Primary button: **Prepare application** (only if gate passed). Secondary: **Not a fit — hide.**
7. **Gap table** — requirement | evidence | met / not met. Continue or back out.
8. **Preview** — résumé + letter, side by side, with a “source” chip on every bullet (which profile item it came from).
9. **Pack** — download `.docx` + `.pdf`, copy apply URL, checklist (“do not add skills on the employer form that are not in this pack”).

No “one-click apply.” No “we submitted 40 jobs for you.”

## 7. Employer loop (phase 2)

1. Company account, verified email domain preferred.
2. Post an IT job: title, description, must-haves, nice-to-haves, location, work auth, stack.
3. Listing is classified IT or rejected.
4. Employer sees **counts**, not a spam inbox: how many candidates on the platform pass the gate for this job. Optional later: candidate can **release** their pack to the employer. Default is off — this is not a résumé database sold to recruiters.

v1 can advertise jobs **without** employer accounts by ingesting public IT listings (with source attribution and a link back to apply on the original board). That is “advertises IT jobs” without a sales team.

---

## 8. The truth engine (the actual product)

Everything else is a website. This is why someone would pay.

### 8.1 Evidence profile (canonical)

After parse + human confirm, store a structured profile. Not the raw PDF as the source of truth — the **confirmed profile** is.

Minimum fields:

- Identity (name, email, location, work authorization — candidate-provided)
- Experience entries: employer, title, start, end, bullets
- Each bullet: text, `source_span` (where in the original résumé), `tags` (skills it actually evidences)
- Skills: only those grounded in at least one bullet, project, or education row
- Projects: name, what shipped, stack used
- Education and certs: name, year, issuer
- Explicit **banned additions**: candidate can mark “I do not have X” so the model cannot “helpfully” add it

**Parser output is a proposal.** It is not live until the candidate confirms. If the parser reads “TensorFlow” from a course title they never used, they strike it here.

### 8.2 Job record

Normalized from a posting:

- must-haves, nice-to-haves, ATS keywords
- years required (as stated, never inflated)
- stack, seniority, work model, location, authorization
- raw description (kept for the letter’s hook)
- source URL

### 8.3 Gap analysis (always first)

```
| Requirement        | Evidence                         | Verdict   |
|--------------------|----------------------------------|-----------|
| 3+ years Python    | Role 2 bullets 0,2,6             | met       |
| Kubernetes         | —                                | not met   |
| Production RAG     | Project SynthForge               | met       |
```

Verdicts are only `met` or `not met`. No “partially” that becomes a fake bullet. Soft related evidence can live in a **notes** column (“Docker in production, not K8s”) without flipping the verdict.

### 8.4 Selection, not invention

Tailoring **selects, reorders, and rewords** bullets that already exist.

Allowed: phrasing, emphasis, posting vocabulary **when it names something they did**.

Forbidden: a technology, metric, scale, year, or employer not in the profile. Bolting an ATS keyword onto a bullet it does not describe.

This is the same rule as `job-apply` `references/tailoring.md`. On a multi-tenant product it is enforced in code, not in a prompt that a model can ignore.

### 8.5 Firewall (must not be optional)

Two layers, both required to emit a file:

**Layer A — structural.** Every sentence in the résumé and letter is aligned to profile item IDs. A sentence with no ID is dropped. A sentence whose entities are not in those items is dropped.

**Layer B — checker.** A deterministic `truth_check` over the finished text:

- skill tokens not in the profile skill list → fail
- date ranges outside profile → fail
- company names not in profile → fail
- numeric claims not in profile → fail
- per-tenant **banned claims** (optional extra: “never write ‘fine-tuning’ for this person”) → fail

On fail: do not download. Show the line. Regenerate or strip. **Never edit the checker to let a lie through.**

You already have this pattern in `job-apply` (`truth_check.py` + `render_resume.py` refuses to write). Generalize it from one user’s banned list to **each tenant’s evidence profile**.

### 8.6 The model’s job (narrow)

The LLM does **not** “write a résumé from the job description.”

It receives:

- the confirmed profile (or the selected subset)
- the job must-haves and keywords
- the gap table
- hard instructions: only these facts

It returns:

- rewritten bullets with `source_id` on each
- a letter whose evidence paragraphs cite `source_id`s
- a hook that refers to something **in the posting**, not flattery

Then Layer A + Layer B run. The model is a phrasing engine inside a cage.

**Default LLM:** SpaceXAI / xAI (`XAI_API_KEY`, `https://api.x.ai/v1`, OpenAI-compatible). Server-side only. Never in the browser. Confirm current model names on [docs.x.ai](https://docs.x.ai) at implementation time.

---

## 9. Résumé intake (what it takes)

| Step | What happens | Failure mode |
|---|---|---|
| Upload | Store original in object storage; virus scan | Reject executable disguised as PDF |
| Extract | Text + basic layout from PDF/DOCX | Scanned PDF → ask for DOCX or paste |
| Structure | LLM **proposes** roles, dates, skills, bullets with quotes from source | Hallucinated skill → must be confirmable against source_span |
| Ground | Drop any proposed skill that cannot be quoted from the file | Parser enthusiasm |
| Confirm | Candidate edits | Skip-confirm is not allowed on first upload |
| Freeze | Profile version N is the parent of all packs until they upload again | Silent profile drift |

Formats: PDF, DOCX. No “we’ll screenshot your LinkedIn.” LinkedIn is not a source of truth.

Optional later: “add a bullet” with a required **source note** (repo URL, employer, year). Still goes through confirm + firewall.

## 10. Advertising IT jobs

Two ingest pipes. Same job record at the end.

### Pipe 1 — public listings (v1)

Pull IT roles from boards you are allowed to use (official APIs first: Adzuna, The Muse, Greenhouse job boards, company career pages, RSS). Store title, company, location, description, apply URL, retrieved-at.

**IT classifier:** title + description must match a closed list of role families (software engineering, data, ML/AI engineering, SRE/DevOps, security, IT ops, QA, product engineering, etc.). Reject “IT sales,” “IT recruiter,” “Excel analyst” unless the posting is clearly a technical IC/manager role.

**Dedup** by apply URL + company + title.

Always keep **apply on original site**. You are a shop window and a workshop, not a dark ATS.

### Pipe 2 — employers post (phase 2)

Form: title, description, must-haves, stack, location, auth, compensation if they will share it. Same classifier. Same job record. Apply URL can be “email us” or an external ATS.

### What “advertises” means in v1

A public `/jobs` index, SEO pages per job, filters (remote, stack, seniority). Logged-out users can browse. **Prepare application** requires an account and a confirmed profile.

## 11. Qualification gate (“eminently qualified”)

This is the product’s spine. Define it in code, show it to the user, do not hide it in a similarity score.

A job **passes** the gate when **all** of the following hold:

1. **Must-have coverage.** Every item the posting marks as required (or that the parser marked `must_have`) is `met` in the gap table, **or** the candidate has explicitly accepted a listed exception (see below).
2. **Seniority band.** Junior / mid / senior inferred from years **as stated in the profile**, never padded. A 2023 start does not pass a “5+ years professional” must-have.
3. **Authorization.** If the posting requires a right-to-work the profile does not have, fail. Do not invent “no sponsorship needed.”
4. **Location / remote.** On-site-only in another country with no remote flag → fail unless the profile says they will relocate.
5. **Stack core.** At least one of the posting’s primary languages/platforms is in the profile (e.g. a Java shop with zero Java in the profile fails even if they have “programming”).

**Exceptions (opt-in, visible):** the candidate may still prepare a pack if they check “I know I do not meet X; write the honest gap into the letter; do not add X to the résumé.” The résumé still cannot contain X. The letter’s bridge paragraph must name the gap. This is for near-misses they want to try anyway — not a back door to fiction.

**Default:** jobs that fail the gate are filtered **out** of “Prepare for me.” They can sit in a separate “Long shots” list with the miss explained, no tailor button until the exception is checked.

“Eminently qualified” is **not** “ATS 90%.” A keyword score that ignores missing Kubernetes is how the rest of the market lies. Do not ship a match percentage as the gate.

## 12. Tailoring the résumé

For a gate-passed job:

1. Score each profile bullet against must-haves, keywords, nice-to-haves (same spirit as job-apply: +2 / +1 / +1).
2. Take the highest-scoring 4–6 bullets per relevant role. Drop irrelevant roles or shrink them; do not delete true history to look like a different person (dates stay honest).
3. Reword selected bullets to the posting’s vocabulary **only where true**.
4. Reorder skills so evidenced, job-relevant skills come first. Skills with no evidence are not listed.
5. Summary: 3–4 lines, only facts from selected bullets.
6. Render ATS-safe DOCX (single column, standard headings, no text boxes) and PDF.
7. Run firewall. If fail, do not render files.

Output artifacts per job:

```
packs/<user>/<job-id>/<timestamp>/
  gap.json
  selection.json      # bullet ids, skill order
  resume.docx
  resume.pdf
  cover_letter.md
  cover_letter.pdf
  truth_report.json   # pass/fail, line hits
```

The candidate can regenerate. Each generation is stored. They download a **specific** pack, never “whatever was last in memory.”

## 13. Cover letter

Not a template with the company name swapped.

**Structure (v1 default):**

1. **Hook** — one specific, verifiable thing from **this** posting or product. Not “I am excited to apply.”
2. **Two evidence paragraphs** — each tied to profile items, preferably with a real number if the profile has one.
3. **Bridge** — the largest remaining gap, in plain language. Do not skip because it is uncomfortable. Do not close it with a fake year.
4. **Close** — availability as the candidate entered it, matched to the posting’s hours if stated.

Length: a band you enforce (e.g. 400–700 words). Empty flattery phrases are banned in the checker (“passionate about,” “proven track record,” “leverage,” “synergy,” “great fit”).

Same firewall as the résumé. Same source IDs.

## 14. Hand-off (the last mile)

The pack page contains:

- Resume PDF + DOCX
- Letter PDF + Markdown
- Job title, company, official apply URL
- Gap table (so they do not “improve” the résumé in the employer form)
- Short instruction: *Submit these files. Do not add tools on the form that are not in this pack. We will not click Submit for you.*

**Out of scope forever unless you explicitly change the product:** pressing Submit, storing employer passwords, solving CAPTCHAs, creating accounts on Greenhouse/Lever/Workday.

That is also a legal and trust feature. Auto-apply tools get candidates banned. This product’s reputation is the opposite.

Optional phase 3: browser **opens** the apply URL and lists the files to attach. Still stops short of Submit.

## 15. Data model (logical)

**User** — auth, email, plan.

**EvidenceProfile** — versioned; `confirmed_at`; JSON of roles/bullets/skills with tags and source spans.

**SourceResume** — original file pointer, hash, parse log.

**Job** — normalized posting, source, apply URL, IT classification, must-haves.

**QualificationResult** — per (profile_version, job): pass/fail, gap table, exception flags.

**Pack** — selection, generated files, truth report, status (`previewed` | `downloaded`).

**Employer** / **JobPost** (phase 2).

No selling of résumés. Retention: originals and packs stay until the user deletes them. Deleted profile → generated packs that depended on it are tombstoned.

## 16. System shape

```
[Browser]  →  [Web app]
                 ├─ Auth
                 ├─ Jobs API (browse, ingest worker)
                 ├─ Profile API (upload, confirm)
                 ├─ Qualify API
                 └─ Pack API
                        │
                        ▼
              [Worker queue]
                 ├─ parse résumé
                 ├─ classify job (IT?)
                 ├─ gap + gate
                 ├─ generate (LLM, server-side)
                 ├─ truth_check
                 └─ render docx/pdf
                        │
                        ▼
              [Postgres]   [Object storage]   [LLM: api.x.ai]
```

Keep generation **asynchronous**. A pack is a job in a queue. The UI polls until preview is ready. Do not generate in the HTTP request.

## 17. Tech (v1, boring on purpose)

| Layer | Choice | Why |
|---|---|---|
| Web | Next.js (or similar) on a boring host | SEO for job pages; one repo |
| API / workers | Python (you already have parse/render/truth scripts) | Reuse `job-apply` ideas; PDF/DOCX ecosystem |
| DB | Postgres | Profiles, jobs, packs, JSONB for gap tables |
| Files | S3-compatible (Cloudflare R2 is cheap) | Originals + generated PDFs |
| Queue | One worker process + Postgres-backed jobs at first | Avoid Redis until you have load |
| LLM | SpaceXAI / xAI via OpenAI-compatible client, key only on server | Default for AI features on this machine |
| Docs | python-docx + a constrained HTML-to-PDF or Word COM on a Windows worker if you stay on this PC | ATS-safe, not Canva |
| Auth | Email magic link or OAuth (GitHub is natural for IT) | IT candidates already have GitHub |

Do not start with Kubernetes. One VPS or a small PaaS runs v1.

## 18. What to reuse from job-apply

You are not starting from zero. Lift **ideas and tests**, not Ezeking’s personal `master_profile.yaml`, into the product.

| Existing | Product equivalent |
|---|---|
| `master_profile.yaml` | Per-user EvidenceProfile |
| `truth_rules.md` + `truth_check.py` | Per-pack checker against **that user’s** skills/dates/companies |
| `tailoring.md` scoring | Qualification + selection |
| `gap_analysis.md` | Gap table UI, shown before generate |
| `letter_check.py` | Length + banned-phrase checks |
| `render_resume.py` refuses to write on fail | Pack API returns 409 + report, no files |
| Never Submit | Pack download only |
| Banned claims (fine-tuning, FastAPI, …) | Become **this user’s** bans if absent from **their** profile — not global |

Do **not** ship Ezeking’s résumé, salary floors, or email rules as platform defaults.

## 19. Build phases

### Phase 0 — paper (this week)

- Lock the gate definition (§11) so you do not argue with the model later
- One sample profile + three sample jobs: one clear yes, one clear no, one near-miss with exception
- Run them through a **manual** gap table and a checker script (even CLI-only)

Exit: you can show a stranger a before/after pack and the gap table, and they believe the “never invent” claim.

### Phase 1 — workshop MVP (the differentiator)

Ship only:

- Auth + upload + confirm profile
- Job list from **curated ingest or even a hand-maintained set of IT jobs** (50–200 is enough)
- Gate + gap table
- Generate résumé + letter
- Firewall
- Download

No employer accounts. No payments if you are testing with friends. Invite-only.

**Success:** 20 IT candidates produce at least one pack they would actually submit. Zero cases of a skill in the PDF that was not in the confirmed profile (audit this).

### Phase 2 — real job advertising

- Ingest pipeline + IT classifier + dedup
- Public job SEO pages
- Filters, alerts (“new jobs you qualify for”)
- Employer self-serve post (optional paid)

### Phase 3 — money

Pick one, not three:

- Candidate subscription (N packs / month)
- Employer pay-to-post or pay-to-feature
- Take-rate later if you ever add applications **to you** (still not auto-submit)

Honesty is easier to charge employers for (“fewer fake seniors”) than candidates, but candidates feel the pain today. A cheap candidate plan plus featured employer listings is enough.

### Phase 4 — only if Phase 1 is loved

- “Open apply URL” helper
- Extra evidence (GitHub repo import as **proposed** bullets, still confirmed)
- Multiple résumé templates (still ATS-safe)

## 20. What it takes (honest)

These are order-of-magnitude, one technical founder who already has the personal pipeline.

| | Time | Money (bootstrap) |
|---|---|---|
| Phase 0, CLI + fixtures | 1–2 weeks | $0 plus LLM tokens |
| Phase 1 MVP (usable web) | 6–10 weeks | Hosting ~$20–50/mo; LLM tokens (budget for $50–200/mo while testing); domain when you can |
| Phase 2 ingest + SEO | +4–6 weeks | API costs if you pay a jobs API; still small |
| Phase 3 payments | +2 weeks | Stripe; accounting |

**Skills needed:** product sense on the gate, Python for parse/check/render, a web UI, Postgres, stubbornness about the firewall.

**You already have:** tailoring rules, a truth checker philosophy, cover-letter structure, “stop at Submit,” IT-job taste, brand work in this folder.

**You do not have yet:** multi-tenant profile confirm UX, job ingest, rendering that is not Ezeking-specific, payments, legal pages.

**Legal (budget time, not just money):**

- Terms: you are not the applicant; they submit; they own the content
- Privacy: résumés are sensitive; do not train public models on them; do not sell them
- Equal opportunity: the gate must use job-related evidence, not demographic proxies
- Job listing copyright: prefer APIs and employer posts; do not wholesale clone Indeed
- “AI-generated” disclosure where the law requires it — and still tell the truth that **facts** came from the candidate

## 21. How to know it is working

- **Truth:** sampled packs, zero ungrounded skills (human audit)
- **Use:** packs downloaded / confirmed profiles (not signups)
- **Fit:** % of packs whose gate passed without exception
- **Trust:** candidates who come back for a second job
- **Employer (later):** interviews reported, not “applications sent”

Vanity: ATS scores, “40 jobs applied this week.” Those are the competitors’ metrics and they fight this product’s soul.

## 22. Risks

| Risk | What to do |
|---|---|
| Parser invents a skill | Confirm screen + drop unquoted skills |
| Model invents a skill | Source IDs + checker; no file on fail |
| Gate too strict, nobody gets a pack | Exception path with mandatory gap in the letter |
| Gate too loose, honesty dies | Must-haves are binary; no “80% match” as pass |
| Job ingest is legally messy | Start curated; add APIs; employer posts |
| Auto-apply pressure from users | Refuse in copy and in code. That is the brand |
| Can’t pay for `.com` yet | Build on a subdomain or GitHub Pages for Phase 0–1; buy when you can (see `domain-availability.md`) |
| Name not locked | Product works regardless of Plytara vs Meritvox |

## 23. Decisions already made in this plan

So the document is executable, not a pile of options:

- Workshop first (Approach A), board second
- Qualification gate is binary must-haves, not an ATS percentage
- LLM is caged: phrasing only, SpaceXAI/xAI server-side
- Download only; never Submit
- Confirmed profile is source of truth, not the PDF
- IT classifier is a closed role-family list
- Reuse job-apply **rules**, not Ezeking’s personal data

## 24. Open (only these)

Change these on purpose if you disagree; otherwise keep the defaults.

1. **Brand:** Plytara vs Meritvox vs Bespokra (`2026-08-20-brand-names.md`).
2. **Exception path:** allow honest near-miss packs, or hide those jobs entirely.
3. **Who pays first:** candidates or employers.
4. **Job sources in Phase 1:** hand-curated 100 IT roles vs the first jobs API.

---

When you come back, the next engineering step is **Phase 0**: one fixture profile, three jobs, a CLI that prints a gap table and will not emit a résumé that contains a skill not in the profile. That is the product in miniature. The website is clothing.
