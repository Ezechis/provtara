from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoleTemplate:
    id: str
    title: str
    family: str
    focus: str
    tools: str


FAMILY_ORDER = (
    "Networking & infrastructure",
    "Programming",
    "Mobile",
    "DevOps & cloud",
    "AI / ML",
    "Data",
    "Security",
    "Quality",
    "Architecture",
    "IT operations",
    "Databases & enterprise",
    "Specialized",
)

# family, title, focus, typical tools (hints — never copy onto a résumé unearned)
_RAW: tuple[tuple[str, str, str, str], ...] = (
    (
        "Networking & infrastructure",
        "Network Engineer",
        "routing, switching, and the paths packets actually take",
        "TCP/IP, BGP, OSPF, VLANs, Cisco or Juniper, Wireshark, firewalls",
    ),
    (
        "Networking & infrastructure",
        "Network Administrator",
        "day-to-day LAN/WAN health, access, and documentation",
        "switching, DHCP, DNS, VPNs, monitoring, ticketing",
    ),
    (
        "Networking & infrastructure",
        "Network Security Engineer",
        "segmentation, perimeter, and what is allowed on the wire",
        "firewalls, IDS/IPS, VPNs, Zero Trust, packet capture",
    ),
    (
        "Networking & infrastructure",
        "Wireless Network Engineer",
        "RF coverage, capacity, and roaming that holds up",
        "Wi-Fi 6, controllers, site surveys, RADIUS, spectrum analysis",
    ),
    (
        "Networking & infrastructure",
        "NOC Engineer",
        "shift work that keeps services up and incidents honest",
        "monitoring, SNMP, escalation, runbooks, incident comms",
    ),
    (
        "Networking & infrastructure",
        "Telecommunications Engineer",
        "voice, circuits, and carrier handoffs",
        "VoIP, SIP, PBX, MPLS, SD-WAN, circuit provisioning",
    ),
    (
        "Networking & infrastructure",
        "Systems Administrator",
        "servers, identity, and the box staying up",
        "Linux or Windows Server, Active Directory, backups, patching, DNS",
    ),
    (
        "Networking & infrastructure",
        "Linux Administrator",
        "Linux estates you can boot, patch, and recover",
        "RHEL or Ubuntu, systemd, bash, SSH, LVM, SELinux",
    ),
    (
        "Networking & infrastructure",
        "Windows Administrator",
        "Windows Server and the directory that authenticates people",
        "Active Directory, GPO, PowerShell, Hyper-V, DNS, DHCP",
    ),
    (
        "Networking & infrastructure",
        "Storage Engineer",
        "capacity, latency, and data that is still there after a failure",
        "SAN, NAS, NFS, iSCSI, snapshots, replication",
    ),
    (
        "Networking & infrastructure",
        "Virtualization Engineer",
        "hypervisors and the guests that depend on them",
        "VMware, Hyper-V, KVM, vCenter, HA, capacity planning",
    ),
    (
        "Programming",
        "Backend Engineer",
        "APIs, data stores, and services that stay correct under load",
        "Python, Java, Go, SQL, REST or gRPC, Docker",
    ),
    (
        "Programming",
        "Frontend Engineer",
        "interfaces people can actually use, measured in the browser",
        "HTML, CSS, JavaScript, TypeScript, React or Vue, accessibility",
    ),
    (
        "Programming",
        "Full-Stack Engineer",
        "a vertical slice from the UI to the store",
        "TypeScript, React, Node or Django, SQL, HTTP, Git",
    ),
    (
        "Programming",
        "Python Developer",
        "Python in production — services, scripts, or data paths you ran",
        "Python, pytest, packaging, SQL, REST, Linux",
    ),
    (
        "Programming",
        "Java Developer",
        "JVM services you shipped and operated",
        "Java, Spring, SQL, Maven or Gradle, testing, HTTP",
    ),
    (
        "Programming",
        "JavaScript Developer",
        "JavaScript in the browser or on the server that you own",
        "JavaScript, Node.js, npm, testing, HTTP, Git",
    ),
    (
        "Programming",
        "TypeScript Developer",
        "typed JavaScript you compiled and shipped",
        "TypeScript, Node.js, React, testing, REST, Git",
    ),
    (
        "Programming",
        "Go Developer",
        "Go services that compile, run, and fail loudly",
        "Go, gRPC or REST, SQL, Docker, concurrency, testing",
    ),
    (
        "Programming",
        "Rust Developer",
        "Rust where safety or performance was the point",
        "Rust, cargo, systems APIs, testing, Linux",
    ),
    (
        "Programming",
        "C / C++ Developer",
        "native code you built, debugged, and shipped",
        "C, C++, CMake, debugging, memory, Linux or embedded",
    ),
    (
        "Programming",
        "C# .NET Developer",
        ".NET services or apps you put in front of users",
        "C#, .NET, ASP.NET, SQL Server, testing, Azure or IIS",
    ),
    (
        "Programming",
        "PHP Developer",
        "PHP applications you maintained in production",
        "PHP, Laravel or Symfony, MySQL, HTTP, testing",
    ),
    (
        "Programming",
        "Ruby Developer",
        "Ruby on Rails or services you actually ran",
        "Ruby, Rails, PostgreSQL, Sidekiq, testing, HTTP",
    ),
    (
        "Programming",
        "Scala Developer",
        "Scala on the JVM for data or services you shipped",
        "Scala, Akka or Spark, JVM, testing, SQL",
    ),
    (
        "Programming",
        "Kotlin Developer",
        "Kotlin on the JVM or Android that you released",
        "Kotlin, Spring or Android, coroutines, testing, SQL or Room",
    ),
    (
        "Programming",
        "Node.js Developer",
        "Node services you deployed and watched fail",
        "Node.js, TypeScript, Express or Fastify, SQL, testing, HTTP",
    ),
    (
        "Mobile",
        "iOS Engineer",
        "apps that shipped to the App Store from your hands",
        "Swift, UIKit or SwiftUI, Xcode, REST, TestFlight",
    ),
    (
        "Mobile",
        "Android Engineer",
        "apps that shipped to Play from your hands",
        "Kotlin, Jetpack, Android Studio, REST, Play Console",
    ),
    (
        "Mobile",
        "React Native Engineer",
        "cross-platform apps you released on both stores",
        "React Native, TypeScript, native modules, REST, CI",
    ),
    (
        "Mobile",
        "Flutter Developer",
        "Flutter apps you published, not sample widgets",
        "Dart, Flutter, state management, REST, store release",
    ),
    (
        "Mobile",
        "Mobile Engineer",
        "native or cross-platform clients you put on devices",
        "Swift or Kotlin, REST, offline storage, crash reporting",
    ),
    (
        "DevOps & cloud",
        "DevOps Engineer",
        "the path from commit to production that you built",
        "CI/CD, Docker, Linux, Terraform or Ansible, cloud, Git",
    ),
    (
        "DevOps & cloud",
        "Site Reliability Engineer",
        "error budgets, toil, and systems that stay up",
        "Linux, monitoring, SLO/SLI, incident response, Kubernetes or VMs",
    ),
    (
        "DevOps & cloud",
        "Platform Engineer",
        "internal platforms other engineers actually use",
        "Kubernetes, CI, golden paths, IAM, Terraform, documentation",
    ),
    (
        "DevOps & cloud",
        "Cloud Engineer",
        "cloud accounts you designed, secured, and paid for",
        "AWS or Azure or GCP, IAM, networking, Terraform, observability",
    ),
    (
        "DevOps & cloud",
        "AWS Engineer",
        "AWS services you ran in an account you owned",
        "EC2, IAM, VPC, S3, RDS or DynamoDB, CloudWatch, Terraform",
    ),
    (
        "DevOps & cloud",
        "Azure Engineer",
        "Azure subscriptions you built and operated",
        "Azure, Entra ID, VNets, ARM or Bicep, Monitor, AKS or VMs",
    ),
    (
        "DevOps & cloud",
        "GCP Engineer",
        "GCP projects you provisioned and operated",
        "GCP, IAM, VPC, GKE or Compute, Cloud SQL, Terraform",
    ),
    (
        "DevOps & cloud",
        "Kubernetes Engineer",
        "clusters you stood up, upgraded, and recovered",
        "Kubernetes, kubectl, Helm, networking, RBAC, observability",
    ),
    (
        "DevOps & cloud",
        "Terraform / IaC Engineer",
        "infrastructure as code that applied cleanly more than once",
        "Terraform, state, modules, CI, cloud APIs, policy as code",
    ),
    (
        "DevOps & cloud",
        "CI/CD Engineer",
        "pipelines that build, test, and ship without theatre",
        "GitHub Actions or GitLab CI or Jenkins, artifacts, secrets, Docker",
    ),
    (
        "DevOps & cloud",
        "Observability Engineer",
        "metrics, logs, and traces people use during an incident",
        "Prometheus, Grafana, OpenTelemetry, logging, alerting",
    ),
    (
        "DevOps & cloud",
        "Infrastructure Engineer",
        "the substrate: compute, network, image, and recovery",
        "Linux, networking, images, backups, automation, cloud or DC",
    ),
    (
        "AI / ML",
        "Machine Learning Engineer",
        "models you trained, evaluated, and put behind an interface",
        "Python, PyTorch or TensorFlow, data pipelines, evaluation, serving",
    ),
    (
        "AI / ML",
        "AI Engineer",
        "applied AI in a product, with evals you can point to",
        "Python, APIs, evaluation, retrieval or fine-tuning, production logs",
    ),
    (
        "AI / ML",
        "MLOps Engineer",
        "the path from notebook to a monitored model",
        "Python, CI, model registry, feature store or pipelines, monitoring",
    ),
    (
        "AI / ML",
        "Data Scientist",
        "questions you answered with data, not slides about data",
        "Python, SQL, statistics, notebooks, visualization, experiment design",
    ),
    (
        "AI / ML",
        "NLP Engineer",
        "text systems you trained or shipped",
        "Python, transformers, evaluation, tokenization, serving",
    ),
    (
        "AI / ML",
        "Computer Vision Engineer",
        "vision models or pipelines you ran on real images",
        "Python, OpenCV, PyTorch, datasets, evaluation, deployment",
    ),
    (
        "AI / ML",
        "Applied Scientist",
        "research that became a measured change in a product",
        "Python, statistics, experiments, papers-to-prod, evaluation",
    ),
    (
        "AI / ML",
        "LLM / Applied AI Engineer",
        "language-model features with evals, not prompt folklore",
        "Python, APIs, retrieval, evaluation sets, latency, safety checks",
    ),
    (
        "AI / ML",
        "Research Engineer",
        "experiments you reproduced and productionized",
        "Python, papers, training loops, ablation, code that others ran",
    ),
    (
        "Data",
        "Data Engineer",
        "pipelines that move trusted data on a schedule",
        "SQL, Python, Spark or dbt or Airflow, warehouses, orchestration",
    ),
    (
        "Data",
        "Analytics Engineer",
        "modeled tables analysts can trust",
        "SQL, dbt, warehouses, testing, documentation, BI",
    ),
    (
        "Data",
        "Data Analyst",
        "answers from warehouses, with the query attached",
        "SQL, spreadsheets or BI, Python optional, dashboards, stakeholder questions",
    ),
    (
        "Data",
        "ETL Engineer",
        "extract, transform, load jobs you own when they break",
        "SQL, Python, Airflow or similar, schemas, incremental loads",
    ),
    (
        "Data",
        "Data Warehouse Engineer",
        "the warehouse schema and the jobs that fill it",
        "SQL, Snowflake or BigQuery or Redshift, modeling, cost, access",
    ),
    (
        "Data",
        "Business Intelligence Engineer",
        "dashboards tied to definitions, not vanity charts",
        "SQL, Looker or Power BI or Tableau, semantic layer, access control",
    ),
    (
        "Data",
        "Data Architect",
        "how data is stored, named, and allowed to move",
        "modeling, warehouses, governance, SQL, pipeline topology",
    ),
    (
        "Data",
        "Streaming Data Engineer",
        "events in motion that you can replay and reason about",
        "Kafka or Pub/Sub, SQL, Python or Scala, exactly-once caveats, lag",
    ),
    (
        "Security",
        "Security Engineer",
        "controls you designed, tested, and still operate",
        "IAM, detection, hardening, reviews, incident response",
    ),
    (
        "Security",
        "Cybersecurity Analyst",
        "alerts you triaged and the ones you proved were real",
        "SIEM, log analysis, MITRE ATT&CK, ticketing, containment",
    ),
    (
        "Security",
        "SOC Analyst",
        "shift work on detections, with notes another analyst can follow",
        "SIEM, EDR, playbooks, escalation, packet or log review",
    ),
    (
        "Security",
        "Penetration Tester",
        "authorized tests with findings a team actually fixed",
        "OWASP, Burp, recon, report writing, retest evidence",
    ),
    (
        "Security",
        "Application Security Engineer",
        "code and pipelines you made harder to abuse",
        "SAST/DAST, threat modeling, reviews, secrets, OWASP",
    ),
    (
        "Security",
        "Cloud Security Engineer",
        "cloud identities, networks, and posture you locked down",
        "IAM, CSPM, network policy, encryption, Terraform or console evidence",
    ),
    (
        "Security",
        "IAM Engineer",
        "who can log in, and how you know they should",
        "SSO, SAML or OIDC, directory, RBAC, joiner-mover-leaver",
    ),
    (
        "Security",
        "GRC Analyst",
        "controls mapped to evidence, not a policy nobody follows",
        "ISO or SOC 2 or NIST, audits, risk register, evidence collection",
    ),
    (
        "Security",
        "Security Architect",
        "the shape of trust across systems you still have to live with",
        "threat models, patterns, IAM, network, review boards",
    ),
    (
        "Quality",
        "QA Engineer",
        "bugs you found before users did, with steps to reproduce",
        "test cases, exploratory testing, defect tracking, APIs or UI",
    ),
    (
        "Quality",
        "SDET",
        "tests in code that gate a release",
        "Python or Java or JS, Selenium or Playwright or pytest, CI, APIs",
    ),
    (
        "Quality",
        "Test Automation Engineer",
        "suites you own when they go red",
        "Playwright or Cypress or Selenium, CI, page objects, flake hunting",
    ),
    (
        "Quality",
        "Performance Engineer",
        "load you put on a system and the bottleneck you named",
        "k6 or JMeter, metrics, profiling, SLAs, reports",
    ),
    (
        "Quality",
        "QA Analyst",
        "acceptance you signed only after you tried to break it",
        "test plans, UAT, regression, tickets, product sense",
    ),
    (
        "Architecture",
        "Solutions Architect",
        "designs that got built, not slideware",
        "system design, integration, cloud, trade-off writeups, reviews",
    ),
    (
        "Architecture",
        "Software Architect",
        "boundaries, contracts, and the code that still respects them",
        "design docs, APIs, domain modeling, reviews, evolution",
    ),
    (
        "Architecture",
        "Cloud Architect",
        "cloud topologies you can still draw from production",
        "AWS or Azure or GCP, networking, IAM, cost, landing zones",
    ),
    (
        "Architecture",
        "Enterprise Architect",
        "how portfolios connect, with decisions written down",
        "capability maps, integration, standards, governance, roadmaps",
    ),
    (
        "Architecture",
        "Technical Architect",
        "the technical path a delivery team actually followed",
        "design, spikes, NFRs, reviews, delivery with engineers",
    ),
    (
        "Architecture",
        "Integration Architect",
        "how systems talk when none of them want to",
        "APIs, events, ESB or iPaaS, contracts, failure modes",
    ),
    (
        "IT operations",
        "IT Support Specialist",
        "tickets you closed and the ones you escalated with evidence",
        "Windows or macOS, identity, imaging, remote tools, customer notes",
    ),
    (
        "IT operations",
        "Help Desk Technician",
        "first-line fixes and a trail another tech can follow",
        "ticketing, passwords, hardware, SOP, remote support",
    ),
    (
        "IT operations",
        "Desktop Support",
        "devices you imaged, repaired, and returned to people",
        "Windows, macOS, imaging, hardware, MDM, on-site",
    ),
    (
        "IT operations",
        "IT Operations Engineer",
        "the run of production IT, not a single ticket",
        "monitoring, change, backups, identity, on-call",
    ),
    (
        "IT operations",
        "IT Manager",
        "a team, a budget, and services that stayed up",
        "people, vendors, SLAs, change, reporting — name the estate",
    ),
    (
        "IT operations",
        "Technical Project Manager",
        "IT deliveries you drove to a date with a scope",
        "plans, risks, vendors, engineering partners, status that was true",
    ),
    (
        "IT operations",
        "Scrum Master",
        "an engineering team whose board matched reality",
        "facilitation, impediments, metrics you did not game, delivery",
    ),
    (
        "IT operations",
        "Solutions Engineer",
        "proofs of concept that ran on the customer’s problem",
        "demos, architecture talks, APIs, the deal you technically unblocked",
    ),
    (
        "IT operations",
        "Sales Engineer",
        "technical sales you supported with a working demo",
        "product, objections, POCs, RFPs, the stack you showed",
    ),
    (
        "IT operations",
        "Technical Writer",
        "docs engineers or users used without asking you",
        "docs-as-code, APIs, tutorials, review with the team that ships",
    ),
    (
        "IT operations",
        "Developer Advocate",
        "talks, samples, or issues you filed that changed a product",
        "samples, public speaking, GitHub, the product you actually used",
    ),
    (
        "IT operations",
        "IT Auditor",
        "controls you tested, with samples and exceptions",
        "ITGC, sampling, evidence, SOX or ISO, writeups",
    ),
    (
        "Databases & enterprise",
        "Database Administrator",
        "databases you backed up, recovered, and tuned",
        "SQL, backups, replication, permissions, incident recovery",
    ),
    (
        "Databases & enterprise",
        "PostgreSQL DBA",
        "Postgres you vacuumed, replicated, and restored",
        "PostgreSQL, replication, EXPLAIN, backups, extensions",
    ),
    (
        "Databases & enterprise",
        "Oracle DBA",
        "Oracle instances you kept recoverable",
        "Oracle, RMAN, Data Guard, performance, patching",
    ),
    (
        "Databases & enterprise",
        "Salesforce Developer",
        "Salesforce org work that went to production",
        "Apex, Lightning, SOQL, flows, deployment",
    ),
    (
        "Databases & enterprise",
        "SAP Technical Consultant",
        "SAP technical work you configured or coded",
        "ABAP or Basis or integration, transports, the module you touched",
    ),
    (
        "Databases & enterprise",
        "ERP Developer",
        "ERP customizations you released and supported",
        "the ERP name, code or config, integrations, testing",
    ),
    (
        "Databases & enterprise",
        "ServiceNow Developer",
        "ServiceNow apps or workflows you shipped",
        "JavaScript, Flow Designer, ITSM, update sets, CMDB",
    ),
    (
        "Databases & enterprise",
        "Microsoft 365 Administrator",
        "tenants you secured and kept usable",
        "Entra ID, Exchange, Intune, SharePoint, Conditional Access",
    ),
    (
        "Specialized",
        "Embedded Engineer",
        "firmware or devices that left the bench",
        "C, RTOS or bare metal, peripherals, debugging, schematics",
    ),
    (
        "Specialized",
        "Firmware Engineer",
        "firmware versions you flashed and could roll back",
        "C, bootloaders, hardware bring-up, test jigs, versioning",
    ),
    (
        "Specialized",
        "IoT Engineer",
        "devices in the field that still reported in",
        "MQTT or similar, firmware, cloud ingest, OTA, hardware constraints",
    ),
    (
        "Specialized",
        "Gameplay Programmer",
        "game systems players actually touched",
        "C++ or C#, Unity or Unreal, gameplay, debugging, shipping a build",
    ),
    (
        "Specialized",
        "Graphics Engineer",
        "rendering work that hit a frame budget",
        "C++, shaders, GPU, profiling, the engine you used",
    ),
    (
        "Specialized",
        "Blockchain Engineer",
        "contracts or nodes you deployed, with the tx on a chain",
        "Solidity or similar, testing, wallets, audits you did not skip",
    ),
    (
        "Specialized",
        "GIS Engineer",
        "maps and spatial data you processed for a real area",
        "PostGIS or QGIS, Python, projections, pipelines, tiles",
    ),
    (
        "Specialized",
        "HPC Engineer",
        "jobs you ran on a cluster and got back",
        "Linux, schedulers, MPI or similar, storage, performance",
    ),
    (
        "Specialized",
        "Robotics Engineer",
        "robots or simulations you made move on purpose",
        "ROS, C++ or Python, sensors, control, the hardware or sim",
    ),
    (
        "Specialized",
        "UX Engineer",
        "design-system code that shipped in a product",
        "HTML, CSS, JS, accessibility, design tools, the component library",
    ),
    (
        "Specialized",
        "Accessibility Engineer",
        "barriers you found and the fixes that landed",
        "WCAG, screen readers, ARIA, audits, engineering partners",
    ),
    (
        "Specialized",
        "FinTech Engineer",
        "money movement or ledgers you could reconcile",
        "backend, SQL, idempotency, audit logs, the payment or ledger path",
    ),
)


