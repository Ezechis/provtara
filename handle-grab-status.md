# Handle grab — 20 August 2026

You asked to grab GitHub org, X, Instagram, LinkedIn company, and Product Hunt **before buying domains**. This is what actually happened.

Logged-in Chrome (OpenCLI) at the time:

| Site | Session |
|---|---|
| GitHub | **Ezechis** (id 192227605) — CLI and Chrome agree |
| Instagram | **kentematics** (personal). Do not rename. |
| LinkedIn | **Ezechinyere (Ezechi) Nnabugwu Kingsley** |
| X | `whoami` → AUTH_REQUIRED (can be a false negative; no create-account command anyway) |

## GitHub

API **cannot** create organizations (site-admin only). `gh org` has `list` only.

Used your logged-in Chrome: opened https://github.com/account/organizations/new?plan=free, filled **Plytara**, contact Gmail from public commits, accepted terms. Submit blocked by **DataDome** / “You can’t perform that action at this time.”

**Org was not created.** You still have to click **Next** in that tab (or reopen the URL as Ezechis).

Do **not** try to create org `provevox` — that user login exists.

Creating five extra GitHub **users** would violate GitHub’s one-person-one-free-account rule. Path is **organizations under Ezechis**.

## X / Instagram / LinkedIn / Product Hunt

No tool on this machine can finish signup. Each new X/IG account wants a **phone OTP**. Agent Reach is read-only (no posts, no account creation). OpenCLI has no “create company” / “create Instagram user” command.

I will not:

- Invent emails or sockpuppet accounts
- Rename `@kentematics`
- Open five LinkedIn company pages with no website
- File a Product Hunt product with no URL

Instagram profile 404s suggest **plytara** (and several sisters) are still claimable from “Add account” while you can receive the code.

## After you click GitHub Next

Ask the agent to verify:

```
gh api user/orgs
gh api users/plytara
```

Expect `login: plytara`, `type: Organization`, and you as owner.
