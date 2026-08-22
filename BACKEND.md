# How Provtara should generate a CV (plain language)

Read this top to bottom. Each numbered block is one machine. The next block is not allowed to start until the previous one has finished.

The one rule that never changes: **the computer may only write what the candidate has already proven.** If Kubernetes is not in the confirmed résumé, it must not appear on the tailored CV. The language model is not the author. It is a copy editor that can be thrown away.

---

## What exists today vs what we add later

Today, after you upload a résumé, Provtara already:

- reads the file
- guesses skills
- asks you to confirm
- checks a job against those skills
- writes a pack (résumé + cover letter) from that evidence
- stops before Submit

Later we add one extra step in the middle of that: an LLM that **rewrites the same facts in better prose**. If the rewrite sneaks in a new skill, we discard it and keep the old pack.

Web3 jobs and Web3 templates are already on the site. They use the same pipeline. They do not get a special “make me sound crypto” model.

---

## Step 1 — Read the résumé (Parser)

**Input:** a PDF, Word file, or pasted text.

**What it does:** pulls the raw words off the page. Name, dates, job titles, bullets. It does not decide if those words are true. It does not talk to an LLM.

**Output:** a blob of text. “Chioma was a backend engineer at Paystack. She wrote Python services…”

**If this fails:** we ask the candidate to paste the text instead.

This is the existing upload screen: **Upload Your Resume**.

---

## Step 2 — Guess a profile (Proposer)

**Input:** the blob from Step 1.

**What it does:** walks through the text and lists:

- name, email, location
- skills it saw (Python, Docker, Solidity…)
- jobs and the bullets under them

It is a guess. A PDF that says “familiar with Kubernetes” will often get Kubernetes on this list even if the person never ran a cluster. That is why Step 3 exists.

**Output:** a **draft profile**. Not live. Not used for a job yet.

**No LLM here.** Guessing from keywords is cheaper and easier to audit. An LLM at this step is how fake skills get invented.

---

## Step 3 — The human says what is true (Confirm)

**Input:** the draft from Step 2.

**What it does:** shows the candidate every skill and every bullet. They keep, edit, or strike. A skill with no bullet underneath gets struck automatically.

Until they click confirm, Provtara has **no profile**. Auto-apply must refuse to run.

**Output:** a **confirmed profile**. This is the only source of truth for everything after.

This is the existing Confirm screen (it is not on the left rail on purpose — it is a step after upload, not a place to browse).

If you only remember one thing: **Steps 1 and 2 are the machine proposing. Step 3 is the person signing it.**

---

## Step 4 — Can this person actually do this job? (Gate)

**Input:** confirmed profile + one job listing.

**What it does:** for each must-have on the job (example: Solidity, PostgreSQL, Kubernetes), it looks for a matching skill **and** a bullet that uses it.

- All must-haves evidenced → the job **passes**. We may prepare a pack.
- Any must-have missing → the job **fails**. We may still show it as a long shot. We do **not** write a tailored CV that pretends the gap is filled.

**Output:** pass or fail, plus a gap table (met / not met).

No LLM. A yes/no checklist is the product.

---

## Step 5 — Write the pack without a model (Deterministic writer)

**Input:** confirmed profile + a job that passed.

**What it does:** stitches a résumé and a cover letter using only:

- the candidate’s confirmed bullets
- the job title and company
- the must-haves that were evidenced

It will put the matching bullets near the top. It will not add a year, a tool, or a team size that was not in the profile.

**Output:** Pack A. This pack is always kept, even if a later rewrite happens.

This is what Auto-apply already prepares today.

---

## Step 6 — Optional polish (LLM stylist)

**Input:** Pack A + the confirmed profile + the job. Nothing else.

**What we tell the model, in one sentence:**  
“Rewrite these sentences so they read well for this job. You may reorder. You may not add a tool, employer, date, degree, or achievement that is not in the input.”

**Which model:** SpaceXAI, model **grok-4.6**, called from the **server** with `XAI_API_KEY`. Never from the phone browser. One vendor. If that key is missing, skip this step and show Pack A.

**Output:** Pack B (a draft). Not shown to the candidate yet.

---

## Step 7 — Catch lies (Truth firewall)

**Input:** Pack B.

**What it does:** scans every word against the confirmed profile and against a closed list of dangerous tokens (Kubernetes, Solidity, TensorFlow, and so on). If Pack B contains a token the profile does not have, Pack B is **deleted**.

Two tries. If both fail, the candidate sees Pack A and a note: “The rewrite was discarded because it added something you did not evidence.”

**Output:** either Pack B (clean) or Pack A (fallback). Call this the **final pack**.

This firewall already exists in code (`truth.py`). The LLM is not allowed to bypass it.

---

## Step 8 — Show it, then the human submits (Presenter)

On screen, in this order:

1. The **worked example** for that title (the measurement stick — already on the right-hand templates).
2. **Your final pack** (résumé + letter).
3. The **gap table**.
4. Download buttons.
5. A button that opens the **employer’s official apply URL**.

Provtara never logs into the ATS. Provtara never clicks Submit.

---

## How the pieces sit on a server

```
Phone / browser
    |
    |  HTTPS
    v
Flask (Provtara on Render)
    |
    +-- SQLite: users, confirmed profiles, packs, job listings
    +-- Parser, proposer, gate, writer, firewall  (no paid API)
    +-- Optional: grok-4.6 via https://api.x.ai/v1
```

For the workshop, one web process is enough. A background worker is only needed later if a rewrite takes more than about 15 seconds and the page feels stuck.

Every pack we store should remember:

- which profile version was used
- which job
- Pack A text
- Pack B text (if any)
- whether the firewall passed

That is how we debug “the CV invented Terraform” without guessing.

---

## Web3 does not get a different brain

Web3 jobs go through the same eight steps.

The only extras:

- extra title templates (Smart Contract, Solidity, Protocol, …) — already added
- extra tokens in the firewall (Solidity, Ethereum, Foundry, Hardhat, EVM) — already added
- later, optional proof: a transaction hash or GitHub repo the candidate pastes, which we fetch, and only then may “Solidity” stay on the pack

A “make it sound Web3” prompt with no evidence is how people get hired into jobs they cannot do. We will not build that.

---

## What the candidate sees, in order

1. Upload Your Resume  
2. Confirm (strike anything untrue)  
3. Pick a job (Nigeria, Web3, remote, …)  
4. If the gate passes: see your pack next to the worked example  
5. Download  
6. Open the official listing and submit yourself  

If the gate fails: see the gap. No fake CV.

---

## What we should not do

- Do not generate a CV from the job description alone.
- Do not call OpenAI / Anthropic / Gemini as a second brain unless SpaceXAI is actually down.
- Do not put the API key in the frontend.
- Do not let Step 6 run if Step 3 or Step 4 has not passed.
- Do not use the LLM to invent the 80 title templates. Those stay hand-written examples plus a fill-in form.

---

## Build order when we code this

1. Keep Steps 1–5 and 7 as they are (already shipping).  
2. Add Step 6 behind a flag: `XAI_API_KEY` present → try rewrite; absent → Pack A only.  
3. Wire Step 8 so the screen shows example / your pack / gaps.  
4. Only then: Web3 proof-of-work (tx hash, repo).  

Nothing in that list requires a new database product or a new host.