def _slug(title: str) -> str:
    out = []
    for ch in title.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


ROLES: tuple[RoleTemplate, ...] = tuple(
    RoleTemplate(id=_slug(title), title=title, family=family, focus=focus, tools=tools)
    for family, title, focus, tools in _RAW
)

_BY_ID = {r.id: r for r in ROLES}


def get_role(role_id: str) -> RoleTemplate | None:
    return _BY_ID.get(role_id)


def grouped_roles() -> list[tuple[str, list[RoleTemplate]]]:
    buckets: dict[str, list[RoleTemplate]] = {}
    for role in ROLES:
        buckets.setdefault(role.family, []).append(role)
    return [(fam, buckets[fam]) for fam in FAMILY_ORDER if fam in buckets]


def resume_markdown(role: RoleTemplate) -> str:
    return (
        f"[Your name]\n"
        f"[email] · [city, country]\n"
        f"Work authorization: [yours]\n"
        f"\n"
        f"SUMMARY\n"
        f"{role.title} — {role.focus}. Career start: [year]. "
        f"Write only work you have done.\n"
        f"\n"
        f"SKILLS\n"
        f"List tools you can evidence in a bullet below. "
        f"Common in this title (do not copy a tool you have not used): {role.tools}.\n"
        f"\n"
        f"EXPERIENCE\n"
        f"[Title], [Employer] ([start] – [end or present])\n"
        f"- [What you shipped. Name the system, the tool, the outcome.]\n"
        f"- [A second bullet from the same job.]\n"
        f"- [A third bullet. No keyword without a system behind it.]\n"
        f"\n"
        f"[Earlier title], [Employer] ([dates])\n"
        f"- [One evidenced bullet.]\n"
        f"\n"
        f"Do not add {role.title} keywords you cannot point to in a bullet. "
        f"Provtara will not invent them later either.\n"
    )


