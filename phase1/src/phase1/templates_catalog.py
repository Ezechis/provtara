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
