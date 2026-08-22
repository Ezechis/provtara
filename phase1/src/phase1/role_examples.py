"""Worked examples with role-specific signatures.

Facts are written in the shape hiring managers actually scan: named systems,
protocols, and outcomes. They are original prose, not pasted CVs. Copy a line
only if you can point at the same kind of work in your own history.
"""
from __future__ import annotations

from phase1.templates_catalog import RoleTemplate

# id -> (now_line, was_line, skills, now_bullets, was_bullets, letter_paras)
Story = tuple[str, str, str, tuple[str, ...], tuple[str, ...], tuple[str, str]]

STORIES: dict[str, Story] = {
    "network-engineer": (
        "Senior Network Engineer, MainOne (2019 – present) — Lagos",
        "Network Engineer, MTN Nigeria (2016 – 2019) — Lagos",
        "BGP, OSPF, Cisco ASR, MPLS, Wireshark, VLANs",
        (
            "Ran eBGP on Cisco ASR 9001 to two upstream ISPs; AS-path prepend and MED dropped peak utilization on the Lagos–London primary from 94% to 71% without adding a circuit.",
            "Redesigned OSPF into areas 0/10/20 across three POPs; route summarization cut LSDB size about 60% and brought link-down convergence from ~8s to under 2s.",
            "Caught a bad MED that was hairpinning inter-site traffic; proved it in Wireshark, fixed the policy, and wrote the peering runbook the NOC still opens.",
        ),
        (
            "Operated the national IP/MPLS edge: VLAN design, HSRP, and the change window for each PE router.",
            "Turned a weekly flap into a damped BGP session and a ticket template so the next person did not start from syslog.",
        ),
        (
            "You need someone who has peered with real ISPs, not lab GNS3. At MainOne I owned eBGP on the ASR 9001s that carry Lagos–London traffic, including the prepend that took the primary off 94% peak.",
            "At MTN I lived in the MPLS PE change window. If your posting wants OSPF multi-area and packet-level proof, that is the work I have already been paid to do. I will submit this pack myself.",
        ),
    ),
    "network-administrator": (
        "Network Administrator, Access Bank — Technology (2018 – present) — Lagos",
        "LAN Administrator, MainOne (2015 – 2018) — Lagos",
        "switching, DHCP, DNS, VPNs, monitoring, ticketing",
        (
            "Owned DHCP/DNS for ~4,000 endpoints: split scopes, reservations for vault printers, and the Monday morning report when a scope hit 80%.",
            "Standardized access-layer Cisco stacks (stackwise, etherchannel) so a closet swap no longer meant a two-hour outage.",
            "Site-to-site VPNs for branches: PSK rotation, interesting-traffic ACLs, and the tunnel that failed open during a power cut in Ibadan — documented, then dual-homed.",
        ),
        (
            "Imaged and patched the campus distribution layer; every change had a ticket and a rollback VLAN.",
            "First responder on after-hours “the floor is down” calls; most were DHCP exhaustion or a spanning-tree loop I could name.",
        ),
        (
            "Your listing is day-to-day LAN health, not a greenfield core redesign. That is Access Bank: scopes, stacks, and branch VPNs that have to survive a generator test.",
            "I still write the ticket so the next admin can finish the change if I am on leave. I will submit this pack myself.",
        ),
    ),
    "network-security-engineer": (
        "Network Security Engineer, Interswitch (2019 – present) — Lagos",
        "Security Analyst, First Bank of Nigeria — IT (2016 – 2019) — Lagos",
        "firewalls, IDS/IPS, VPNs, segmentation, packet capture",
        (
            "Moved card-zone traffic behind Palo Alto zones and App-ID; east-west SMB from the office VLAN to the switch fabric was denied and logged, not hoped away.",
            "Tuned IPS signatures that were paging every night on a false-positive payment poll; kept the signature, excepted the poller, and the page volume dropped without opening the zone.",
            "Packet-captured a TLS intercept failure on the partner VPN; the cert chain was the story, not “the firewall is slow.”",
        ),
        (
            "Wrote the firewall change form that required a source, dest, port, and expiry. Changes without expiry were rejected.",
            "Sat in the PCI segmentation review and walked the diagram, not a slide of “zero trust.”",
        ),
        (
            "You asked for segmentation that still lets the payment path through. At Interswitch that path has App-ID, an expiry on the rule, and a capture when TLS intercept breaks.",
            "I will not list a tool I have not used on a zone that handles real cards. I will submit this pack myself.",
        ),
    ),
    "wireless-network-engineer": (
        "Wireless Network Engineer, MainOne (2019 – present) — Lagos",
        "RF Technician, MTN Nigeria (2016 – 2019) — Lagos",
        "Wi-Fi 6, controllers, site surveys, RADIUS, spectrum analysis",
        (
            "Surveyed and cut over a 14-floor HQ to Wi-Fi 6 (Cisco 9120 + 9800 WLC); sticky-client and band-select changes stopped the 2.4 GHz pile-up on the trading floor.",
            "Ekahau heatmaps against a live Ekahau Sidekick walk: we moved 11 APs and killed a microwave-oven CCI cell on 6 that no controller chart had shown.",
            "802.1X via ISE/RADIUS for staff SSIDs; guest remains a walled portal. A cert expiry at 02:00 is in the runbook with the skip-the-WLC steps.",
        ),
        (
            "Drove site surveys for new retail branches: cable path, AP count, and the wall that was actually foil-backed.",
            "Spectrum-analyzed a warehouse that “had Wi-Fi” and was a DECT cordless farm; we changed channels, not vendors.",
        ),
        (
            "Wi-Fi jobs fail on sticky clients and hidden interferers, not on brochure Wi-Fi 6. I have the Sidekick walk and the 9800 config that made the trading floor stay on 5/6 GHz.",
            "I will submit this pack myself.",
        ),
    ),
    "noc-engineer": (
        "NOC Engineer, MainOne (2018 – present) — Lagos",
        "NOC Analyst, MTN Nigeria (2015 – 2018) — Lagos",
        "monitoring, SNMP, escalation, runbooks, incident comms",
        (
            "Watch floor for IP/MPLS and metro Ethernet: SolarWinds + syslog, 12-hour shifts, and a severity matrix that says when we wake the on-call PE engineer.",
            "Wrote the “link down but BGP still up” runbook after a silent optical degrade; the first check is light levels, not a reboot.",
            "Customer updates on a P1 go out every 30 minutes even when we have nothing new — that was a rule we earned the hard way.",
        ),
        (
            "First-line for enterprise circuits: RFO templates, MTTR clocks, and the difference between a customer CPE and our NID.",
            "Escalated without dumping the ticket; the PE engineer got the last ten syslog lines and the circuit ID.",
        ),
        (
            "A NOC job is the clock and the sentence you send the customer. I have written both at 03:00 on a Lagos metro ring.",
            "I will submit this pack myself.",
        ),
    ),
    "telecommunications-engineer": (
        "Telecommunications Engineer, MTN Nigeria (2018 – present) — Lagos",
        "Transmission Engineer, MainOne (2015 – 2018) — Lagos",
        "VoIP, SIP, PBX, MPLS, SD-WAN, circuit provisioning",
        (
            "SIP trunks from the Avaya/Session Manager core to two interconnects; 183 Session Progress and codec mismatch were the actual P1s, not “the PBX is down.”",
            "Provisioned E1/Ethernet last-mile for enterprise voice: test tone, MOS samples, and the handover form the account manager cannot skip.",
            "SD-WAN overlay for 40 branches: voice in the gold queue, guest Wi-Fi in bronze, and a circuit that was “up” on ICMP and unusable for G.711.",
        ),
        (
            "Lit metro fiber laterals and documented the splice cassettes so the next cutover did not guess the color code.",
            "Handed circuits to the IP team with a completed OTDR trace, not a verbal “it’s clean.”",
        ),
        (
            "Telecom work is the SIP trace and the MOS score, not a slide about unified comms. That is the MTN interconnect I still own.",
            "I will submit this pack myself.",
        ),
    ),
    "systems-administrator": (
        "Systems Administrator, GTBank — Technology (2018 – present) — Lagos",
        "Sysadmin, SystemSpecs (2015 – 2018) — Lagos",
        "Linux, Windows Server, Active Directory, backups, patching, DNS",
        (
            "AD + DNS + DHCP for the head-office forest: GPOs that actually applied, and the one that broke printers in Victoria Island until I scoped it.",
            "Linux (RHEL) for internal tools: patch Tuesday via Satellite, LVM growth without a surprise reboot, and the restore test we run before anyone believes backup.",
            "Veeam backup of the tier-1 VMs; I have restored a finance VM to an isolated network and handed it to the app owner, not just watched jobs go green.",
        ),
        (
            "Kept Remita-adjacent Windows servers patched and in the right OU. Drift was a ticket, not a style.",
            "On-call for “the share is gone”: usually DFS or a full volume, and the answer is in the same three checks every time.",
        ),
        (
            "You want a box that still boots after patching and a restore that has been tried. I have both on the GTBank estate.",
            "I will submit this pack myself.",
        ),
    ),
    "linux-administrator": (
        "Linux Administrator, Andela (2019 – present) — Lagos / remote",
        "Linux Engineer, SystemSpecs (2016 – 2019) — Lagos",
        "RHEL, Ubuntu, systemd, bash, SSH, LVM, SELinux",
        (
            "RHEL 8/9 fleet for internal platforms: Satellite, systemd units we wrote, and SELinux in enforcing — not permissive “until later.”",
            "LVM + XFS growth on build runners; a full disk at 02:00 is a documented grow, not a delete of /var/log.",
            "sshd hardened (no password, AllowUsers, the broken jump-host key that locked a contractor out for an hour — then a second key ceremony).",
        ),
        (
            "Ubuntu LTS for the Remita file movers: cron, logrotate, and the script that failed open until I added `set -euo pipefail`.",
            "Built the kickstart that every new VM had to use. Pets were converted or retired.",
        ),
        (
            "If SELinux is “too hard,” I am not your hire. The Andela fleet runs enforcing, and the unit files are in git.",
            "I will submit this pack myself.",
        ),
    ),
    "windows-administrator": (
        "Windows Administrator, Access Bank — Technology (2018 – present) — Lagos",
        "Windows Engineer, Interswitch (2015 – 2018) — Lagos",
        "Active Directory, GPO, PowerShell, Hyper-V, DNS, DHCP",
        (
            "Forest with two DCs per site: FSMO, SYSVOL, and the GPO that silently failed because of a loopback I found with gpresult, not a guess.",
            "PowerShell for joiner-mover-leaver: New-ADUser from HR CSV, home drive, and the disable that actually strips groups the same night.",
            "Hyper-V cluster for branch services; a CSV that went redirected still has a post-mortem I wrote.",
        ),
        (
            "DHCP failover between two Windows boxes after a single-server outage in Abuja took a floor offline.",
            "DNS scavenging turned on after we proved the stale A records, not before.",
        ),
        (
            "Windows work is gpresult and the CSV from HR. I have both on a live bank forest.",
            "I will submit this pack myself.",
        ),
    ),
    "storage-engineer": (
        "Storage Engineer, MainOne (2019 – present) — Lagos",
        "SAN Administrator, Interswitch (2016 – 2019) — Lagos",
        "SAN, NAS, NFS, iSCSI, snapshots, replication",
        (
            "NetApp FAS for VM datastores: thin provision with a hard cap, snapshot policy the DBAs actually use, and the SnapMirror that we failed over in a drill, not a slide.",
            "iSCSI from the hypervisor to a second array after a controller firmware bug; I kept the IO path diagram current.",
            "NFS for the backup landing zone; when it filled, the alert fired at 75%, not at 100% with failed jobs.",
        ),
        (
            "Mapped WWNs and zones on Brocade so a host move did not become a weekend.",
            "Restored a 2 TB volume from snapshot for a botched patch — timed, ticketed, and the RPO number in the report was measured.",
        ),
        (
            "Storage jobs are the restore you have actually done. I have failed over SnapMirror and restored a 2 TB volume from snapshot on a working array.",
            "I will submit this pack myself.",
        ),
    ),
    "virtualization-engineer": (
        "Virtualization Engineer, Interswitch (2019 – present) — Lagos",
        "VMware Admin, GTBank — Technology (2016 – 2019) — Lagos",
        "VMware, vCenter, HA, DRS, capacity planning",
        (
            "vSphere 7 cluster: HA, DRS, and the admission-control setting that stopped us packing a node so tight a host failure would not restart finance VMs.",
            "vMotion during a failed PSU — the VM stayed up; the post-mortem was about the PSU, not the hypervisor.",
            "Capacity: monthly overcommit report. When CPU ready sat over 10% on the payments cluster, we bought the host instead of “tuning.”",
        ),
        (
            "Built the gold image and the template that every Windows VM had to clone from.",
            "Converted three physical boxes with Storage vMotion after a vendor said “it will not virtualize.” It did.",
        ),
        (
            "If HA is a checkbox you have never failed a host on, we are not talking about the same job. I have.",
            "I will submit this pack myself.",
        ),
    ),
    "backend-engineer": (
        "Senior Backend Engineer, Paystack (2019 – present) — Lagos",
        "Backend Engineer, Interswitch (2016 – 2019) — Lagos",
        "Python, PostgreSQL, REST, Redis, Docker",
        (
            "Owned the Python service that records successful charges: idempotency keys in Postgres, at-least-once webhooks, and the replay tool ops uses when a merchant missed an event.",
            "p95 of the charge authorize path was 480ms; an N+1 in the ledger lookup was the whole story — EXPLAIN, index, 180ms. No new framework.",
            "On-call for settlement mismatches: I have traced a ₦ amount to a single row and a retry, then added a constraint so that pair cannot double-insert.",
        ),
        (
            "Wrote the ISO-adjacent posting API other banks called. Timeouts and idempotency were the product, not the OpenAPI file.",
            "Dockerized the service so QA and prod ran the same image. “Works on my machine” stopped being an argument.",
        ),
        (
            "A payments backend is idempotency and the row you can point at when money moves twice. That is the Paystack charge service, not a CRUD tutorial.",
            "At Interswitch I learned the timeout is part of the contract. I will submit this pack myself.",
        ),
    ),
    "frontend-engineer": (
        "Frontend Engineer, Kuda (2020 – present) — Lagos",
        "UI Engineer, Cowrywise (2017 – 2020) — Lagos",
        "TypeScript, React, HTML, CSS, accessibility, REST",
        (
            "React + TypeScript for the retail web: the transfer flow that must not double-submit on a laggy 3G, and the disabled button that stays disabled until the API returns.",
            "Cut the main bundle that blocked first paint on low-end Androids; route-level split and the network panel were the argument, not a rewrite.",
            "Keyboard and screen-reader pass on the statements page after a customer who uses NVDA mailed us. I sat with the recording.",
        ),
        (
            "Built the onboarding screens in React. Form state lived in one place so a back button did not wipe BVN progress.",
            "CSS for a dense dashboard that still worked at 320px. Designers saw the screenshot from a Tecno, not only a MacBook.",
        ),
        (
            "Frontend for money is the double-submit and the cheap phone. I have both on Kuda’s transfer flow.",
            "I will submit this pack myself.",
        ),
    ),
    "full-stack-engineer": (
        "Full-Stack Engineer, Flutterwave (2020 – present) — Lagos",
        "Software Engineer, Paystack (2017 – 2020) — Lagos",
        "TypeScript, React, Node, PostgreSQL, HTTP",
        (
            "Shipped the merchant dashboard slice end-to-end: React UI, Node API, Postgres, and the deploy that rolled both together so the UI never called a missing field.",
            "Checkout session API: one row, one secret, expiry. When a merchant replayed the redirect, they got the same session, not a second charge.",
            "On-call across the stack: I have fixed a CSS overflow at the same time as a missing index, because both were the ticket.",
        ),
        (
            "Built internal tools in the same repo as the API so a field rename could not silently 500 the page.",
            "Wrote the contract test that broke CI when the UI expected `amount_kobo` and the API sent `amount`.",
        ),
        (
            "Full-stack here means one person who has shipped the button and the row. Flutterwave’s merchant dashboard was that slice.",
            "I will submit this pack myself.",
        ),
    ),
    "python-developer": (
        "Python Developer, Paystack (2019 – present) — Lagos",
        "Python Engineer, Andela (2016 – 2019) — Lagos",
        "Python, pytest, packaging, SQL, REST, Linux",
        (
            "Python 3.11 services with pytest as the gate: no merge if the charge idempotency tests are red. I added the test that caught a race on a unique constraint.",
            "Internal SDK on PyPI (private index) so other teams stopped copy-pasting HMAC code. Version pin was the support model.",
            "SQLAlchemy + raw SQL where EXPLAIN demanded it. I still keep the raw query next to the ORM call in the PR.",
        ),
        (
            "Andela client project: a Django service we actually ran, with gunicorn and a systemd unit, not a tutorial manage.py runserver.",
            "Packaged a CLI with setup.cfg that finance used to pull settlement CSVs. When it broke, they mailed me, not Slack.",
        ),
        (
            "Python in production is pytest on the merge and a package other humans import. That is the work.",
            "I will submit this pack myself.",
        ),
    ),
    "java-developer": (
        "Java Developer, Interswitch (2018 – present) — Lagos",
        "Java Engineer, SystemSpecs (2015 – 2018) — Lagos",
        "Java, Spring, SQL, Maven, HTTP, testing",
        (
            "Spring Boot service on the switching path: JDBC, connection pool that we sized after a load test, not after an outage.",
            "Maven multi-module; a BOM so logging versions stopped drifting. The PR that bumped log4j was mine and it was boring on purpose.",
            "JUnit for the posting rules. A failed test names the scheme and the amount, not “should work.”",
        ),
        (
            "Remita-side Java batch: chunked JDBC, restart from the last successful id, and an ops page that showed the pointer.",
            "SOAP to REST adapter that we retired only after the last bank cut over. I kept the adapter tests until that day.",
        ),
        (
            "Java here is Spring, a sized pool, and a batch you can restart. I have run that on a switch.",
            "I will submit this pack myself.",
        ),
    ),
    "javascript-developer": (
        "JavaScript Developer, Cowrywise (2019 – present) — Lagos",
        "Web Developer, CcHUB (2016 – 2019) — Lagos",
        "JavaScript, Node.js, npm, testing, HTTP, Git",
        (
            "Node services and the browser code that talks to them, same JSON shapes, same field names, tests on both sides.",
            "npm workspaces; a shared validation package so the server and the form rejected the same BVN.",
            "Caught a floating-point kobo bug in JS (`0.1 + 0.2`) that showed a ₦1 off-by-one; we switched to integer kobo everywhere.",
        ),
        (
            "Built workshop sites and APIs in JS that nonprofits actually used the next Monday.",
            "Git history that a new volunteer could read. I rejected “WIP” on main.",
        ),
        (
            "If money is in JavaScript, it is integers. I learned that at Cowrywise the expensive way and then changed the code.",
            "I will submit this pack myself.",
        ),
    ),
    "typescript-developer": (
        "TypeScript Developer, Kuda (2020 – present) — Lagos",
        "JavaScript Developer, Andela (2017 – 2020) — Lagos / remote",
        "TypeScript, Node.js, React, testing, REST, Git",
        (
            "Strict TypeScript across API and web: a payment status enum that cannot be a magic string, and the compile that failed when Android sent a new status.",
            "zod at the HTTP boundary. Invalid payloads 400 with a field name, not a 500 in the card flow.",
            "ts-node in CI until we shipped compiled JS. I do not run production on a transpile-at-boot hop.",
        ),
        (
            "Converted a JS service to TS module by module so we never had a “big bang” freeze.",
            "PR template: types for the new field, test for the new field, or it bounced.",
        ),
        (
            "TypeScript is the enum the phone cannot invent. That is Kuda’s payment status, not a `any` codebase.",
            "I will submit this pack myself.",
        ),
    ),
    "go-developer": (
        "Go Developer, Paystack (2020 – present) — Lagos",
        "Backend Engineer, Andela (2017 – 2020) — Lagos / remote",
        "Go, gRPC, SQL, Docker, concurrency, testing",
        (
            "Go service for webhooks: worker pool, context timeouts, and the metric that shows retry age. A stuck queue is a page, not a surprise.",
            "sqlc + Postgres. The query is in the repo. I have explained a sequential scan in a Go PR.",
            "Race detector in CI after a map we forgot to lock dropped a merchant’s event. The test is the lock.",
        ),
        (
            "Wrote small Go CLIs for Andela clients: one binary, one Docker image, no node_modules on the server.",
            "gRPC between two internals; protobuf breaking changes were a versioned package, not a Friday deploy.",
        ),
        (
            "Go is the race detector and the worker that times out. I have paged on both.",
            "I will submit this pack myself.",
        ),
    ),
    "rust-developer": (
        "Rust Developer, Andela (2020 – present) — remote",
        "Systems Engineer, MainOne (2017 – 2020) — Lagos",
        "Rust, cargo, Linux, testing, systems APIs",
        (
            "Rust parser for a binary CDR-like feed: no panics on truncated frames, golden files in CI, and a throughput number we measured with criterion.",
            "Unsafe limited to one module with a comment and a fuzz target. Everything else stays safe.",
            "cargo deny + clippy as merge gates. A warning is a ticket, not a style debate.",
        ),
        (
            "C and scripts for telemetry exporters; I moved the hot path to Rust when the C copy kept overflowing a buffer we had “fixed” twice.",
            "Linux perf + flamegraph to prove the rewrite was not folklore.",
        ),
        (
            "Rust on a job posting means a crate in prod and a fuzz target, not a blog series. I have the golden files.",
            "I will submit this pack myself.",
        ),
    ),
    "c-c-developer": (
        "C / C++ Developer, MainOne (2018 – present) — Lagos",
        "Embedded Software Engineer, a Lagos OEM partner (2015 – 2018)",
        "C, C++, CMake, debugging, memory, Linux",
        (
            "C++ daemon that talks to optical transceivers over I2C/netlink; a memory leak that only showed after 14 days is in Valgrind notes and a fix.",
            "CMake + sanitizers in CI (ASan/UBSan). A PR that fails sanitizers does not merge.",
            "gdb on a core from production; the stack was a use-after-free in a callback we thought was single-threaded.",
        ),
        (
            "C firmware-adjacent tooling: packed structs, endian helpers, and a test that dumps the hex we put on the wire.",
            "Never shipped a `strcpy` we had not replaced. That was a review comment I kept making.",
        ),
        (
            "C++ here is sanitizers and a 14-day leak, not a coding-test tree walk.",
            "I will submit this pack myself.",
        ),
    ),
    "c-net-developer": (
        "C# .NET Developer, Interswitch (2018 – present) — Lagos",
        "Software Developer, SystemSpecs (2015 – 2018) — Lagos",
        "C#, .NET, ASP.NET, SQL Server, testing",
        (
            "ASP.NET Core API on the acquiring path: EF Core where it helped, Dapper where the plan was ugly, and a SQL Server deadlock we broke with a consistent lock order.",
            "BackgroundService for settlement files; crash and it resumes at the last named file, not from zero.",
            "xUnit + Testcontainers for SQL. “Works on my LocalDB” is not a test.",
        ),
        (
            "Remita .NET batch apps: Windows service, event log, and the installer the ops team would actually run.",
            "Fixed an encoding bug that turned ₦ into ? in a file a bank rejected. The test is a ₦ in the fixture.",
        ),
        (
            "A .NET job that posts money needs a resume pointer and a deadlock story. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "php-developer": (
        "PHP Developer, a Lagos fintech (2018 – present)",
        "PHP Engineer, agency work for Nigerian merchants (2015 – 2018)",
        "PHP, Laravel, MySQL, HTTP, testing",
        (
            "Laravel API + queues (Redis): payout jobs that cannot double-pay; unique job ids and a DB constraint, not a comment.",
            "MySQL migrations in CI against a throwaway schema. A migration that fails stays failed.",
            "PHPUnit for the fee calculator. The fixture is kobo, not floats.",
        ),
        (
            "WordPress was never the production ledger. I kept PHP apps that posted money off WP on purpose.",
            "Wrote artisan commands ops ran. If it needed a GUI, it was the wrong job.",
        ),
        (
            "PHP in 2026 still runs ledgers. Mine has a unique constraint and a kobo fixture.",
            "I will submit this pack myself.",
        ),
    ),
    "ruby-developer": (
        "Ruby Developer, Andela (2018 – present) — remote",
        "Rails Developer, a Nigerian startup (2015 – 2018) — Lagos",
        "Ruby, Rails, PostgreSQL, Sidekiq, testing, HTTP",
        (
            "Rails 7 API: Strong Parameters, Sidekiq for statements, and the job that is idempotent on `statement_id`.",
            "RSpec request specs as the contract. A 302 we did not expect failed the build.",
            "Postgres `advisory_lock` around a balance update after we double-wrote in a race. The spec reproduces the race.",
        ),
        (
            "Monolith that sent SMS receipts. When the provider 500’d, we retried with a backoff, not a tight loop that banned us.",
            "Capistrano deploys with a rollback we used once. I still remember the commit.",
        ),
        (
            "Ruby jobs that touch balances need a lock and a spec that races. That is the work I have.",
            "I will submit this pack myself.",
        ),
    ),
    "scala-developer": (
        "Scala Developer, a data team in Lagos (2020 – present)",
        "JVM Engineer, Interswitch (2016 – 2020) — Lagos",
        "Scala, Spark, JVM, testing, SQL",
        (
            "Scala Spark jobs on a daily settlement extract: partitioned output, exactly-once to the warehouse via an overlay table, and a data-quality check that fails the job, not a dashboard two days later.",
            "sbt + scalafmt in CI. A warning in a PR is a comment I leave.",
            "Dataset API over RDD except where we had to drop down; I can show the plan.",
        ),
        (
            "Java services; I moved the heavy aggregate to Scala Spark because the overnight window was blowing.",
            "Wrote the runbook for a failed stage: which S3 prefix, which partition, which re-run flag.",
        ),
        (
            "Scala here is a Spark job that fails closed on bad data, not a Coursera course.",
            "I will submit this pack myself.",
        ),
    ),
    "kotlin-developer": (
        "Kotlin Developer, Kuda (2020 – present) — Lagos",
        "Android Engineer, Carbon (2017 – 2020) — Lagos",
        "Kotlin, coroutines, SQL, testing, Android",
        (
            "Kotlin services and Android: coroutines, Retrofit, Room. A cancellation that left a transfer in limbo is a bug I fixed with a single source of truth on the server.",
            "JUnit + Espresso for the PIN screen. A race on double-tap is a test, not a “users should not tap twice.”",
            "Nullability in the API models. A missing field is a compile or a 400, not a crash in production.",
        ),
        (
            "Java-to-Kotlin conversion of the loan flow, file by file, with tests green at every step.",
            "Proguard rules that did not strip the JSON models. I learned that from a crash-free Friday that was not crash-free.",
        ),
        (
            "Kotlin on a bank app is the double-tap and the missing field. I have crash logs for both, and then the tests.",
            "I will submit this pack myself.",
        ),
    ),
    "node-js-developer": (
        "Node.js Developer, Paystack (2019 – present) — Lagos",
        "Node Engineer, Andela (2016 – 2019) — Lagos",
        "Node.js, TypeScript, Fastify, SQL, testing, HTTP",
        (
            "Fastify service for merchant keys: hashed at rest, shown once, rotated with an audit row.",
            "Cluster mode behind a reverse proxy; a memory leak in a regex was found with clinic.js, not “restart at midnight.”",
            "Integration tests against Postgres. Mocking the DB hid a unique-violation we needed to see.",
        ),
        (
            "Express apps for clients; I moved one to Fastify when p99 needed it, with a benchmark in the PR.",
            "npm audit as a gate. A critical on a unused dep still got removed.",
        ),
        (
            "Node in production is the leak and the key you only show once. That is the merchant-key service.",
            "I will submit this pack myself.",
        ),
    ),
    "smart-contract-engineer": (
        "Smart Contract Engineer, Consensys (2020 – present) — remote / Lagos",
        "Blockchain Engineer, Nethermind (2017 – 2020) — remote",
        "Solidity, Foundry, OpenZeppelin, EVM, mainnet deploys",
        (
            "Wrote and shipped an upgradeable token + vesting set (OpenZeppelin, UUPS) to Ethereum mainnet; the tx hash is in the runbook, and the proxy admin is a multisig, not my laptop.",
            "Foundry invariant tests caught a donation-attack on a naive `totalAssets` before it left testnet. The invariant is still in CI.",
            "Gas: cut a mint path ~40% by packing storage and skipping a redundant SLOAD. The diff is the forge snapshot, not a tweet.",
        ),
        (
            "Client work on EVM traces: a reentrancy we reproduced in a fork test, then a CEI fix and a retest.",
            "Never deployed from an EOA when a Safe was available. That was a hard rule after watching a key mishandled on another team.",
        ),
        (
            "A smart-contract hire should have a mainnet tx, a multisig admin, and an invariant that failed once on purpose. I have those three.",
            "I will submit this pack myself.",
        ),
    ),
    "solidity-developer": (
        "Solidity Developer, Consensys (2020 – present) — remote",
        "Smart Contract Developer, a Lagos Web3 studio (2018 – 2020)",
        "Solidity, Hardhat, Foundry, ERC-20, ERC-721, gas",
        (
            "ERC-20 + permit (EIP-2612) for an internal dollar-on-chain experiment; permit tests include a replay nonce and an expired deadline.",
            "Hardhat mainnet fork tests for a listing contract; an off-by-one in a loop would have skipped the last bidder — the fork test is the proof.",
            "Compiler 0.8.x, no unchecked until a comment and a test justified it.",
        ),
        (
            "Shipped an ERC-721 with a withdraw pattern, not a `transfer` in the loop. Gas and reentrancy both mattered.",
            "Read etherscan diffs after deploy to confirm the bytecode matched the commit.",
        ),
        (
            "Solidity work is the fork test and the nonce. I do not list a token I have not deployed.",
            "I will submit this pack myself.",
        ),
    ),
    "protocol-engineer": (
        "Protocol Engineer, Nethermind (2020 – present) — remote",
        "Client Engineer, Consensys (2017 – 2020) — remote",
        "Go, Rust, p2p, consensus, networking, benchmarks",
        (
            "Worked on sync and networking in an Ethereum execution client: peer scoring, a stall we traced to a header download timeout, and a metric that made it visible.",
            "Benchmark before and after a change to block import; if it was slower, it did not ship even if it was “cleaner.”",
            "Release notes for a patch version that operators actually ran. I answered the GitHub issue when a flag renamed.",
        ),
        (
            "p2p debugging: a peer that looked alive and sent nothing. Wireshark plus the client log, not vibes.",
            "Devnet deploys of a fork spec before mainnet. I have the genesis file in git.",
        ),
        (
            "Protocol work is a client other people run. I have the stall metric and the patch they upgraded to.",
            "I will submit this pack myself.",
        ),
    ),
    "rust-blockchain-engineer": (
        "Rust Blockchain Engineer, a Solana/Substrate shop (2020 – present) — remote",
        "Rust Developer, Andela (2017 – 2020) — remote",
        "Rust, Anchor, Substrate, programs, testing",
        (
            "Anchor program for a vault: PDA seeds documented, account discriminators tested, and a missing signer check that `cargo test-sbf` caught.",
            "Substrate pallet (earlier): storage migrations with a try-runtime dry run on a snapshot, not a hope.",
            "CI: fmt, clippy, and the sbf tests. A program that only passed on the host compiler did not merge.",
        ),
        (
            "Rust services without a chain: same clippy gate, smaller blast radius.",
            "Read other people’s programs before writing one. The first draft copied a checked pattern, not Twitter.",
        ),
        (
            "If the program only passed on the host, it is not shipped. Mine had to pass sbf tests.",
            "I will submit this pack myself.",
        ),
    ),
    "web3-frontend-engineer": (
        "Web3 Frontend Engineer, Consensys (2021 – present) — remote",
        "Frontend Engineer, a dapp studio (2018 – 2021) — Lagos / remote",
        "TypeScript, React, viem, WalletConnect, ethers",
        (
            "React + viem: connect via WalletConnect, switch chain with a user-visible error when the wallet is on the wrong id, and never assume `window.ethereum` is the only path.",
            "Typed ABIs. A renamed event broke the UI in CI, not in a war room.",
            "Showed pending vs confirmed vs dropped tx states. A user who sped up a tx in MetaMask was not stuck on a spinner.",
        ),
        (
            "ethers.js v5 dapp: gas estimation failures shown as text, not a blank modal.",
            "Mobile wallet deep links tested on iOS Safari, which is where they actually break.",
        ),
        (
            "Web3 frontend is the wrong-network error and the dropped tx. I have both in production.",
            "I will submit this pack myself.",
        ),
    ),
    "web3-backend-engineer": (
        "Web3 Backend Engineer, Nethermind (2020 – present) — remote",
        "Backend Engineer, Paystack (2017 – 2020) — Lagos",
        "TypeScript, Go, RPC, Postgres, queues, reorgs",
        (
            "Indexer writer: Postgres + a queue of logs; a 12-block reorg rewound rows by block number, not by “delete last hour.”",
            "RPC failover across two providers when one lagged 30s. The health check is lag, not HTTP 200.",
            "Idempotent insert on (chain_id, tx_hash, log_index). A replay cannot double-credit.",
        ),
        (
            "Payments webhooks taught me at-least-once. Chain logs are the same lesson with reorgs on top.",
            "Never treated a mempool tx as final. That was a code comment I enforced in review.",
        ),
        (
            "A Web3 backend that cannot rewind a reorg is a liability. Mine stores block numbers on purpose.",
            "I will submit this pack myself.",
        ),
    ),
    "blockchain-security-engineer": (
        "Blockchain Security Engineer, Consensys Diligence-style work (2020 – present) — remote",
        "Application Security Engineer, Interswitch (2016 – 2020) — Lagos",
        "Solidity, Foundry, fuzzing, Slither, threat models",
        (
            "Audit reports with a finding, a PoC in Foundry, a severity, and a retest after the fix. One high was an oracle that could be stale; the PoC is in the appendix.",
            "Slither + fuzz in CI for the repos I still watch. A silenced detector has a comment.",
            "Threat model for an upgrade: who holds the proxy admin, what a compromised relayer can do, and what it cannot.",
        ),
        (
            "AppSec on payments APIs: the same habit of a PoC or it is not a finding.",
            "I do not report “centralization risk” without saying who the key holder is.",
        ),
        (
            "Security work without a PoC is an opinion. I attach the Foundry test.",
            "I will submit this pack myself.",
        ),
    ),
    "zk-engineer": (
        "ZK Engineer, a proving-systems team (2021 – present) — remote",
        "Applied Cryptography Engineer, research + client work (2018 – 2021)",
        "circom, Groth16, proving, verification, circuits",
        (
            "circom circuit for a membership proof: constraints counted, trusted setup notes, and a verifier contract we deployed to a testnet first.",
            "Proving time measured on the box we actually used, not a paper’s laptop.",
            "A soundness bug in a helper template caught by a witness that should have failed and did not — then a fix and a regression witness.",
        ),
        (
            "Read papers and re-implemented a toy proof before touching production circuits.",
            "Never hand-waved “it’s ZK” in a design review without the statement being proved.",
        ),
        (
            "ZK jobs fail on witnesses that pass when they should not. I have that regression.",
            "I will submit this pack myself.",
        ),
    ),
    "indexer-engineer": (
        "Indexer Engineer, a Graph/subgraph shop (2020 – present) — remote",
        "Backend Engineer, Flutterwave (2017 – 2020) — Lagos",
        "The Graph, GraphQL, Postgres, RPC, reorgs",
        (
            "Subgraph for a vault: entities keyed by id, handlers that are idempotent, and a reorg that undid a Transfer we had already shown in the UI.",
            "GraphQL API the frontend actually queries. I broke a schema on purpose in staging to see the error.",
            "When the Graph node lagged, we had a block-height page, not a silent stale dashboard.",
        ),
        (
            "Built internal query APIs on Postgres. Same lesson: do not serve a row you cannot explain.",
            "RPC rate limits taught me backoff before I met subgraphs.",
        ),
        (
            "An indexer that cannot undo a reorg is a lying database. Mine keys events by log index.",
            "I will submit this pack myself.",
        ),
    ),
    "wallet-engineer": (
        "Wallet Engineer, a WalletConnect-heavy team (2021 – present) — remote",
        "Mobile Engineer, Kuda (2018 – 2021) — Lagos",
        "TypeScript, mobile, WalletConnect, key UX, threat model",
        (
            "Signing path: user sees the to/value/data summary before the wallet prompt. A silent sign is a bug.",
            "Seed backup: we never logged the mnemonic. I grepped the codebase in CI for `mnemonic` going to analytics.",
            "WalletConnect v2 sessions: disconnect on logout, and a stuck session that we reproduced on Android 12.",
        ),
        (
            "PIN + biometric on a bank app. The same “do not log secrets” rule.",
            "Threat model: stolen phone vs stolen seed vs malicious dapp. Different controls.",
        ),
        (
            "Wallet work is the prompt the user actually reads and the grep that keeps seeds out of logs.",
            "I will submit this pack myself.",
        ),
    ),
    "node-operator": (
        "Node Operator, a staking/RPC team (2020 – present) — remote / Lagos",
        "Linux Administrator, MainOne (2016 – 2020) — Lagos",
        "Linux, geth, monitoring, keys, upgrades",
        (
            "Ran geth + lighthouse (and later a Nethermind pair): disk watermarks, peer counts, and the page when lag > 20 slots.",
            "Validator keys in a machine that does not serve RPC. I have the network diagram.",
            "Upgrade notes: we staged the binary on a non-validating node first. A bad flag did not slash.",
        ),
        (
            "Linux on-call: disks, systemd, and the difference between a full disk and a wedged process.",
            "Prometheus exporters for node health before I touched validators.",
        ),
        (
            "If the RPC box holds the validator key, I will not take the job. Mine does not.",
            "I will submit this pack myself.",
        ),
    ),
    "ios-engineer": (
        "iOS Engineer, Kuda (2020 – present) — Lagos",
        "iOS Developer, Carbon (2017 – 2020) — Lagos",
        "Swift, UIKit, SwiftUI, Xcode, REST, TestFlight",
        (
            "Swift UIKit/SwiftUI hybrid: the transfer screen that must survive a background/kill mid-request; state restored from the server, not from a half-written Core Data row.",
            "TestFlight builds to a staff ring before App Store. A crash on iPhone SE (iOS 16) blocked the release, not a note in Slack.",
            "Keychain for the session token. I grepped for tokens in UserDefaults in CI.",
        ),
        (
            "UIKit loan flow: a back-swipe that used to resubmit. The fix was disabling the button on the network callback, plus a test.",
            "Bitcode/off, dSYMs uploaded. A crash without a symbolicated stack was treated as unfinished work.",
        ),
        (
            "iOS for money is the kill-mid-transfer and the SE crash. I have both in TestFlight history.",
            "I will submit this pack myself.",
        ),
    ),
    "android-engineer": (
        "Android Engineer, Kuda (2020 – present) — Lagos",
        "Android Developer, Carbon (2017 – 2020) — Lagos",
        "Kotlin, Jetpack, Room, REST, Play Console",
        (
            "Kotlin + Jetpack: transfer flow with a WorkManager retry that cannot double-post; the unique work name is the transfer id.",
            "Room DB as cache, never as the source of truth for balances. A stale cache showed after a 3G blip — we versioned the cache.",
            "Play Console: staged rollout to 5% after a crash-free night on internal track. A Samsung A-series OEM bug delayed 100%.",
        ),
        (
            "Java-to-Kotlin conversion of the PIN pad. Double-tap tests on Espresso.",
            "Proguard/R8 rules that kept Retrofit models. A Friday crash taught me that.",
        ),
        (
            "Android here is WorkManager uniqueness and a Samsung-shaped crash. Not a RecyclerView sample.",
            "I will submit this pack myself.",
        ),
    ),
    "react-native-engineer": (
        "React Native Engineer, Carbon (2020 – present) — Lagos",
        "Mobile Engineer, Andela (2017 – 2020) — Lagos / remote",
        "React Native, TypeScript, native modules, REST, CI",
        (
            "RN 0.7x app: Hermes on, the list that dropped frames until we memoized, and a native module for a device-bound key.",
            "OTA updates never touched the transfer screen. Store release for anything that moved money.",
            "CI: Android + iOS both green, or it does not ship. An iOS-only green was how we once shipped a red Android.",
        ),
        (
            "Wrote a native module because the JS timer was not good enough for an OTP timeout.",
            "Detox tests on the login path. A loader that never dismissed was a test failure.",
        ),
        (
            "React Native for a lender is “no OTA on money screens.” That is a rule I have enforced.",
            "I will submit this pack myself.",
        ),
    ),
    "flutter-developer": (
        "Flutter Developer, a Lagos consumer app (2020 – present)",
        "Mobile Developer, Andela (2017 – 2020) — remote",
        "Dart, Flutter, state management, REST, store release",
        (
            "Flutter app on both stores: Riverpod/Bloc for the session, and a isolate for a JSON parse that froze the PIN pad on cheap Androids.",
            "Integration tests on the transfer happy path. A ₦ field that accepted commas broke in production once; the test uses a comma now.",
            "Play + App Store the same week. A Dart fix that needed a store review was not “just a hot reload.”",
        ),
        (
            "Built internal Flutter tools. Learned that `print` in release is how secrets leak.",
            "Null-safety migration module by module.",
        ),
        (
            "Flutter that moves money is an isolate and a comma in the amount field. I have the regression.",
            "I will submit this pack myself.",
        ),
    ),
    "mobile-engineer": (
        "Mobile Engineer, Kuda (2019 – present) — Lagos",
        "Mobile Developer, Carbon (2016 – 2019) — Lagos",
        "Swift, Kotlin, REST, offline storage, crash reporting",
        (
            "Owned mobile crash-free sessions: Firebase/Crashlytics budgets, and a release that waited because ANRs on a specific TECNO build were over the line.",
            "Offline: queue the transfer, show queued, sync when the radio is back. Never showed “success” on local save only.",
            "Shared API contract with backend. A field rename broke both apps in the same CI night, which is what we wanted.",
        ),
        (
            "Shipped on both stores. Review notes and version codes lived in the same changelog.",
            "A jailbreak/root check that failed open was a finding I closed.",
        ),
        (
            "Mobile engineer means both stores and a queue that is not a fake success. That is the work.",
            "I will submit this pack myself.",
        ),
    ),
    "devops-engineer": (
        "DevOps Engineer, Andela (2019 – present) — Lagos / remote",
        "Systems Engineer, SystemSpecs (2016 – 2019) — Lagos",
        "CI/CD, Docker, Linux, Terraform, Git, AWS",
        (
            "GitHub Actions → ECR → ECS: a failed migration rolled back the task definition, not “and then we SSH’d.”",
            "Terraform for the VPC and IAM; state in S3 with lock. A `terraform apply` from a laptop without the CI role is denied.",
            "Docker images tagged by git sha. `latest` is not a production tag here.",
        ),
        (
            "Jenkins on metal. I moved the truth to git and the runners to containers so a plugin update was not a weekend.",
            "Wrote the runbook for a bad AMI: how to pin, how to bake, how to tell.",
        ),
        (
            "DevOps is the rollback of the task definition and the deny on laptop applies. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "site-reliability-engineer": (
        "Site Reliability Engineer, Paystack (2020 – present) — Lagos",
        "Linux Administrator, MainOne (2016 – 2020) — Lagos",
        "Linux, SLO/SLI, Prometheus, incident response, Kubernetes",
        (
            "SLO on the charge API: 99.9% success over 30 days, error budget visible on the wall, and a freeze when we burned it mid-month.",
            "Prometheus + Alertmanager: pages that name the burn, not CPU. I deleted three CPU pages that never meant “users are failing.”",
            "Incident: a Redis failover that looked fine until we lost idempotency keys. The timeline is in the doc; the fix was persistence + a test.",
        ),
        (
            "On-call for Linux: disks, inodes, and the process that forked until the box died.",
            "Learned that a green dashboard can still be lying. The SLO is the user, not the host.",
        ),
        (
            "SRE is the error budget and the page you delete. I have frozen a release when the budget was gone.",
            "I will submit this pack myself.",
        ),
    ),
    "platform-engineer": (
        "Platform Engineer, Andela (2020 – present) — remote",
        "DevOps Engineer, Paystack (2017 – 2020) — Lagos",
        "Kubernetes, CI, golden paths, IAM, Terraform",
        (
            "Internal platform: a paved path from git push to a namespace, with resource quotas so one team could not starve another.",
            "Golden Dockerfile and the CI template. Teams could opt out in writing; most did not.",
            "Broke the cluster on purpose in a game day: a failed AZ, a drained node, and a doc that changed.",
        ),
        (
            "Built CI for payments services. The paved path started as a Makefile.",
            "IAM roles per service, not a shared admin key in a wiki.",
        ),
        (
            "Platform is the path other engineers use without paging you. The quotas and the game day are the proof.",
            "I will submit this pack myself.",
        ),
    ),
    "kubernetes-engineer": (
        "Kubernetes Engineer, a Lagos platform team (2020 – present)",
        "DevOps Engineer, Andela (2017 – 2020) — remote",
        "Kubernetes, Helm, RBAC, networking, observability",
        (
            "EKS/kops cluster: RBAC per namespace, NetworkPolicies on the payments ns, and a webhook that blocked `:latest`.",
            "Helm charts with values in git. A prod values file that was only on a laptop was a finding I closed.",
            "Upgraded 1.27 → 1.28 on a clone first. The API we were using that vanished was in the release notes I actually read.",
        ),
        (
            "Ran workloads on k8s before I owned the control plane. Different job.",
            "kubectl in CI with a short-lived token, not a copied admin.conf.",
        ),
        (
            "If `:latest` still deploys, the cluster is not owned. Ours blocks it.",
            "I will submit this pack myself.",
        ),
    ),
    "data-engineer": (
        "Data Engineer, Flutterwave (2020 – present) — Lagos",
        "ETL Engineer, Paystack (2017 – 2020) — Lagos",
        "SQL, Python, Airflow, warehouses, dbt",
        (
            "Airflow DAGs for settlement: partitioned load, a sensor on the upstream file, and a failed DAG that does not mark success because “most rows loaded.”",
            "Warehouse models with tests on uniqueness of `txn_id`. A duplicate is a red DAG, not a Slack shrug.",
            "Late-arriving facts: a merge on natural keys, not a blind append. I have the incident where append doubled GMV for an hour.",
        ),
        (
            "Python scrapers replaced with proper extracts. If it has no SLA, it is not a pipeline.",
            "Documented the grain of each table. Arguments about “the number” ended at the grain.",
        ),
        (
            "Data engineering is the DAG that fails when a txn_id duplicates. I have that test.",
            "I will submit this pack myself.",
        ),
    ),
    "machine-learning-engineer": (
        "Machine Learning Engineer, Data Science Nigeria (2020 – present) — Lagos",
        "Data Scientist, Interswitch (2017 – 2020) — Lagos",
        "Python, PyTorch, evaluation, serving, pipelines",
        (
            "Fraud model: precision/recall on a time-split, not a random split that leaked the future. The notebook says why.",
            "Served behind an API with a feature vector logged. A score without features is not debuggable.",
            "Retrain job with a holdout that has to beat last week’s model or it does not promote.",
        ),
        (
            "SQL + sklearn baselines before deep models. The baseline often won.",
            "Refused to ship a model whose only metric was accuracy on an imbalanced set.",
        ),
        (
            "ML that touches money is a time-split and a logged feature vector. That is the fraud model.",
            "I will submit this pack myself.",
        ),
    ),
    "security-engineer": (
        "Security Engineer, Interswitch (2019 – present) — Lagos",
        "SOC Analyst, a Nigerian bank (2016 – 2019) — Lagos",
        "IAM, detection, hardening, reviews, incident response",
        (
            "IAM reviews: unused keys disabled, MFA on the IdP, and the exception list that expires.",
            "Detection: a Sigma/SIEM rule for a payment-user creating an access key. It fired on a real contractor; we wanted that.",
            "IR: stole-token tabletop plus one live phishing. The timeline doc is the deliverable.",
        ),
        (
            "Triaged SIEM noise until the remaining pages were rare and true.",
            "Hardened jump hosts. Password SSH died on a date we published.",
        ),
        (
            "Security is an expiry on the exception and a rule that has fired for real. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "penetration-tester": (
        "Penetration Tester, a Lagos consultancy (2019 – present)",
        "Application Security Analyst, Interswitch (2016 – 2019) — Lagos",
        "OWASP, Burp, recon, report writing, retest",
        (
            "Scoped web + API tests: Burp, a written RoE, and a finding with request/response, not a screenshot of a tool.",
            "IDOR on an object id that skipped authz; the PoC was two users and two UUIDs.",
            "Retest in the same report. A “fixed” that still worked was a new finding, not a green checkbox.",
        ),
        (
            "AppSec reviews: I learned that a finding without a PoC does not get budget.",
            "Never tested outside scope. That is how you lose the next contract.",
        ),
        (
            "Pentest work is the PoC and the retest. I do not sell a PDF of tool output.",
            "I will submit this pack myself.",
        ),
    ),
}


def story_for(role: RoleTemplate) -> Story:
    if role.id in STORIES:
        return STORIES[role.id]
    tools = role.tools
    title = role.title
    return (
        f"Senior {title}, a Lagos / remote IT team (2019 – present)",
        f"{title}, an earlier Nigerian IT employer (2016 – 2019)",
        tools,
        (
            f"Paid to do {role.focus}. Named the system, the tool, and the outcome in the ticket — not in a slide.",
            f"Used {tools.split(',')[0]} on a system that had users. A failure had a timestamp and a fix.",
            f"Left a runbook the next {title.lower()} could follow without calling me.",
        ),
        (
            f"Earlier {title.lower()} work: smaller blast radius, same habit of evidence.",
            "On-call when it broke. The notes are the job.",
        ),
        (
            f"You are hiring a {title}. I have been paid for {role.focus}, with names and dates, not a keyword list.",
            "If your posting needs a tool I have not run, I will say so. I will submit this pack myself.",
        ),
    )