def letter_markdown(role: RoleTemplate) -> str:
    return (
        f"Dear hiring team,\n"
        f"\n"
        f"You are hiring a {role.title} — {role.focus}. "
        f"I am writing from work I have already shipped, not from a stack I am pretending to have.\n"
        f"\n"
        f"[One paragraph: the problem in their posting that matches something you built.]\n"
        f"\n"
        f"[One paragraph: two or three evidenced bullets, rewritten as prose. "
        f"Typical tools in this title, only if you used them: {role.tools}.]\n"
        f"\n"
        f"If the role requires a tool I have not used in production, I will name that gap "
        f"in this letter and leave it off the résumé.\n"
        f"\n"
        f"I will submit this pack myself.\n"
        f"\n"
        f"[Your name]\n"
        f"[email]\n"
    )


# Worked examples: a person who already has this title's evidence.
# Candidates measure their own bullets against these. Do not copy unearned claims.

_PERSONAS: tuple[tuple[str, str, str, str, str], ...] = (
    ("Chioma Okonkwo", "Lagos, Nigeria", "chioma.okonkwo@example.com", "NG", "University of Lagos"),
    ("Adewale Balogun", "Abuja, Nigeria", "adewale.balogun@example.com", "NG", "University of Ibadan"),
    ("Ngozi Eze", "Port Harcourt, Nigeria", "ngozi.eze@example.com", "NG", "University of Nigeria, Nsukka"),
    ("Yusuf Abdullahi", "Kano, Nigeria", "yusuf.abdullahi@example.com", "NG", "Ahmadu Bello University"),
    ("Amina Bello", "Lagos, Nigeria", "amina.bello@example.com", "NG", "Covenant University"),
    ("Ibrahim Suleiman", "Abuja, Nigeria", "ibrahim.suleiman@example.com", "NG", "University of Jos"),
    ("Wanjiku Mwangi", "Nairobi, Kenya", "wanjiku.mwangi@example.com", "KE", "University of Nairobi"),
    ("Kwame Mensah", "Accra, Ghana", "kwame.mensah@example.com", "GH", "KNUST"),
    ("Thandiwe Nkosi", "Johannesburg, South Africa", "thandiwe.nkosi@example.com", "ZA", "University of Cape Town"),
    ("Tunde Adebayo", "London / Lagos", "tunde.adebayo@example.com", "NG, UK", "Obafemi Awolowo University"),
)

