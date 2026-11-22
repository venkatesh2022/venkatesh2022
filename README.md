<div align="center">

# Venkatesh Thota
### Forward Deployed Engineering · Software Engineering · Applied AI

**From ambiguous customer problems to software people can actually operate.**

I work at the intersection of backend engineering, data integration, and AI-powered applications. I enjoy translating real operational problems into reliable systems, useful workflows, and clear handoffs.

[![FDE Portfolio](https://img.shields.io/badge/Explore-FDE%20Project%20Lab-2563EB)](fde-lab/README.md)
[![GitHub](https://img.shields.io/badge/GitHub-venkatesh2022-181717?logo=github&logoColor=white)](https://github.com/venkatesh2022?tab=repositories)

</div>

## What I bring to a customer deployment

- **Business-to-engineering translation:** unpack workflow bottlenecks, map stakeholders, define acceptance criteria, and build a useful first vertical slice.
- **Systems integration:** connect APIs, events, identity boundaries, and messy enterprise data with explicit contracts and failure handling.
- **Safe automation:** design review gates, role checks, auditability, deterministic fallbacks, and clear escalation paths before adding AI.
- **Operational ownership:** think beyond the demo—tests, observability, runbooks, rollback plans, and maintainable handoff documentation.

**Background:** Senior Software Engineer at **LPL Financial**, previously Software Development Engineer I at **Amazon**, working with enterprise applications, AI-assisted workflows, authentication, smart-vehicle services, and telemetry analytics.

## Three FDE project case studies

> These are **original, runnable local reference prototypes with synthetic data**, not client deployments or production systems. Each includes a fictional customer brief, implementation, test suite, architecture, acceptance criteria, and handoff considerations.

### 01 · [AdvisorBridge — Audit-First Workflow Orchestrator](fde-lab/advisorbridge/README.md)

**Customer challenge:** A financial-services operations team needs document-release workflows with evidence verification, separation of duties, and minimal audit data.

**What the prototype demonstrates:** role-policy enforcement, evidence checks, independent approval, request idempotency, reason-coded decisions, and an audit trail without storing customer identities in clear text.

**Why it matters to FDE:** deploy technology into regulated, approval-heavy workflows without giving an AI assistant unchecked authority.

[Read case study](fde-lab/advisorbridge/README.md) · [Code](fde-lab/advisorbridge/app.py) · [Tests](fde-lab/advisorbridge/test_app.py)

### 02 · [FleetSignal — Telemetry-to-Service Incident Engine](fde-lab/fleetsignal/README.md)

**Customer challenge:** A fleet operator is overwhelmed by duplicate vehicle alerts that aren't connected to service-ticket history.

**What the prototype demonstrates:** multi-source event correlation, threshold reasoning, duplicate suppression, anomaly severity, explainable recommendations, and ticket-awareness.

**Why it matters to FDE:** fit operational software to physical-world workflows rather than ship an isolated dashboard.

[Read case study](fde-lab/fleetsignal/README.md) · [Code](fde-lab/fleetsignal/app.py) · [Tests](fde-lab/fleetsignal/test_app.py)

### 03 · [ContractLens — Vendor Schema Drift & Migration Dry-Run](fde-lab/contractlens/README.md)

**Customer challenge:** A manufacturer needs to onboard mismatched supplier exports without silently losing data or corrupting orders.

**What the prototype demonstrates:** field mapping, schema-drift detection, validation, duplicate checks, record/value reconciliation, and a no-write approval gate.

**Why it matters to FDE:** solve the messy last mile of enterprise integration, where data quality and operator trust are part of the product.

[Read case study](fde-lab/contractlens/README.md) · [Code](fde-lab/contractlens/app.py) · [Tests](fde-lab/contractlens/test_app.py)

## Deployment mindset

| Stage | Question I ask | Engineering artifact |
| --- | --- | --- |
| Discover | What actually blocks the customer's workflow? | Customer brief, constraints, success criteria |
| Integrate | How do their data and systems really behave? | Mapping contract, adapters, error taxonomy |
| De-risk | What happens on bad input or an unsafe action? | Policy checks, dry-run, audit, unit tests |
| Hand off | Can the customer support this after go-live? | Runbook, ownership, monitoring and rollback plan |

## Technology

**Backend & integrations:** Java · Python · SQL · REST APIs · FastAPI

**AI & analytics:** Retrieval-Augmented Generation (RAG) · LLM application patterns · scikit-learn · Pandas · PySpark

**Cloud & delivery:** AWS · Docker · GitHub Actions · Databricks · CI/CD concepts

## More engineering work

- [Receipt Rewards API](https://github.com/venkatesh2022/receipt-processor-challenge) — FastAPI/Pydantic service, Dockerfile, and endpoint tests.
- [Orders Analytics Lakehouse](https://github.com/venkatesh2022/databricks-task) — PySpark/SQL medallion architecture and order analytics.
- [Movie Recommendation Prototype](https://github.com/venkatesh2022/mlrecommendation-app-flask) — Flask and ML experimentation; development work remains.

## Experience

**LPL Financial** · Senior Software Engineer · Nov 2024–Present  
Enterprise advisor workflows, backend integration, secure session management, and AI-assisted applications.

**Amazon** · Software Development Engineer I · Sep 2022–Oct 2024  
Cloud-connected smart-vehicle services, backend engineering, and sensor-data analytics.

## Connect

[Explore my repositories](https://github.com/venkatesh2022?tab=repositories) · [FDE project lab](fde-lab/README.md)

*The best software doesn't end at a successful demo—it makes the customer's workflow better and remains operable afterward.*
