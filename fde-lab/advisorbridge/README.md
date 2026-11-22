# AdvisorBridge — Audit-First Financial Operations Workflow

**Status: working local reference prototype (synthetic data, no external integrations).**

## Fictional customer brief
A financial-services operations team receives requests to prepare and release document packets. Staff need a way to verify documentation, enforce independent review, and leave an auditable trail **without copying sensitive customer data into logs**. An AI assistant could eventually propose steps, but must not override policy or execute sensitive actions unsupervised.

## What is implemented
- Declarative role/action policy for preparing and releasing a packet
- Evidence completeness checks for identity verification and customer consent
- Separation of duties for simulated packet release
- Deterministic blocked/awaiting-approval/approved decisions
- Idempotent, minimized in-memory audit entries with hashed customer references
- Six unit tests covering approvals, permission failures, missing evidence, and audit behavior

No real packets are sent and no external services are called.

## Architecture

~~~mermaid
flowchart LR
  A["Customer request"] --> B["Policy and evidence checks"]
  B --> C{"Allowed?"}
  C -->|No| D["Blocked + reason codes"]
  C -->|Needs approval| E["Independent compliance approval"]
  E --> F["Simulated approval"]
  D --> G["Minimized audit log"]
  F --> G
~~~

## Try it
From this directory, with Python 3.9+:

~~~bash
python app.py sample_request.json
python app.py sample_request.json --approve risk-2
python -m unittest test_app.py -v
~~~

Without approval, the sample request is awaiting independent approval. With the synthetic approver, it is approved **for simulation only**.

## FDE engagement story
1. **Discovery:** interview operations and compliance about packet-release bottlenecks and exception handling.
2. **Constraints:** no customer PII in logs; separation of duties; deterministic policy before any model suggestions.
3. **Integration plan:** read-only CRM document metadata adapter, configurable policy store, human approval service.
4. **Acceptance criteria:** missing evidence always blocks; requester cannot self-approve; repeated request IDs don't create duplicate audit events.
5. **Handoff:** publish policy ownership, incident runbook, audit retention policy, and approval escalation contacts.

## Honest limitations / next steps
This is an **in-memory CLI simulation**, not a regulated or deployed system. A production adaptation would require authentication, immutable audit persistence, real identity controls, secure adapters, tests against external systems, and compliance sign-off. Avoid using live customer data in this demo.

**Portfolio owner:** [Venkatesh Thota](https://github.com/venkatesh2022)