_SHOPS: dict[str, tuple[tuple[str, str, str, str], tuple[str, str, str, str]]] = {
    "Networking & infrastructure": (
        ("MainOne", "Lagos", "2019", "present"),
        ("MTN Nigeria", "Lagos", "2016", "2019"),
    ),
    "Programming": (
        ("Paystack", "Lagos", "2019", "present"),
        ("Interswitch", "Lagos", "2016", "2019"),
    ),
    "Mobile": (
        ("Kuda", "Lagos", "2020", "present"),
        ("Carbon", "Lagos", "2017", "2020"),
    ),
    "DevOps & cloud": (
        ("Andela", "Lagos / remote", "2019", "present"),
        ("SystemSpecs", "Lagos", "2016", "2019"),
    ),
    "AI / ML": (
        ("Data Science Nigeria", "Lagos", "2020", "present"),
        ("Interswitch", "Lagos", "2017", "2020"),
    ),
    "Data": (
        ("Flutterwave", "Lagos", "2020", "present"),
        ("Paystack", "Lagos", "2017", "2020"),
    ),
    "Security": (
        ("Interswitch", "Lagos", "2019", "present"),
        ("First Bank of Nigeria — IT", "Lagos", "2016", "2019"),
    ),
    "Quality": (
        ("Andela", "Lagos / remote", "2019", "present"),
        ("Cowrywise", "Lagos", "2016", "2019"),
    ),
    "Architecture": (
        ("Flutterwave", "Lagos", "2019", "present"),
        ("Interswitch", "Lagos", "2015", "2019"),
    ),
    "IT operations": (
        ("Access Bank — Technology", "Lagos", "2018", "present"),
        ("MainOne", "Lagos", "2015", "2018"),
    ),
    "Databases & enterprise": (
        ("SystemSpecs", "Lagos", "2018", "present"),
        ("GTBank — Technology", "Lagos", "2015", "2018"),
    ),
    "Specialized": (
        ("Andela", "Lagos / remote", "2019", "present"),
        ("CcHUB", "Lagos", "2016", "2019"),
    ),
}


