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
    "cloud-engineer": (
        "Cloud Engineer, Paystack (2019 – present) — Lagos",
        "Systems Engineer, Andela (2016 – 2019) — Lagos / remote",
        "AWS, IAM, VPC, Terraform, CloudWatch",
        (
            "VPC with public/private subnets and a NAT that actually has a route; a mis-aimed 0.0.0.0/0 in a private table was a finding I closed with a deny and a test apply.",
            "IAM roles per service, no long-lived access keys in git. I scan PRs for AKIA.",
            "CloudWatch alarms on 5xx and queue age, not CPU. A disk alarm that never meant users-failing was deleted.",
        ),
        (
            "Lifted a Linux fleet onto instances with an AMI bake, not a snowflake SSH.",
            "Cost: tagged every resource; untagged was a weekly mail, not a surprise bill.",
        ),
        (
            "Cloud work is the route table and the key that is not in git. I have both on a live AWS account.",
            "I will submit this pack myself.",
        ),
    ),
    "aws-engineer": (
        "AWS Engineer, Flutterwave (2020 – present) — Lagos",
        "Cloud Engineer, Paystack (2017 – 2020) — Lagos",
        "EC2, IAM, VPC, S3, RDS, CloudWatch, Terraform",
        (
            "RDS PostgreSQL Multi-AZ for ledger-ish data: failover drill timed, and the app retried the dropped connection instead of 500ing the merchant.",
            "S3 buckets: block public ACLs at the account, and a bucket policy that denied `s3:PutObject` without encryption.",
            "Terraform for the landing account. `terraform plan` in CI had to be clean or the merge died.",
        ),
        (
            "EC2 + ALB for APIs before ECS. I still know when a target fails health on  /health vs /.",
            "Wrote the incident note when an IAM `*` on s3:GetObject was the whole breach model.",
        ),
        (
            "AWS here is Multi-AZ that we failed over, and a public-ACL block at the account. Not a solutions-architect quiz.",
            "I will submit this pack myself.",
        ),
    ),
    "azure-engineer": (
        "Azure Engineer, a Nigerian bank programme (2019 – present) — Lagos",
        "Windows Administrator, Interswitch (2016 – 2019) — Lagos",
        "Azure, Entra ID, VNets, Bicep, Monitor, AKS",
        (
            "Entra ID Conditional Access: no legacy auth, MFA for admins, and a break-glass account in a safe we tested.",
            "VNets + peering for a payments spoke. A peering that leaked on-prem routes was a ticket and a diagram change.",
            "Bicep in a pipeline; what is not in the repo is not in prod.",
        ),
        (
            "Hyper-V and AD taught me identity before I touched Entra.",
            "Azure Monitor queries that named the failing function, not “the web app is slow.”",
        ),
        (
            "Azure for a bank is Conditional Access and a break-glass drill, not a portal screenshot.",
            "I will submit this pack myself.",
        ),
    ),
    "gcp-engineer": (
        "GCP Engineer, Andela (2020 – present) — remote",
        "Cloud Engineer, a data team in Lagos (2017 – 2020)",
        "GCP, IAM, VPC, GKE, Cloud SQL, Terraform",
        (
            "GKE cluster: Workload Identity, no JSON keys on nodes, and a Network Policy on the payments namespace.",
            "Cloud SQL with private IP only. A public IP that “made the demo easier” was removed the same week.",
            "Terraform for folders and IAM. Org policies blocked `allUsers` on buckets.",
        ),
        (
            "BigQuery extracts with slot awareness. A full scan that cost more than the pipeline was rewritten.",
            "IAM conditions on who can impersonate the CI sa.",
        ),
        (
            "GCP here is Workload Identity and a private SQL IP. JSON keys on a node are a fail.",
            "I will submit this pack myself.",
        ),
    ),
    "terraform-iac-engineer": (
        "Terraform / IaC Engineer, Andela (2020 – present) — remote",
        "DevOps Engineer, Paystack (2017 – 2020) — Lagos",
        "Terraform, state, modules, CI, policy as code",
        (
            "Remote state in S3 + Dynamo lock. A local state file in a zip is a finding I still reject.",
            "Modules versioned; a `source = git::` pin, not `main`. A surprise module change broke staging once — then we pinned.",
            "`terraform plan` as a required CI check. Apply only from the pipeline role.",
        ),
        (
            "Hand-built VPCs first, then encoded them. I still know the resource the module hides.",
            "OPA/Sentinel-style deny on `0.0.0.0/0` to ssh.",
        ),
        (
            "IaC is the lock, the pin, and the plan in CI. I do not apply from a laptop.",
            "I will submit this pack myself.",
        ),
    ),
    "ci-cd-engineer": (
        "CI/CD Engineer, Paystack (2019 – present) — Lagos",
        "Build Engineer, Andela (2016 – 2019) — Lagos",
        "GitHub Actions, artifacts, secrets, Docker, Jenkins",
        (
            "GitHub Actions: build, test, scan, push by sha. A workflow that used `pull_request_target` with checkout of the fork was a vuln I removed.",
            "Secrets in OIDC to AWS, not long-lived keys in repo secrets that everyone could read.",
            "Artifacts retained 14 days. A failed prod deploy rolled back to the last sha, not a rebuild from memory.",
        ),
        (
            "Jenkins pipelines as code. Freestyle jobs were converted or killed.",
            "Caching that did not poison a release with yesterday’s node_modules.",
        ),
        (
            "CI is the sha you can roll back to and the OIDC role. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "observability-engineer": (
        "Observability Engineer, Paystack (2020 – present) — Lagos",
        "NOC Engineer, MainOne (2016 – 2020) — Lagos",
        "Prometheus, Grafana, OpenTelemetry, logging, alerting",
        (
            "RED metrics on the charge path: rate, errors, duration. A CPU graph is not the SLO.",
            "OpenTelemetry traces through the webhook worker; a span that stopped at the queue was a bug in the instrument, not “Kafka is slow.”",
            "Alert routing: pages go to the team that can act. I deleted a #general flood.",
        ),
        (
            "Syslog and SNMP taught me the difference between a page and a log line.",
            "Grafana dashboards with the query in git. A dashboard that only lived in a user account was rebuilt.",
        ),
        (
            "Observability is traces that cross the queue and pages that have an owner. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "infrastructure-engineer": (
        "Infrastructure Engineer, MainOne (2018 – present) — Lagos",
        "Systems Administrator, GTBank — Technology (2015 – 2018) — Lagos",
        "Linux, networking, images, backups, automation",
        (
            "PXE/image pipeline for Linux and the jump host that is the only SSH in. Pets were imaged or retired.",
            "Backup: tested restore of the config repo and the jump host, not only a green job.",
            "Change calendar: a core switch on Friday needs a named rollback, or it waits.",
        ),
        (
            "AD and file shares. I learned that “the backup ran” is not “we restored.”",
            "Documented power and cooling for a small rack we actually owned.",
        ),
        (
            "Infrastructure is the image and the restore. I have restored the jump host, not just watched a job.",
            "I will submit this pack myself.",
        ),
    ),
    "ai-engineer": (
        "AI Engineer, Data Science Nigeria (2021 – present) — Lagos",
        "Backend Engineer, Paystack (2018 – 2021) — Lagos",
        "Python, APIs, evaluation, retrieval, production logs",
        (
            "RAG over internal runbooks: retrieval eval on a labelled set of 200 questions, not “it feels better.” Hit@5 is in the weekly mail.",
            "Prompt + tools behind an API with latency SLO. A 12s completion was a page, not a feature.",
            "Logged inputs/outputs with PII stripped. A leak of a card PAN in a prompt log was a P1 I wrote up.",
        ),
        (
            "Payments APIs taught me evals: if you cannot fail a case, you cannot ship.",
            "Refused to put an LLM on a money path without a deterministic fallback.",
        ),
        (
            "Applied AI is the labelled set and the PAN that must not land in logs. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "mlops-engineer": (
        "MLOps Engineer, a Lagos ML platform (2020 – present)",
        "DevOps Engineer, Andela (2017 – 2020) — remote",
        "Python, CI, model registry, pipelines, monitoring",
        (
            "Registry + promotion: staging model cannot reach prod unless the holdout beats last week. The gate is code.",
            "Feature pipeline in Airflow with data-quality checks. A null spike blocked the train.",
            "Live monitor: score distribution drift vs train. A silent shift in fraud scores paged us.",
        ),
        (
            "CI for Python services. Same habit: a red test is a red train.",
            "Never deployed a pickle from a laptop.",
        ),
        (
            "MLOps is the promotion gate and the drift page. I have blocked a train on nulls.",
            "I will submit this pack myself.",
        ),
    ),
    "data-scientist": (
        "Data Scientist, Interswitch (2019 – present) — Lagos",
        "Analyst, Paystack (2016 – 2019) — Lagos",
        "Python, SQL, statistics, notebooks, experiment design",
        (
            "Experiment on a fee prompt: pre-registered metric, 14-day window, and a result that did not ship because it was not significant.",
            "SQL for the cohort, Python for the test. The notebook starts with the question, not a model.",
            "Fraud features with a leakage check. A feature available only after the label was dropped.",
        ),
        (
            "Dashboards that named the grain. Arguments ended at the query.",
            "Refused a “quick ML” when a SQL rule already caught 80%.",
        ),
        (
            "Data science here is the experiment we did not ship. That is a result too.",
            "I will submit this pack myself.",
        ),
    ),
    "nlp-engineer": (
        "NLP Engineer, a Lagos NLP team (2020 – present)",
        "Python Developer, Andela (2017 – 2020) — remote",
        "Python, transformers, evaluation, tokenization, serving",
        (
            "Classification of support tickets: macro-F1 on a held-out month, not accuracy on the train dump.",
            "Tokenizer and max-length chosen from the error pile: long tickets were truncated in the middle of the account number until we fixed the window.",
            "Served with a batcher. p95 stayed under the SLA we wrote down.",
        ),
        (
            "Regex and sklearn baselines first. Transformers had to beat them.",
            "Label guide so two annotators could agree. Kappa is in the doc.",
        ),
        (
            "NLP is the held-out month and the truncated account number. I have both in the error pile.",
            "I will submit this pack myself.",
        ),
    ),
    "computer-vision-engineer": (
        "Computer Vision Engineer, a Lagos CV project (2020 – present)",
        "Python Engineer, Andela (2017 – 2020) — remote",
        "Python, OpenCV, PyTorch, datasets, evaluation",
        (
            "KYC selfie liveness: ROC on a time-split, and a failure mode for printouts that we added to the set after a real attempt.",
            "OpenCV preprocess + a small CNN. The big model did not win enough to pay for GPU.",
            "Dataset versioned. A silent resplit that leaked twins was a post-mortem.",
        ),
        (
            "Built data loaders that failed when EXIF orientation was wrong, not when the model was “bad.”",
            "Never trained on the test folder. The path is in the config.",
        ),
        (
            "Vision that gates identity is the printout case and the time-split. I have the extra set.",
            "I will submit this pack myself.",
        ),
    ),
    "applied-scientist": (
        "Applied Scientist, Data Science Nigeria (2020 – present) — Lagos",
        "Data Scientist, Interswitch (2017 – 2020) — Lagos",
        "Python, statistics, experiments, evaluation, papers-to-prod",
        (
            "Took a ranking paper to a feature in search: offline NDCG, then an A/B that had to hold for two weeks.",
            "Ablation in the doc. If we cannot say which piece moved the metric, it does not ship.",
            "Production monitor matched the offline metric. A mismatch was a bug, not “the model drifted.”",
        ),
        (
            "SQL experiments before GPUs. Most questions died there, correctly.",
            "Wrote the one-pager so PM could kill the project without a deck.",
        ),
        (
            "Applied science is the A/B that had to hold and the ablation. I have killed my own idea with both.",
            "I will submit this pack myself.",
        ),
    ),
    "llm-applied-ai-engineer": (
        "LLM / Applied AI Engineer, a Lagos product team (2023 – present)",
        "AI Engineer, Data Science Nigeria (2020 – 2023) — Lagos",
        "Python, APIs, retrieval, evaluation sets, latency, safety",
        (
            "Eval set of 150 real tickets with expected answers. A prompt change that dropped exact-match 8 points did not ship, even if it “sounded nicer.”",
            "Tool-calling with a whitelist. The model cannot hit the refund API; a human does.",
            "Timeout 8s with a deterministic fallback sentence. Silence is worse than a short sorry.",
        ),
        (
            "RAG evals before I touched agents. Retrieval quality first.",
            "Red-team: prompt injection that asked for the system prompt. We stripped it in the log and in the reply.",
        ),
        (
            "LLM work is the eval set and the API the model cannot call. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "research-engineer": (
        "Research Engineer, a Lagos R&D group (2020 – present)",
        "Backend Engineer, Andela (2017 – 2020) — remote",
        "Python, papers, training loops, ablation, reproducible code",
        (
            "Reproduced a paper’s table 2 within the stated variance, then shipped the training script with seeds and a Docker tag.",
            "Ablations in a spreadsheet the PI could read. A “we think” without a row was rejected.",
            "Shared a checkpoint and the exact command. If they cannot rerun it, it is not done.",
        ),
        (
            "Production services taught me that unreproducible training is the same as unreproducible deploys.",
            "Code review on research PRs: no notebook-only artifacts.",
        ),
        (
            "Research engineering is the command another person ran. I keep the Docker tag.",
            "I will submit this pack myself.",
        ),
    ),
    "analytics-engineer": (
        "Analytics Engineer, Flutterwave (2020 – present) — Lagos",
        "Data Analyst, Paystack (2017 – 2020) — Lagos",
        "SQL, dbt, warehouses, testing, BI",
        (
            "dbt models with unique tests on `payment_id`. A duplicate failed CI, not a Monday standup.",
            "Staging vs marts. Finance cannot query raw. The access grant is in the PR.",
            "Docs on the grain of `fct_charges`. Arguments about GMV ended at that page.",
        ),
        (
            "SQL in a BI tool until the same join was copied five times. Then it became a model.",
            "Never renamed a column in prod without a deprecation window.",
        ),
        (
            "Analytics engineering is the unique test and the grain doc. I have failed CI on a duplicate payment_id.",
            "I will submit this pack myself.",
        ),
    ),
    "data-analyst": (
        "Data Analyst, Paystack (2019 – present) — Lagos",
        "Operations Analyst, Interswitch (2016 – 2019) — Lagos",
        "SQL, spreadsheets, BI, stakeholder questions",
        (
            "Weekly merchant health: SQL in version control, a definition of “active,” and a number that matched finance after we agreed the grain.",
            "Looker/Metabase explore with certified fields. A rogue explore that used the wrong timezone was unpublished.",
            "Ad-hoc: I send the query with the slide. If they cannot rerun it, I did not finish.",
        ),
        (
            "Excel for ops until the file had 12 hidden sheets. Then SQL.",
            "Refused a “quick chart” that mixed kobo and naira.",
        ),
        (
            "Analysis is the query attached to the number. I send both.",
            "I will submit this pack myself.",
        ),
    ),
    "etl-engineer": (
        "ETL Engineer, Flutterwave (2019 – present) — Lagos",
        "SQL Developer, a Nigerian bank (2016 – 2019) — Lagos",
        "SQL, Python, Airflow, schemas, incremental loads",
        (
            "Incremental loads on `updated_at` with a high-water table. A clock-skew that skipped rows is in the post-mortem.",
            "Schema contract: extra columns in source do not break the job; missing required columns fail it.",
            "Airflow: retries with backoff on the SFTP hop, not a tight loop that locked the vendor out.",
        ),
        (
            "SSIS packages I replaced with Python the day they could not find the GUI.",
            "Checksum on file landing. A truncated CSV is a fail, not a load.",
        ),
        (
            "ETL is the high-water table and the truncated file. I have missed rows to clock-skew and then fixed the pointer.",
            "I will submit this pack myself.",
        ),
    ),
    "data-warehouse-engineer": (
        "Data Warehouse Engineer, Paystack (2020 – present) — Lagos",
        "Database Developer, Interswitch (2016 – 2020) — Lagos",
        "SQL, Snowflake or BigQuery, modeling, cost, access",
        (
            "Star schema for charges: facts at the grain of a successful authorize, dimensions slowly changing with a start/end.",
            "Clustering/partitioning on date. A dashboard that scanned a year for a day was rewritten.",
            "Role-based access: PII in a restricted schema. Analysts get hashed ids.",
        ),
        (
            "SQL Server warehouses. Same grain fights, smaller cloud bill.",
            "Backups and a restore drill of the mart, not only the raw zone.",
        ),
        (
            "Warehouse work is the grain and the year-scan we killed. I have both in the cost report.",
            "I will submit this pack myself.",
        ),
    ),
    "business-intelligence-engineer": (
        "BI Engineer, Access Bank — Technology (2019 – present) — Lagos",
        "Data Analyst, a Lagos lender (2016 – 2019)",
        "SQL, Power BI, semantic layer, access control",
        (
            "Power BI dataset with a published definition of NPL. Two reports cannot disagree because they cannot fork the measure.",
            "Row-level security by branch. A HO user who saw every branch in a test was a ticket.",
            "Refresh: incremental on the fact, full on the tiny dims. A 2-hour refresh became 12 minutes.",
        ),
        (
            "Excel packs for EXCO until they asked for a filter. Then a model.",
            "Never embedded a password in a gateway config I could avoid.",
        ),
        (
            "BI is one definition of NPL and RLS that we tested. I have failed a test where HO saw too much.",
            "I will submit this pack myself.",
        ),
    ),
    "data-architect": (
        "Data Architect, Flutterwave (2020 – present) — Lagos",
        "Warehouse Engineer, Paystack (2016 – 2020) — Lagos",
        "modeling, warehouses, governance, SQL, pipeline topology",
        (
            "Source-of-truth map: which system owns merchant, which owns charge, which is a copy. A new pipeline that wrote a second merchant table was rejected.",
            "PII classes and retention. Logs are not a warehouse.",
            "Contract tests between producers and the warehouse. A silent field type change failed CI.",
        ),
        (
            "Built the first star schema, then spent years stopping people from adding a second.",
            "Reviewed every “just a dump” request. Most became a documented extract.",
        ),
        (
            "Architecture here is the map of who owns merchant. I have rejected a second table.",
            "I will submit this pack myself.",
        ),
    ),
    "streaming-data-engineer": (
        "Streaming Data Engineer, Paystack (2020 – present) — Lagos",
        "Backend Engineer, Interswitch (2016 – 2020) — Lagos",
        "Kafka, SQL, Python, lag, exactly-once caveats",
        (
            "Kafka topic for authorize events: partitioning by merchant, lag alert at 30s, and a consumer that is idempotent on event id.",
            "Exactly-once is a sentence in the doc: we are at-least-once plus a unique key. I will not say exactly-once otherwise.",
            "Poison messages on a dead-letter topic with a replay tool. A bad payload does not stall the partition forever.",
        ),
        (
            "HTTP webhooks taught me retries. Streams are retries with order.",
            "Schema registry when a field vanished and the consumer NPE’d.",
        ),
        (
            "Streaming is lag, a unique key, and a dead letter. I do not sell exactly-once I do not have.",
            "I will submit this pack myself.",
        ),
    ),
    "cybersecurity-analyst": (
        "Cybersecurity Analyst, a Nigerian bank (2019 – present) — Lagos",
        "SOC L1, MSSP shift work (2016 – 2019) — Lagos",
        "SIEM, MITRE ATT&CK, ticketing, containment, log analysis",
        (
            "Mapped detections to ATT&CK. A “malware” page without a technique was rewritten or deleted.",
            "Contained a workstation that beaconed: isolate, image, ticket. The user got a loaner, not a lecture only.",
            "Weekly false-positive review. Rules that never caught truth lost their page.",
        ),
        (
            "L1: first 15 minutes are triage, not a novel. I wrote the 15-minute card.",
            "Escalated with the last 20 log lines, not “please check.”",
        ),
        (
            "Analyst work is the isolate and the technique. I have both on a ticket with a loaner laptop.",
            "I will submit this pack myself.",
        ),
    ),
    "soc-analyst": (
        "SOC Analyst, Interswitch (2018 – present) — Lagos",
        "NOC/SOC hybrid, MainOne (2015 – 2018) — Lagos",
        "SIEM, EDR, playbooks, escalation, packet or log review",
        (
            "12-hour SOC shifts: EDR + SIEM, a playbook for ransomware-like encryption spikes, and a page that names the host.",
            "Packet capture when the SIEM story was not enough. A DNS tunnel was the pcap, not the rule name.",
            "Handover notes the next shift can run. A mystery at 07:00 is a failure of the night notes.",
        ),
        (
            "NOC first: uptime pages. SOC added intent.",
            "Never closed “no further action” without saying what we looked at.",
        ),
        (
            "SOC is the handover and the pcap. I have both on a DNS-tunnel night.",
            "I will submit this pack myself.",
        ),
    ),
    "application-security-engineer": (
        "Application Security Engineer, Paystack (2019 – present) — Lagos",
        "Backend Engineer, Interswitch (2016 – 2019) — Lagos",
        "SAST/DAST, threat modeling, reviews, secrets, OWASP",
        (
            "PR review on the charge API: IDOR, authz, and a secret that almost landed in a test fixture. The fixture uses a fake PAN.",
            "SAST in CI with a baseline. New high findings fail the build; old ones have tickets.",
            "Threat model for webhooks: replay, spoofed IP, and HMAC. The test is a bad signature.",
        ),
        (
            "Wrote the APIs I later reviewed. I still think like an author.",
            "Secret scanning in git. A key in history was rotated, not ignored.",
        ),
        (
            "AppSec is the bad HMAC test and the PAN that is not in the fixture. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "cloud-security-engineer": (
        "Cloud Security Engineer, Flutterwave (2020 – present) — Lagos",
        "Security Engineer, Interswitch (2016 – 2020) — Lagos",
        "IAM, CSPM, network policy, encryption, Terraform",
        (
            "CSPM findings with owners. An open security group that had been “temporary” for 11 months was closed with a change ticket.",
            "IMDSv2 required. A metadata-ssrf story from another company became our control.",
            "KMS: no plaintext secrets in env on the box. The exception list expires.",
        ),
        (
            "On-prem firewalls first. Cloud is the same question with a JSON policy.",
            "Terraform for the guardrails so a console click cannot undo them silently.",
        ),
        (
            "Cloud security is the 11-month temporary SG and IMDSv2. I have closed the first.",
            "I will submit this pack myself.",
        ),
    ),
    "iam-engineer": (
        "IAM Engineer, a Nigerian bank (2019 – present) — Lagos",
        "Windows Administrator, Access Bank — Technology (2016 – 2019) — Lagos",
        "SSO, SAML, OIDC, directory, RBAC, joiner-mover-leaver",
        (
            "Joiner-mover-leaver: HR CSV in the morning, AD/Entra at noon, app groups the same day. A leaver who still had VPN the next morning was a P1.",
            "SAML to two SaaS apps. A clock-skew that broke login was NTP, documented.",
            "RBAC reviews quarterly. Owners attest or the group empties.",
        ),
        (
            "AD groups until they were a swamp. Then a model and an expiry.",
            "MFA for admins on a date we published, not “when we can.”",
        ),
        (
            "IAM is the leaver who still had VPN. I have that P1, and then the same-day disable.",
            "I will submit this pack myself.",
        ),
    ),
    "grc-analyst": (
        "GRC Analyst, a Nigerian payments firm (2019 – present) — Lagos",
        "IT Auditor support, a bank (2016 – 2019) — Lagos",
        "ISO, SOC 2, NIST, audits, risk register, evidence",
        (
            "Control evidence in a folder an auditor can walk: screenshot, config export, dated. A Word doc that says “we do MFA” is not evidence.",
            "Risk register with an owner and a next review. Unowned rows are not risks, they are wishes.",
            "SOC 2 week: I sat with the tester on the access review sample, not a slide.",
        ),
        (
            "Pulled samples for ITGC. Learned the difference between a policy and a log.",
            "Never backdated a screenshot. That is how you lose the letter.",
        ),
        (
            "GRC is the dated export and the owner. I have sat the sample with the tester.",
            "I will submit this pack myself.",
        ),
    ),
    "security-architect": (
        "Security Architect, Interswitch (2020 – present) — Lagos",
        "Security Engineer, a Nigerian bank (2016 – 2020) — Lagos",
        "threat models, patterns, IAM, network, review boards",
        (
            "Pattern: no direct internet from the card zone; a proxy with an allow-list. A new vendor that “needed any:any” was a no.",
            "Review board: I write the decision, not just attend. The decision is in git.",
            "Threat model for a new API: spoof, replay, insider. Controls mapped to tickets, not adjectives.",
        ),
        (
            "Implemented the firewalls I later drew. Architecture without scars is a slide.",
            "Said no to a design and offered a smaller yes.",
        ),
        (
            "Architecture is the written no to any:any. I have that mail.",
            "I will submit this pack myself.",
        ),
    ),
    "qa-engineer": (
        "QA Engineer, Kuda (2019 – present) — Lagos",
        "QA Analyst, Carbon (2016 – 2019) — Lagos",
        "test cases, exploratory testing, defect tracking, APIs",
        (
            "Wrote the transfer cases that include double-tap, kill-app, and ₦ with a comma. Two of those caught production bugs before they shipped.",
            "Exploratory charter on statements: I found a date filter that ignored the user’s timezone. Ticket had steps and a screenshot from a TECNO.",
            "API tests on the status endpoint. A 200 with `failed` in the body is a fail, not a pass.",
        ),
        (
            "Excel cases until they rotted. Then a repo.",
            "Refused to sign UAT when the PIN pad still accepted 0000 on a build.",
        ),
        (
            "QA for money is the comma and the kill-app. I have both as cases that caught bugs.",
            "I will submit this pack myself.",
        ),
    ),
    "sdet": (
        "SDET, Paystack (2020 – present) — Lagos",
        "QA Engineer, Andela (2016 – 2020) — Lagos / remote",
        "Python, pytest, Playwright, CI, APIs",
        (
            "pytest API suite on charges: idempotency replay is a test, not a hope. CI red blocks merge.",
            "Playwright on checkout: a flake we hunted for a week was a race on a toast. We waited on the role, not `sleep(3)`.",
            "Test data factory that does not reuse a live PAN. Fixtures are obvious fakes.",
        ),
        (
            "Manual first, then automated the path that broke twice.",
            "Owned the pipeline that other QAs run. If it is red, it is my red.",
        ),
        (
            "SDET is the replay test and no `sleep(3)`. I have both in CI.",
            "I will submit this pack myself.",
        ),
    ),
    "test-automation-engineer": (
        "Test Automation Engineer, Kuda (2019 – present) — Lagos",
        "QA Engineer, Cowrywise (2016 – 2019) — Lagos",
        "Playwright, Cypress, CI, page objects, flake hunting",
        (
            "Playwright suite for onboarding: page objects, and a flake dashboard. A test that failed 8% was quarantined or fixed, not ignored.",
            "CI on every PR. A skipped test needs a ticket id in the name.",
            "Mobile web on a 360px profile. A button that overflowed off the transfer CTA was a fail.",
        ),
        (
            "Cypress until Playwright fit the stack better. I still know both traces.",
            "Never committed a test that only passed on my laptop’s timezone.",
        ),
        (
            "Automation is the 8% flake we either fixed or quarantined. I have the dashboard.",
            "I will submit this pack myself.",
        ),
    ),
    "performance-engineer": (
        "Performance Engineer, Paystack (2020 – present) — Lagos",
        "Backend Engineer, Interswitch (2016 – 2020) — Lagos",
        "k6, metrics, profiling, SLAs, reports",
        (
            "k6 on the authorize path: p95 budget 300ms at a stated RPS. We missed it, found the N+1, then met it.",
            "Report with the command, the version, and the environment. A “looks fine on my machine” is not a report.",
            "Soak test overnight. A leak that only showed at hour 6 is in the graph.",
        ),
        (
            "APIs without budgets. I learned to write the number first.",
            "Profilers on a single process before blaming the network.",
        ),
        (
            "Performance is the overnight leak and the command in the report. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "qa-analyst": (
        "QA Analyst, Flutterwave (2019 – present) — Lagos",
        "UAT Analyst, a Nigerian bank (2016 – 2019) — Lagos",
        "test plans, UAT, regression, tickets, product sense",
        (
            "UAT for a new payout corridor: cases signed by ops, not only engineering. A missing field on the bank file failed UAT on purpose.",
            "Regression pack before each release. I will not “test the happy path only” on money.",
            "Tickets with expected vs actual and environment. A “it doesn’t work” ticket bounced.",
        ),
        (
            "Bank UAT: sign-off is a date and a name. I kept both.",
            "Sat with a merchant on a call and reproduced, then wrote the steps.",
        ),
        (
            "QA analysis is the corridor file that failed UAT on purpose. That is a pass for quality.",
            "I will submit this pack myself.",
        ),
    ),
    "solutions-architect": (
        "Solutions Architect, Interswitch (2020 – present) — Lagos",
        "Technical Architect, a Lagos SI (2016 – 2020)",
        "system design, integration, cloud, trade-off writeups, reviews",
        (
            "Wrote the design that got built: ISO-ish posting to a REST adapter, timeouts, and who retries. The diagram matches production.",
            "Trade-off: duplicate-detect in the adapter vs in the core. We picked the core and wrote why.",
            "Review: I sat with the engineers through the first outage of that design and updated the doc.",
        ),
        (
            "Drew pictures that became tickets. If there is no ticket, it is not a design.",
            "Said no to a vendor box we did not need.",
        ),
        (
            "Solutions architecture is the design that survived the first outage. I have the updated doc.",
            "I will submit this pack myself.",
        ),
    ),
    "software-architect": (
        "Software Architect, Paystack (2020 – present) — Lagos",
        "Senior Backend Engineer, Paystack (2016 – 2020) — Lagos",
        "design docs, APIs, domain modeling, reviews, evolution",
        (
            "Bounded context for charges vs payouts. A team that wanted to join them in one table had to read the doc first — then they did not.",
            "API compatibility: additive changes only. A field removal needs a version.",
            "RFC process: I still write the comment that asks for the failure mode.",
        ),
        (
            "Shipped the services I later split. Architecture without scars is theory.",
            "Code review on the module boundaries, not the commas.",
        ),
        (
            "Software architecture is the table we refused to join. I have that mail.",
            "I will submit this pack myself.",
        ),
    ),
    "cloud-architect": (
        "Cloud Architect, Flutterwave (2020 – present) — Lagos",
        "AWS Engineer, Paystack (2016 – 2020) — Lagos",
        "AWS, networking, IAM, cost, landing zones",
        (
            "Landing zone: org, guardrails, no public S3 at the SCP. A sandbox account that bypassed it was pulled back.",
            "Cost: unit economics per million charges. A NAT gateway we did not need left the bill.",
            "Network: shared services VPC and spokes. A flat VPC proposal was a no.",
        ),
        (
            "Built the first accounts by hand, then encoded them.",
            "Still on-call when the design page is wrong. Then the page changes.",
        ),
        (
            "Cloud architecture is the SCP and the NAT we deleted. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "enterprise-architect": (
        "Enterprise Architect, a Nigerian bank (2019 – present) — Lagos",
        "Solutions Architect, Interswitch (2015 – 2019) — Lagos",
        "capability maps, integration, standards, governance, roadmaps",
        (
            "Capability map for payments vs channels vs core. A project that rebuilt a capability we already had was stopped at architecture review.",
            "Standard: REST + HMAC for new internal APIs. SOAP only where a regulator still demands it, with an expiry.",
            "Roadmap on one page the EXCO can reject. A 40-slide deck is not a roadmap.",
        ),
        (
            "Integration diagrams that named the owner of each box.",
            "Learned that governance without a no is a newsletter.",
        ),
        (
            "Enterprise architecture is the duplicate project we stopped. I have the review minute.",
            "I will submit this pack myself.",
        ),
    ),
    "technical-architect": (
        "Technical Architect, Andela (2020 – present) — remote",
        "Lead Engineer, a Lagos product team (2016 – 2020)",
        "design, spikes, NFRs, reviews, delivery",
        (
            "Spike: two days on a queue vs a table. We picked the table, with the numbers in the writeup.",
            "NFRs in the story: p95, RPO, who is on-call. A story without them bounced.",
            "Sat in the standup until the design was in the code, then left.",
        ),
        (
            "Led a squad that shipped weekly. Architecture that cannot ship is a hobby.",
            "Pair-programmed the first adapter so the pattern existed in git.",
        ),
        (
            "Technical architecture is the two-day spike and the NFR on the story. I bounce stories without them.",
            "I will submit this pack myself.",
        ),
    ),
    "integration-architect": (
        "Integration Architect, Interswitch (2019 – present) — Lagos",
        "Backend Engineer, SystemSpecs (2015 – 2019) — Lagos",
        "APIs, events, contracts, failure modes, iPaaS",
        (
            "Contract: timeout, retry, idempotency key. A bank that retried without a key double-posted until we made the key mandatory.",
            "Event vs API: settlement is a file; authorize is an API. Mixing them was a design we unwound.",
            "Failure: poison message, DLQ, replay runbook. I have replayed a day without double-credit.",
        ),
        (
            "Wrote the adapters. Then drew them.",
            "SOAP where we had to; REST where we could. The map is dated.",
        ),
        (
            "Integration is the mandatory idempotency key after a double-post. I have that incident.",
            "I will submit this pack myself.",
        ),
    ),
    "it-support-specialist": (
        "IT Support Specialist, Access Bank — Technology (2018 – present) — Lagos",
        "Help Desk, a Lagos insurer (2015 – 2018)",
        "Windows, identity, imaging, remote tools, customer notes",
        (
            "Closed 30+ tickets a day with notes another tech can follow: what I tried, what worked, asset tag.",
            "Imaged laptops with the standard image. A “just install it” request that broke BitLocker was a lesson I documented.",
            "Escalated with evidence. A “network is slow” that was a 100% disk on the PC did not go to the network team.",
        ),
        (
            "Password resets until I automated the ones policy allowed.",
            "Walked floors. Some tickets die when you look at the cable.",
        ),
        (
            "Support is the asset tag and the disk that was the “network.” I have both in tickets.",
            "I will submit this pack myself.",
        ),
    ),
    "help-desk-technician": (
        "Help Desk Technician, MainOne (2018 – present) — Lagos",
        "Service Desk, a call-centre IT team (2015 – 2018) — Lagos",
        "ticketing, passwords, hardware, SOP, remote support",
        (
            "First-line SLA: 15 minutes to first response on P2. I missed it twice in a year; both are in the report.",
            "SOP for VPN: the screenshot is the current client, not last year’s.",
            "Remote session that did not leave a tool running as admin. I check after disconnect.",
        ),
        (
            "Phones and a queue. Tone matters. I still write the steps as if the user is tired.",
            "Never asked for a password in chat. That was a firing offence we meant.",
        ),
        (
            "Help desk is the SLA I missed twice and the VPN SOP that matches the client. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "desktop-support": (
        "Desktop Support, GTBank — Technology (2018 – present) — Lagos",
        "Field Tech, an OEM partner (2015 – 2018) — Lagos",
        "Windows, macOS, imaging, hardware, MDM, on-site",
        (
            "On-site swap: failed disk, image, BitLocker recovery key from the escrow, user back in under two hours.",
            "MDM (Intune/similar): a device that left the building lost email. The user was told before it happened.",
            "Hardware: I keep a spare dock count. “We’ll order it” is not a fix for a trading floor.",
        ),
        (
            "Broke and replaced screens in the field. Warranty tickets with serials.",
            "macOS and Windows. The runbook is two columns.",
        ),
        (
            "Desktop support is the recovery key and the spare dock. I have restored BitLocker on a trading-floor deadline.",
            "I will submit this pack myself.",
        ),
    ),
    "it-operations-engineer": (
        "IT Operations Engineer, Interswitch (2019 – present) — Lagos",
        "Sysadmin, SystemSpecs (2015 – 2019) — Lagos",
        "monitoring, change, backups, identity, on-call",
        (
            "Change: CAB for prod, a back-out, and a window. A “quick fix” without a ticket is how we got a six-hour outage; we do not do that now.",
            "Backup restore tested quarterly. The last restore was a file share, timed, signed.",
            "On-call rota with a handoff. A mystery at 08:00 is a failed night.",
        ),
        (
            "Patched and monitored. Ops is the calendar, not the heroics.",
            "Identity tickets until they had an expiry.",
        ),
        (
            "IT ops is the restore we signed and the quick fix we banned. I have both stories.",
            "I will submit this pack myself.",
        ),
    ),
    "it-manager": (
        "IT Manager, a Lagos mid-market firm (2019 – present)",
        "IT Operations Lead, Access Bank — Technology (2015 – 2019) — Lagos",
        "people, vendors, SLAs, change, reporting",
        (
            "Team of six: hiring, 1:1s, and a rota that does not burn the same two people.",
            "Vendor SLA for the ISP and the laptop OEM. A missed SLA is a credit we actually claimed.",
            "Monthly to the business: incidents, patch %, and one number they can argue with.",
        ),
        (
            "Led ops before I managed. I still take a shift when we are short.",
            "Fired a vendor with the email trail. Soft nos waste a year.",
        ),
        (
            "IT management is the credit we claimed and the rota that is fair. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "technical-project-manager": (
        "Technical Project Manager, Interswitch (2019 – present) — Lagos",
        "Delivery Lead, a Lagos SI (2016 – 2019)",
        "plans, risks, vendors, engineering partners, status that was true",
        (
            "Core-to-channel cutover: a plan with a kill switch, a weekend, and a status mail that said we were amber when we were amber.",
            "Risk log with owners. A risk without an owner is a wish.",
            "Vendors on the critical path had a named deputy. One no-show did not kill the window.",
        ),
        (
            "Tracked engineering work without pretending I could write the code.",
            "Never greened a status to please a steering group.",
        ),
        (
            "TPM work is the amber mail and the kill switch. I have sent both.",
            "I will submit this pack myself.",
        ),
    ),
    "scrum-master": (
        "Scrum Master, Andela (2019 – present) — remote",
        "Delivery coordinator, a Lagos product team (2016 – 2019)",
        "facilitation, impediments, metrics you did not game, delivery",
        (
            "Board matched git. A “done” ticket without a merged PR was moved back in the room, not later.",
            "Impediments had owners and dates. A lingering blocker was a 1:1, not a standup performance.",
            "Velocity used for forecast, not for beating people. I stopped a chart that was becoming a weapon.",
        ),
        (
            "Facilitated, then checked the merge. Theatre is easy; the merge is the truth.",
            "Worked with a team that shipped weekly. That is the metric I kept.",
        ),
        (
            "Scrum is the ticket that went back because there was no merge. I moved it in the room.",
            "I will submit this pack myself.",
        ),
    ),
    "solutions-engineer": (
        "Solutions Engineer, Paystack (2020 – present) — Lagos",
        "Support Engineer, Interswitch (2016 – 2020) — Lagos",
        "demos, architecture talks, APIs, POCs",
        (
            "POC that ran on the prospect’s test keys: a charge, a webhook, a refund. A slide deck is not a POC.",
            "Unblocked a go-live: their HMAC clock was 7 minutes off. We documented NTP, they launched.",
            "Said no to a custom flow we could not support. They bought the standard path.",
        ),
        (
            "Support tickets taught me the real failure modes. Demos now include the failure.",
            "Wrote the internal note so product heard the same story.",
        ),
        (
            "Solutions engineering is the POC on their keys and the NTP catch. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "sales-engineer": (
        "Sales Engineer, Flutterwave (2020 – present) — Lagos",
        "Solutions Engineer, Interswitch (2016 – 2020) — Lagos",
        "product, objections, POCs, RFPs, the stack you showed",
        (
            "RFP answers I could defend on a call. A copied paragraph that was not true did not go out.",
            "Live demo on a bad hotel wifi. The retry UI was the feature that day.",
            "Scoped a deal down so we could win without a six-month custom.",
        ),
        (
            "Technical pre-sales with a working sandbox, not a recording only.",
            "Lost a deal by telling the truth about a gap. I still sleep.",
        ),
        (
            "Sales engineering is the RFP line I would say on a call. I delete the rest.",
            "I will submit this pack myself.",
        ),
    ),
    "technical-writer": (
        "Technical Writer, Paystack (2019 – present) — Lagos",
        "Engineer who wrote the docs, Andela (2016 – 2019) — remote",
        "docs-as-code, APIs, tutorials, review with the team that ships",
        (
            "Docs in the same PR as the API change. A field rename without a docs diff failed CI.",
            "Tutorial that a new merchant completed without Slack. I watched a recording of the first stranger.",
            "Deprecation notice with a date. A silent removal is a bug in the docs.",
        ),
        (
            "Wrote runbooks as an engineer. Then made it my job.",
            "Rejected screenshots of a staging URL that would 404.",
        ),
        (
            "Technical writing is the PR that fails without a docs diff. I have that check.",
            "I will submit this pack myself.",
        ),
    ),
    "developer-advocate": (
        "Developer Advocate, Paystack (2020 – present) — Lagos / remote",
        "Backend Engineer, Paystack (2016 – 2020) — Lagos",
        "samples, talks, GitHub, the product you actually used",
        (
            "Sample repo that still runs: a charge, a webhook, a test. A broken sample is a P1 on my board.",
            "Talk with a live demo that failed once; the backup was a recorded happy path plus the error on screen. Honesty landed.",
            "Filed issues on our own SDK and fixed two of them. Advocacy without the repo is marketing.",
        ),
        (
            "Shipped the API I later explained. I still read the changelog before a talk.",
            "Office hours with merchants. The notes went to product the same day.",
        ),
        (
            "DevRel is the sample that still runs and the SDK issue I filed. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "it-auditor": (
        "IT Auditor, a Nigerian bank (2019 – present) — Lagos",
        "ITGC tester, Big Four secondment (2016 – 2019) — Lagos",
        "ITGC, sampling, evidence, SOX or CBN, writeups",
        (
            "Access sample: 25 joiners, 25 leavers. A leaver with active AD was a finding with the screenshot dated.",
            "Change sample: ticket, approval, back-out. A prod change without a ticket was severity high.",
            "Writeup that named the control, the exception, and the owner. Adjectives were edited out.",
        ),
        (
            "Pulled evidence for someone else’s tests. Learned speed without skipping the date on the screenshot.",
            "Never accepted a policy as operating effectiveness.",
        ),
        (
            "Audit is the leaver still in AD and the dated screenshot. I have that finding.",
            "I will submit this pack myself.",
        ),
    ),
    "database-administrator": (
        "Database Administrator, Interswitch (2018 – present) — Lagos",
        "SQL Developer, a Nigerian bank (2015 – 2018) — Lagos",
        "SQL, backups, replication, permissions, incident recovery",
        (
            "SQL Server / Postgres: nightly backup plus a restore to a side instance every month. The restore is the job.",
            "Replication lag page. A replica that was 40 minutes behind was a P2, not “async is fine.”",
            "Permissions: no db_owner for app logins. A grant that snuck in was revoked with a ticket.",
        ),
        (
            "Wrote the queries I later indexed. DBA without SQL is a button-clicker.",
            "Incident: a full disk on the log drive. I still check that first.",
        ),
        (
            "DBA work is the monthly restore and the 40-minute lag. I have paged on both.",
            "I will submit this pack myself.",
        ),
    ),
    "postgresql-dba": (
        "PostgreSQL DBA, Paystack (2019 – present) — Lagos",
        "Database Engineer, Flutterwave (2016 – 2019) — Lagos",
        "PostgreSQL, replication, EXPLAIN, backups, extensions",
        (
            "Primary + replica: lag monitor, and a failover drill that the app survived because we tested connection retry.",
            "EXPLAIN (ANALYZE, BUFFERS) on a charge lookup. A seq scan on a growing table became an index in the same week.",
            "pg_dump + WAL. A restore test recovered to a named time, not “last night.”",
        ),
        (
            "Vacuum and bloat. A table that never got vacuumed was a 3 a.m. page once.",
            "Extensions pinned. A surprise version in prod is a finding.",
        ),
        (
            "Postgres is the failover the app survived and the seq scan we indexed. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "oracle-dba": (
        "Oracle DBA, a Nigerian bank (2018 – present) — Lagos",
        "Oracle Developer, an SI (2015 – 2018) — Lagos",
        "Oracle, RMAN, Data Guard, performance, patching",
        (
            "Data Guard: switchover drill with the app team. A lag that was “normal” until it was not has a number now.",
            "RMAN restore to a cloned host. The tape that “had the backup” and did not is a story I tell in CAB.",
            "SQL tuning: a bind-peek surprise. The fix was a baseline, not a hint forever.",
        ),
        (
            "Wrote PL/SQL. Then I had to keep it running.",
            "Patch cycles with a back-out. We used the back-out once.",
        ),
        (
            "Oracle is the restore that proved the tape was empty. I have that CAB note.",
            "I will submit this pack myself.",
        ),
    ),
    "salesforce-developer": (
        "Salesforce Developer, a Lagos enterprise programme (2019 – present)",
        "CRM Developer, an SI (2016 – 2019) — Lagos",
        "Apex, Lightning, SOQL, flows, deployment",
        (
            "Apex trigger that does not query in a loop. A bulk load of 200 leads used to time out; it does not.",
            "Deploy via pipelines, not change sets from a laptop on Friday.",
            "SOQL with selective filters. A report that scanned everything was rewritten with the architect.",
        ),
        (
            "Flows until they hid logic. Then Apex with tests.",
            "Never shipped without a test that used `seeAllData=false`.",
        ),
        (
            "Salesforce is the bulk 200 and the pipeline deploy. I do not Friday-change-set.",
            "I will submit this pack myself.",
        ),
    ),
    "sap-technical-consultant": (
        "SAP Technical Consultant, a Nigerian bank programme (2018 – present) — Lagos",
        "ABAP Developer, an SI (2015 – 2018) — Lagos",
        "ABAP, Basis coordination, transports, the module you touched",
        (
            "ABAP exits on a payments-related module: transports through QA, and a dump I fixed before PRD.",
            "Partnered with Basis on the window. A transport without a back-out partner did not go.",
            "Documented the user-exit so the next consultant did not reverse-engineer it from a dump.",
        ),
        (
            "Reports and interfaces. Then the dump at 2 a.m.",
            "Never transported untested to PRD because “the business is waiting.” They wait for a dump longer.",
        ),
        (
            "SAP technical work is the transport with a partner and the dump we caught in QA. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "erp-developer": (
        "ERP Developer, SystemSpecs (2018 – present) — Lagos",
        "Application Developer, an SI (2015 – 2018) — Lagos",
        "ERP customizations, integrations, testing, the product name",
        (
            "Custom posting in Remita-adjacent flows: test company code, a reversal, and a recon that matched.",
            "Integration file to a bank: encoding, line endings, and a reject we could explain.",
            "Release notes the ops team used. A silent field was a bug.",
        ),
        (
            "Configured before I customized. Custom was the last resort.",
            "Sat with recon. If they cannot match, I am not done.",
        ),
        (
            "ERP is the recon that matched and the reject we could explain. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "servicenow-developer": (
        "ServiceNow Developer, a Lagos enterprise (2019 – present)",
        "ITSM Analyst, a bank (2016 – 2019) — Lagos",
        "JavaScript, Flow Designer, ITSM, update sets, CMDB",
        (
            "Catalog item with a flow that assigns and SLA-clocks. A flow that emailed everyone was rewritten to a group.",
            "Update sets in order. A skipped set that broke prod is a story I use in review.",
            "CMDB: a server CI without an owner is not a CI. We stopped pretending.",
        ),
        (
            "Tickets before I automated them. The pain is the spec.",
            "Never cloned a flow I did not understand.",
        ),
        (
            "ServiceNow is the skipped update set. I have that review story.",
            "I will submit this pack myself.",
        ),
    ),
    "microsoft-365-administrator": (
        "Microsoft 365 Administrator, Access Bank — Technology (2019 – present) — Lagos",
        "Windows Administrator, GTBank — Technology (2016 – 2019) — Lagos",
        "Entra ID, Exchange, Intune, SharePoint, Conditional Access",
        (
            "Conditional Access: MFA for all, legacy auth blocked, and a break-glass we tested.",
            "Intune: a lost phone wiped mail. The user was in the SOP before the loss.",
            "Exchange: transport rule that stopped a PAN-shaped string leaving the tenant. It fired on a real mail.",
        ),
        (
            "AD and file shares. Then the cloud copy of the same fights.",
            "SharePoint permissions until they matched the org chart, roughly.",
        ),
        (
            "M365 is the wipe SOP and the PAN rule that fired. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "embedded-engineer": (
        "Embedded Engineer, a Lagos OEM partner (2018 – present)",
        "Firmware intern-to-engineer, same shop (2015 – 2018)",
        "C, RTOS, peripherals, debugging, schematics",
        (
            "C on an MCU: UART to a modem, a watchdog that actually bit, and a brown-out we reproduced on the bench.",
            "Schematic next to the code. A pin that was not what the net name said was a day of my life.",
            "Release: hex + git tag. A “latest.bin” on a USB stick is not a release.",
        ),
        (
            "Brought up the first board with a scope and a coffee.",
            "Never shipped a busy-wait that made the watchdog a liar.",
        ),
        (
            "Embedded is the watchdog that bit and the pin that lied. I have both on a bench.",
            "I will submit this pack myself.",
        ),
    ),
    "firmware-engineer": (
        "Firmware Engineer, a device team in Lagos (2018 – present)",
        "Embedded Engineer, OEM partner (2015 – 2018)",
        "C, bootloaders, hardware bring-up, test jigs, versioning",
        (
            "Bootloader + app split: a bad app cannot brick the loader. We tested that by flashing garbage on purpose.",
            "Test jig that presses the button 1,000 times. A hang at 400 is a finding.",
            "Version in a register the host can read. “Which firmware?” is not a Slack poll.",
        ),
        (
            "Wrote the first UART hello. Then the rest.",
            "Scope traces in the ticket. Photos of LEDs are not traces.",
        ),
        (
            "Firmware is flashing garbage on purpose and still booting the loader. I have that test.",
            "I will submit this pack myself.",
        ),
    ),
    "iot-engineer": (
        "IoT Engineer, a Lagos telemetry project (2019 – present)",
        "Embedded Engineer, OEM partner (2016 – 2019)",
        "MQTT, firmware, cloud ingest, OTA, hardware constraints",
        (
            "MQTT to a broker with TLS and a device cert. A shared password for all devices was a no.",
            "OTA with dual banks. A failed image rolled back. We forced a fail in staging.",
            "Field: a unit in Ibadan that only came on at night. The log rotated; we still had the last 2 KB.",
        ),
        (
            "Firmware first. Cloud later. The device still has to boot.",
            "Power budget on a spreadsheet that matched the current draw.",
        ),
        (
            "IoT is dual-bank OTA and a 2 KB log from Ibadan. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "gameplay-programmer": (
        "Gameplay Programmer, a Lagos/remote studio (2019 – present)",
        "Gameplay Engineer, student and contract titles (2016 – 2019)",
        "C#, Unity, gameplay, debugging, shipping a build",
        (
            "Unity: a combat loop that stayed at 30fps on a mid Android. A spike was a GC we moved off Update.",
            "Netcode for a 2-player mode: predicted input, a reconcile that did not rubber-band on 150ms.",
            "Shipped a build to a store. Review notes and a version that old saves could load.",
        ),
        (
            "Prototypes that died. The ones that shipped had a frame budget written down.",
            "Debugged a save that vanished on kill-app. It was a flush we skipped.",
        ),
        (
            "Gameplay is the GC spike and the save that survived kill-app. I have both on a shipped build.",
            "I will submit this pack myself.",
        ),
    ),
    "graphics-engineer": (
        "Graphics Engineer, a remote studio (2020 – present)",
        "Engine programmer, contract (2016 – 2020)",
        "C++, shaders, GPU, profiling, the engine",
        (
            "Frame budget: 16.6ms. A pass that was 4ms on PC and 11ms on the target phone was the one we cut.",
            "Shader variants that exploded compile time. We capped them and measured.",
            "Profiler captures in the ticket, not “it feels smoother.”",
        ),
        (
            "Wrote a blit and a debug overlay. Then the real passes.",
            "Never shipped a pink shader as “placeholder” in a store build.",
        ),
        (
            "Graphics is the 11ms pass we cut and the capture in the ticket. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "blockchain-engineer": (
        "Blockchain Engineer, Nethermind (2019 – present) — remote",
        "Backend Engineer, Paystack (2016 – 2019) — Lagos",
        "Solidity, testing, wallets, audits, nodes",
        (
            "Contracts + a node we ran: a mainnet tx, a test on a fork, and an audit finding we retested.",
            "Wallet integration: wrong chain id is a user-visible error.",
            "Did not treat mempool as final. Payments work taught me that before chains did.",
        ),
        (
            "Idempotent APIs. Then logs on a chain.",
            "Read other people’s post-mortems before writing bytecode.",
        ),
        (
            "Blockchain engineering is the fork test and the chain-id error. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "gis-engineer": (
        "GIS Engineer, a Lagos mapping project (2019 – present)",
        "Data Engineer, a utilities client (2016 – 2019) — Lagos",
        "PostGIS, QGIS, Python, projections, tiles",
        (
            "PostGIS: a projection mistake that put a road 200m off. The ticket is the SRID.",
            "Tile pipeline that rebuilt overnight. A missing zoom was a 404 we monitored.",
            "QGIS project in git. A shapefile that only lived on a laptop was imported or deleted.",
        ),
        (
            "CSV of coordinates until they lied. Then a real CRS.",
            "Field GPS vs the map. The map lost until we proved otherwise.",
        ),
        (
            "GIS is the SRID that was wrong by 200m. I have that ticket.",
            "I will submit this pack myself.",
        ),
    ),
    "hpc-engineer": (
        "HPC Engineer, a research cluster (2019 – present) — remote / Lagos",
        "Linux Administrator, a university lab (2016 – 2019)",
        "Linux, schedulers, MPI, storage, performance",
        (
            "Slurm (or similar): fair share, a stuck job we drained, and a node that failed health and left the pool.",
            "MPI job that did not scale past 32 ranks until we found the allreduce. The plot is in the ticket.",
            "Scratch vs archive. A full scratch that killed a 3-day job is why the quota exists.",
        ),
        (
            "Linux first. The scheduler is a way to share it.",
            "Never ran as root on compute. That was a ban.",
        ),
        (
            "HPC is the 3-day job killed by a full scratch. The quota is the product.",
            "I will submit this pack myself.",
        ),
    ),
    "robotics-engineer": (
        "Robotics Engineer, a Lagos/remote robotics group (2019 – present)",
        "Embedded Engineer, OEM partner (2016 – 2019)",
        "ROS, C++, Python, sensors, control",
        (
            "ROS nodes: a driver for a lidar that dropped packets on a bad USB; the bag file is the proof.",
            "Control loop rate measured, not hoped. A 50Hz loop that was 18Hz on the NUC was a scheduling issue.",
            "Sim + real. A policy that only worked in Gazebo was not a demo.",
        ),
        (
            "Firmware on the actuator. Then the node.",
            "E-stop that actually cut power. A software e-stop only is a finding.",
        ),
        (
            "Robotics is the bag file and the 18Hz loop. I have both.",
            "I will submit this pack myself.",
        ),
    ),
    "ux-engineer": (
        "UX Engineer, Kuda (2020 – present) — Lagos",
        "Frontend Engineer, Cowrywise (2016 – 2020) — Lagos",
        "HTML, CSS, JS, accessibility, design system",
        (
            "Design-system buttons with all states, including disabled during a charge. A designer’s Figma that missed disabled was a ticket both ways.",
            "Token pipeline: colour change in one file. A hex that was copied 40 times was the old world.",
            "Reviewed PRs for focus rings. A `outline: none` without a replacement failed review.",
        ),
        (
            "Built screens, then the library those screens should have used.",
            "Sat in usability on a cheap phone. The library changed.",
        ),
        (
            "UX engineering is the disabled charge button and the banned `outline: none`. I have both in the system.",
            "I will submit this pack myself.",
        ),
    ),
    "accessibility-engineer": (
        "Accessibility Engineer, a Lagos product team (2020 – present)",
        "Frontend Engineer, Kuda (2016 – 2020) — Lagos",
        "WCAG, screen readers, ARIA, audits, engineering partners",
        (
            "NVDA/VoiceOver pass on the transfer flow. A live region that did not announce “failed” was a P1.",
            "Audit with issues, WCAG refs, and a PR. A PDF of scores without tickets is not an audit.",
            "Colour contrast tokens. A grey on grey that passed on a Mac and failed in sunlight was recoded.",
        ),
        (
            "Frontend first. Then the audits.",
            "Never added ARIA to a native button that already had a name.",
        ),
        (
            "Accessibility is the live region for “failed” and the ticket, not a score PDF. I have the P1.",
            "I will submit this pack myself.",
        ),
    ),
    "fintech-engineer": (
        "FinTech Engineer, Paystack (2019 – present) — Lagos",
        "Backend Engineer, Interswitch (2016 – 2019) — Lagos",
        "backend, SQL, idempotency, audit logs, ledger path",
        (
            "Ledger row for a charge: immutable after post, reversal is a new row. A update-in-place was a design we rejected.",
            "Idempotency key on the API and a unique constraint. A double-click is one row.",
            "Audit log that a recon team can read without me. If they Slack me for every line, the log failed.",
        ),
        (
            "Switching APIs. Same money, older protocols.",
            "Learned kobo integers before I learned frameworks.",
        ),
        (
            "Fintech is the immutable row and the unique key. I have rejected update-in-place.",
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

