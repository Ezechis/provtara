# Domain availability

Checked 20 August 2026.

Method:

1. DNS via `https://dns.google/resolve?name=NAME.TLD&type=NS` — `Status 3` = NXDOMAIN
2. Registry RDAP — HTTP 404 = not in registry (treated as free)
   - `.com` → `https://rdap.verisign.com/com/v1/domain/{name}.com`
   - `.io` / `.ai` / `.tech` → Identity Digital RDAP
   - `.dev` → `https://pubapi.registry.google/rdap/domain/{name}.dev`

**RDAP 404 means unregistered, not “free as in $0.”** Some `.ai` / `.io` / `.dev` names are unregistered but premium-priced. Confirm in a registrar cart before paying.

Re-run `scripts/check_names2.py` before buying. These can be taken overnight.

## Finalists — all five TLDs registry-free (404)

| Name | .com | .io | .ai | .dev | .tech |
|---|---|---|---|---|---|
| plytara | FREE | FREE | FREE | FREE | FREE |
| meritvox | FREE | FREE | FREE | FREE | FREE |
| bespokra | FREE | FREE | FREE | FREE | FREE |
| provevox | FREE | FREE | FREE | FREE | FREE |
| provtara | FREE | FREE | FREE | FREE | FREE |
| plynexa (runner-up) | FREE | FREE | FREE | FREE | FREE |

`.dev` for some earlier rows first came back HTTP 429 (Google rate limit) with DNS NXDOMAIN; a later direct check to `pubapi.registry.google` returned **404** for all six.

## Also registry-free on all five (not recommended as the brand)

canduna, plyuna, honuna, plydan, plylon, candwyn, plywyn, plyrel, provevox, attestvox, candinova, adeptova, oraqen, plyqel, qalnova, honovox, adeptvox, siftvox, klynexa, xorvora, honorara, provtara, roleara, hirelyx, plytrue, roletrue, candivora, fitivox, exactvox, …

Rejected for sound, spelling, collisions, or being slogan-like. See `collisions.md`.

## Taken at `.com` (examples — do not reuse)

Plyra, Merivo, Candora, Attesta, Provexa, Verora, Qualora, Skillora, Hirevox, Pathora, Truecraft, Veritora (DNS NX but RDAP TAKEN), and most 5–6 letter pretty coinages.

## When you buy

Same registrar cart, same day, all five:

`NAME.com` `NAME.io` `NAME.ai` `NAME.dev` `NAME.tech`

Lead with `.com` in speech. Use `.dev` or `.ai` in product UI if it fits.