def _persona(role: RoleTemplate) -> tuple[str, str, str, str, str]:
    return _PERSONAS[sum(ord(c) for c in role.id) % len(_PERSONAS)]


def _shops(role: RoleTemplate) -> tuple[tuple[str, str, str, str], tuple[str, str, str, str]]:
    return _SHOPS.get(role.family, _SHOPS["Programming"])


def _tool_list(role: RoleTemplate) -> list[str]:
    parts = [p.strip() for p in role.tools.split(",") if p.strip()]
    return parts or ["Linux", "Git"]


def example_resume(role: RoleTemplate) -> str:
    name, city, email, auth, school = _persona(role)
    current, earlier = _shops(role)
    tools = _tool_list(role)
    t0, t1, t2 = (tools + ["Git", "Linux", "documentation"])[:3]
    skill_line = ", ".join(tools[:8])
    return (
        f"{name}\n"
        f"{email} · {city}\n"
        f"Work authorization: {auth}\n"
        f"\n"
        f"SUMMARY\n"
        f"{role.title} with nine years in production systems. "
        f"I am hired for {role.focus}. "
        f"Career start: 2016. Every tool below appears in a bullet.\n"
        f"\n"
        f"SKILLS\n"
        f"{skill_line}\n"
        f"\n"
        f"EXPERIENCE\n"
        f"Senior {role.title}, {current[0]} ({current[2]} – {current[3]}) — {current[1]}\n"
        f"- Own {role.focus} for a live service: {t0} in production, not a lab. "
        f"On-call notes name the failure, then the fix.\n"
        f"- Cut a recurring incident class by changing how we used {t1}; "
        f"the next person ran the same playbook without asking me.\n"
        f"- Shipped a change that depended on {t2}, with a rollback that we actually used once.\n"
        f"- Review the work of two engineers on the same stack. I do not sign off a keyword with no system behind it.\n"
        f"\n"
        f"{role.title}, {earlier[0]} ({earlier[2]} – {earlier[3]}) — {earlier[1]}\n"
        f"- Built and ran the {role.focus} path using {t0} and {t1}. "
        f"When it broke at 2 a.m., I was the person who could recover it.\n"
        f"- Wrote the internal guide for {t2} that new hires still open in week one.\n"
        f"- Left the job with backups, access lists, and a successor who could deploy without me.\n"
        f"\n"
        f"EDUCATION\n"
        f"B.Sc. Computer Science, {school}, 2016\n"
        f"\n"
        f"This example is a measurement stick. Copy a line only if you can point at the system, the date, and the person who saw you do it.\n"
    )


