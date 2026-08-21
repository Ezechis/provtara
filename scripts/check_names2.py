#!/usr/bin/env python3
from __future__ import annotations

import json
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

NAMES = [
    "probitas", "honestas", "meritum", "aptum", "dignum", "verum", "honos",
    "idonea", "iustum", "merum", "fidex", "probit", "idoneum", "verova",
    "candova", "plyova", "honova", "aptova", "rolova", "fitova", "veruna",
    "canduna", "plyuna", "honuna", "verdan", "candan", "plydan", "verlon",
    "candlon", "plylon", "verwyn", "candwyn", "plywyn", "verrel", "candrel",
    "plyrel", "verden", "canden", "plyden", "candix", "plyix", "honix",
    "aptix", "verox", "candox", "plyox", "honox", "aptox", "verex", "plyex",
    "honex", "aptex", "claros", "lucen", "alumen", "avento", "solvera",
    "plyron", "plyren", "plyris", "plyora", "merora", "attora", "provora",
    "rolora", "plydex", "hondex", "aptdex", "candex", "veridex", "meridex",
    "plynova", "lumenor", "audeon", "audora", "merion", "candion", "aption",
    "plyos", "meros", "candos", "veros", "plyum", "honum", "plyon", "meron",
    "candon", "veran", "honan", "aptis", "apton", "apten", "meris", "candis",
    "veris", "honis", "clarion", "nexora", "velora", "solara", "kinora",
    "kinova", "avenir", "avenly", "avento", "idonea", "fides", "fidelis",
    "integrum", "probity", "candorly", "trueora", "plyora", "merora",
    "honora", "attesta", "provexa", "qualora", "merivo", "plyra",
    "veridex", "plytara", "plynexa", "meritvox", "bespokra", "candivox",
    "qalnova", "honovox", "adeptvox", "siftvox", "klynexa", "xorvora",
    "honorara", "provtara", "roleara", "hirelyx", "plytrue", "roletrue",
    "veritora", "candivora", "fitivox", "exactvox", "provevox", "attestvox",
    "merivox", "talyra", "zorvex", "zyvora", "nyvora", "klyra", "plyrix",
    "qualix", "fitrix", "jobrix", "rolevox", "skillvox", "truevox", "trueply",
    "vlyra", "glyra", "xorvex", "qyvora", "wyvora", "myvora", "xyvora",
    "adevora", "verivox", "orvyn", "orvyna", "plynara", "klyrix",
    "clarivo", "lucivo", "nimbla", "verityx", "integry", "helixa", "siftly",
    "provevo", "avenra", "lumerix", "veriqo", "exactum", "preciso",
    "craftra", "tailory", "pathora", "skillora", "applyra", "hirevox",
    "candidex", "attestly", "vericraft", "truecraft", "mericraft",
    "devmerit", "fitmerit", "skilltrue", "fitvora", "elvora", "zivora",
    "assaya", "truvera", "adeptix", "honorix", "credora", "fitara",
    "korvia", "vorvia", "bravix", "calyra", "nivora", "merixa", "verora",
    "candora", "qualora", "provexa", "attesta", "merivo", "plyra",
    "plyvora", "verixa", "qalora", "talvera", "merova", "credivo",
    "vettra", "honesti", "fidera", "applyora", "hireora", "skilldex",
    "meridx", "candinova", "verinova", "hononova", "adeptova", "attestora",
    "proveora", "fitora", "roleora", "skilora", "pathnova", "craftvox",
    "talnova", "clarinova", "lucinova", "nimvora", "siftnova", "exactora",
    "trueara", "oraqel", "oraqen", "plyqel", "honovox",
]

SEEN, UNIQ = set(), []
for n in NAMES:
    n = n.lower().strip()
    if n and n not in SEEN:
        SEEN.add(n)
        UNIQ.append(n)

TLDS = ["com", "io", "ai", "dev", "tech"]
RDAP = {
    "com": "https://rdap.verisign.com/com/v1/domain/{0}.com",
    "io": "https://rdap.identitydigital.services/rdap/domain/{0}.io",
    "ai": "https://rdap.identitydigital.services/rdap/domain/{0}.ai",
    "tech": "https://rdap.identitydigital.services/rdap/domain/{0}.tech",
}
DEV_URLS = [
    "https://rdap.nic.google/domain/{0}.dev",
    "https://rdap.google/domain/{0}.dev",
    "https://rdap.org/domain/{0}.dev",
]
CTX = ssl.create_default_context()


def get(url: str, timeout: float = 8.0):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 name-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b""
    except Exception as e:
        return f"ERR:{type(e).__name__}", str(e).encode()


def dns_status(domain: str) -> str:
    url = f"https://dns.google/resolve?name={domain}&type=NS"
    code, body = get(url, timeout=6)
    if isinstance(code, str):
        return code
    try:
        data = json.loads(body.decode("utf-8", "replace"))
    except Exception:
        return f"HTTP{code}"
    st = data.get("Status")
    if st == 0:
        return "TAKEN"
    if st == 3:
        return "NX"
    return f"ST{st}"


def rdap_status(name: str, tld: str) -> str:
    if tld == "dev":
        last = "ERR"
        for tmpl in DEV_URLS:
            code, _ = get(tmpl.format(name), timeout=8)
            if isinstance(code, int):
                if code == 404:
                    return "FREE"
                if code == 200:
                    return "TAKEN"
                last = f"HTTP{code}"
            else:
                last = code
        return last
    url = RDAP[tld].format(name)
    code, _ = get(url, timeout=8)
    if isinstance(code, str):
        return code
    if code == 404:
        return "FREE"
    if code == 200:
        return "TAKEN"
    return f"HTTP{code}"


def main() -> int:
    print(f"Checking {len(UNIQ)} names x {len(TLDS)} TLDs via DNS...", flush=True)
    dns = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(dns_status, f"{n}.{t}"): (n, t) for n in UNIQ for t in TLDS}
        for fut in as_completed(futs):
            n, t = futs[fut]
            try:
                dns[(n, t)] = fut.result()
            except Exception as e:
                dns[(n, t)] = f"ERR:{type(e).__name__}"

    com_nx = [n for n in UNIQ if dns.get((n, "com")) == "NX"]
    all5 = [n for n in com_nx if all(dns.get((n, t)) == "NX" for t in TLDS)]
    print(f".com NX: {len(com_nx)} | all-5 NX: {len(all5)}", flush=True)

    # Prefer all-5 NX, but RDAP all .com NX of reasonable length/quality
    targets_names = all5
    print("RDAP confirming all-5 NX names...", flush=True)
    rdap = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(rdap_status, n, t): (n, t) for n in targets_names for t in TLDS}
        for fut in as_completed(futs):
            n, t = futs[fut]
            try:
                rdap[(n, t)] = fut.result()
            except Exception as e:
                rdap[(n, t)] = f"ERR:{type(e).__name__}"

    print("\n==== RESULTS (all 5 DNS NX) ====", flush=True)
    winners = []
    almost = []
    for n in targets_names:
        flags = []
        ok = True
        for t in TLDS:
            d = dns.get((n, t))
            r = rdap.get((n, t))
            flags.append(f"{t}:{r}")
            if r not in ("FREE",):
                ok = False
        line = f"{n:12} " + " ".join(flags)
        if ok:
            winners.append(n)
            print("WIN " + line, flush=True)
        else:
            almost.append(n)
            print("mix " + line, flush=True)

    print("\nWINNERS:", ", ".join(winners) if winners else "(none)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
