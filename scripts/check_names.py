#!/usr/bin/env python3
"""DNS-first then RDAP domain availability probe."""
from __future__ import annotations

import json
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

NAMES = [
    "plyra", "merivo", "candora", "attesta", "provexa", "verora", "qualora",
    "bravix", "calyra", "nivora", "merixa", "honorix", "credora", "fitara",
    "korvia", "vorvia", "adeptix", "truvera", "assaya", "elvora", "zivora",
    "verixa", "plyvora", "exactum", "qalora", "talvera", "merova", "credivo",
    "vettra", "honesti", "fidera", "clarivo", "lucivo", "nimbla", "verityx",
    "integry", "helixa", "siftly", "provevo", "fitvora", "avenra", "lumerix",
    "veriqo", "skillora", "hirevox", "applyra", "mericraft", "meritvox",
    "candidex", "attestly", "vericraft", "truecraft", "roletrue", "pathora",
    "craftra", "tailory", "bespokra", "devmerit", "fitmerit", "skilltrue",
    "merivox", "plyrix", "klyra", "nyvora", "zyvora", "zorvex", "talyra",
    "rolevox", "skillvox", "trueply", "truevox", "merivon", "qualix", "fitrix",
    "jobrix", "hirelyx", "glyra", "vlyra", "xorvex", "qyvora", "wyvora",
    "myvora", "xyvora", "plytrue", "roleora", "skilora", "adevora", "verivox",
    "candivox", "fitvox", "merivon", "talvora", "plyvora", "honoraq",
    "attestix", "clarora", "lucora", "nimvora", "siftora", "proveix",
    "fitcraft", "rolecraft", "skillfit", "truefit", "meritfit", "applyfit",
    "hirefit", "jobfit", "voxmerit", "voxhire", "oraqel", "oraqen",
    "plyora", "merora", "candoraq", "veroraq", "qalvora", "klyvora",
    "zyvora", "xorvora", "plyvex", "merivex", "adeptor", "adeptora",
    "honora", "honorly", "candidly", "candorly", "trueora", "fitora",
    "roleora", "skillora", "hireora", "applyora", "pathora", "craftora",
    "bespora", "talora", "qualora", "attestora", "proveora", "meritora",
    "veritora", "lucivox", "clarivox", "nimblix", "siftvox", "exactora",
    "plynexa", "merinova", "candivora", "verivora", "qalivox", "talivox",
    "fitivox", "roleivox", "skilivox", "hireivox", "plynova", "merinova",
    "honovox", "adeptvox", "attestvox", "provevox", "clarinova", "lucinova",
    "nimvora", "siftnova", "exactvox", "pathnova", "craftvox", "talnova",
    "qalnova", "klynexa", "zynexa", "xorvona", "plytara", "meritara",
    "candidara", "veritara", "qualitara", "adeptara", "honorara", "attestara",
    "provtara", "fitara", "roleara", "skillara", "hireara", "applyara",
    "pathara", "craftara", "bespara", "talara", "clarara", "lucara",
    "nimvara", "siftara", "exactara", "trueara", "oraqel", "plyqel",
    "meriqel", "veriqel", "candiqel", "adeptqel", "honorqel", "attestqel",
    "proveqel", "fitqel", "roleqel", "skillqel", "hireqel", "applyqel",
    "pathqel", "craftqel", "talqel", "qualqel", "clarqel", "lucqel",
    "nimqel", "siftqel", "exactqel", "trueqel", "orvyn", "orvyna",
    "klyrix", "plynara", "merinara", "verinara", "candinara", "adeptnara",
    "honornara", "attestnara", "provenara", "fitnara", "rolenara",
    "skillnara", "hirenara", "applynara", "pathnara", "craftnara",
    "talnara", "qualnara", "clarnara", "lucnara", "nimnara", "siftnara",
    "exactnara", "truenara",
]

# Dedup while preserving order
SEEN = set()
UNIQ = []
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
    "dev": "https://rdap.nic.google/domain/{0}.dev",
    "tech": "https://rdap.identitydigital.services/rdap/domain/{0}.tech",
}

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
        futs = {
            ex.submit(dns_status, f"{n}.{t}"): (n, t)
            for n in UNIQ
            for t in TLDS
        }
        for fut in as_completed(futs):
            n, t = futs[fut]
            try:
                dns[(n, t)] = fut.result()
            except Exception as e:
                dns[(n, t)] = f"ERR:{type(e).__name__}"

    # Names whose .com is NX (candidate available)
    com_nx = [n for n in UNIQ if dns.get((n, "com")) == "NX"]
    print(f".com NXDOMAIN candidates: {len(com_nx)}", flush=True)
    for n in com_nx:
        row = {t: dns.get((n, t)) for t in TLDS}
        print(f"  DNS {n}: {row}", flush=True)

    # RDAP-confirm .com NX names for all 5 TLDs (DNS NX only is not enough)
    print("RDAP confirming .com-NX names...", flush=True)
    rdap = {}
    targets = [(n, t) for n in com_nx for t in TLDS]
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(rdap_status, n, t): (n, t) for n, t in targets}
        for fut in as_completed(futs):
            n, t = futs[fut]
            try:
                rdap[(n, t)] = fut.result()
            except Exception as e:
                rdap[(n, t)] = f"ERR:{type(e).__name__}"

    print("\n==== FULL-STACK (all 5 TLDs DNS NX + RDAP FREE/NX) ====", flush=True)
    winners = []
    for n in com_nx:
        flags = []
        ok = True
        for t in TLDS:
            d = dns.get((n, t))
            r = rdap.get((n, t))
            flags.append(f"{t}:{d}/{r}")
            if d != "NX" or r not in ("FREE", "HTTP404"):
                ok = False
        line = f"{n}  " + " ".join(flags)
        if ok:
            winners.append(n)
            print("WIN " + line, flush=True)
        else:
            print("mix " + line, flush=True)

    print("\nWINNERS:", ", ".join(winners) if winners else "(none)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