def example_letter(role: RoleTemplate) -> str:
    name, city, email, _auth, _school = _persona(role)
    current, earlier = _shops(role)
    tools = _tool_list(role)
    t0, t1 = (tools + ["Git", "Linux"])[:2]
    return (
        f"Dear hiring team,\n"
        f"\n"
        f"You are hiring a {role.title} whose job is {role.focus}. "
        f"That is the work I have been paid to do since 2016, most recently at {current[0]} in {current[1]}.\n"
        f"\n"
        f"At {current[0]} I own the live path, not a slide about it. "
        f"I run {t0} in production. When we had a class of failures tied to {t1}, "
        f"I changed the design, wrote the playbook, and stayed on the rotation until the next person could run it cold. "
        f"That is the standard I will bring to your posting: a system I can name, a change I can date, and an outcome someone else can verify.\n"
        f"\n"
        f"Before that, at {earlier[0]}, I was the {role.title} who recovered the same class of work at 2 a.m. "
        f"I do not list a tool I have not used on a system that billed real users. "
        f"If your role requires something I have not run in production, I will say so in this letter and leave it off the résumé.\n"
        f"\n"
        f"I will submit this pack myself.\n"
        f"\n"
        f"{name}\n"
        f"{email} · {city}\n"
    )


def resume_pack_markdown(role: RoleTemplate) -> str:
    return (
        f"# {role.title} — worked example\n\n"
        f"{example_resume(role)}\n"
        f"---\n\n"
        f"# {role.title} — fill-in template\n\n"
        f"{resume_markdown(role)}"
    )


def letter_pack_markdown(role: RoleTemplate) -> str:
    return (
        f"# {role.title} cover letter — worked example\n\n"
        f"{example_letter(role)}\n"
        f"---\n\n"
        f"# {role.title} cover letter — fill-in template\n\n"
        f"{letter_markdown(role)}"
    )
