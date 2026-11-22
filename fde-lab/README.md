# Forward Deployed Engineering — Project Lab

Three compact **original reference prototypes**, chosen around customer integration problems rather than generic chatbots. Each uses **synthetic input** and Python's standard library; none is connected to live customer systems.

| Prototype | Scenario | Local implementation | Run |
| --- | --- | --- | --- |
| [AdvisorBridge](advisorbridge/README.md) | Financial-operations approvals and auditability | Policy engine + minimized in-memory audit | See [README](advisorbridge/README.md) |
| [FleetSignal](fleetsignal/README.md) | Vehicle telemetry and maintenance triage | Multi-source correlation + deduplication | See [README](fleetsignal/README.md) |
| [ContractLens](contractlens/README.md) | Supplier order onboarding and schema drift | Mapping validation + reconciliation dry-run | See [README](contractlens/README.md) |

## Run the demos

~~~bash
cd fde-lab/advisorbridge
python app.py sample_request.json
python app.py sample_request.json --approve risk-2
python -m unittest test_app.py -v

cd ../fleetsignal
python app.py sample_fleet.json
python -m unittest test_app.py -v

cd ../contractlens
python app.py sample_partner_batch.json
python -m unittest test_app.py -v
~~~

These scripts have no dependencies outside Python 3.9+ and do not make external requests.

## How to evaluate these as FDE case studies

1. **Discovery evidence:** Does the brief identify a real operational bottleneck and decision-maker?
2. **Integration depth:** Can the system reconcile independent inputs or organizational boundaries?
3. **Correctness under failure:** What happens with duplicates, bad input, missing evidence and unsafe actions?
4. **Human workflow fit:** Does the tool explain its reasoning and preserve necessary approvals?
5. **Supportability:** What changes between a demo and a safe production deployment?

## Roadmap to a full FDE-grade portfolio

For each case study, add a real-world-shaped connector sandbox, durable state, authentication and authorization, failure-injection tests, telemetry, an operations dashboard, container deployment, a short demo video, and a documented rollout/rollback. Collect actual benchmark results before adding performance or business-impact claims.

**Current maturity: local prototypes, not production integrations.**

[Back to Venkatesh's profile](../README.md)
