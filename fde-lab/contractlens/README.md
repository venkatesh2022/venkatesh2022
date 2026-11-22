# ContractLens — Vendor Data Contract & Migration Dry-Run

**Status: working local data-validation prototype on synthetic purchase-order records.**

## Fictional customer brief
A mid-market manufacturer acquires a supplier whose export fields don't match the manufacturer's order schema. The first onboarding attempt fails because unexpected columns, duplicated lines, and numeric formatting changes slip through. The integration team needs a safe **dry-run with evidence**, not another fragile one-off ETL script.

## Implemented vertical slice
- Configurable vendor-field-to-canonical-field mapping
- Required mapping and source-field validation
- Detection of new, unmapped vendor columns (schema drift)
- Record-level checks for positive quantities, monetary amounts and ISO dates
- Duplicate order-line detection
- Record and accepted-value reconciliation using Decimal arithmetic
- Machine-readable decisions: validated_dry_run, review_required or blocked
- No database writes, six automated unit tests

## Flow

~~~mermaid
flowchart LR
  A["Partner export"] --> B["Field mapping"]
  B --> C["Contract and row validation"]
  C --> D["Drift + duplicate detection"]
  D --> E["Reconciliation report"]
  E --> F{"Approval"}
  F -. "future, guarded" .-> G["Canonical order system"]
~~~

## Run
Python 3.9+ standard library only:

~~~bash
python app.py sample_partner_batch.json
python -m unittest test_app.py -v
~~~

The sample intentionally contains an extra "fulfillment_code" field. The dry-run should report **review_required** while reconciling accepted rows. No supplier system is modified.

## FDE engagement story
1. **Discovery:** compare source exports with downstream reporting and order-processing expectations.
2. **Contract design:** agree canonical field ownership, accepted formats and failure policies.
3. **Integration:** ingest raw files into quarantine; validate before any write to operational tables.
4. **Acceptance criteria:** no silent field loss; duplicates detected; quantity and value totals reconciled.
5. **Handoff:** mapping change control, migration rollback plan, quarantine playbook, and daily reconciliation reporting.

## Known limitations and next steps
This is a **single-file dry-run**, not a production migration. Extend it with streaming/CSV adapters, schema versioning, external database integration, durable reject queues, per-partner rules, large-batch tests, alerting and operator sign-off. No customer data or deployment results are claimed.

**Portfolio owner:** [Venkatesh Thota](https://github.com/venkatesh2022)
