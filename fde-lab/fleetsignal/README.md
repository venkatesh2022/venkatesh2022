# FleetSignal — Sensor-to-Service Decision Support

**Status: working local correlation prototype; fully synthetic fleet events.**

## Fictional customer brief
A delivery-fleet operator receives noisy telemetry from several vehicle models. Duplicate messages and disconnected maintenance records produce repeat investigations. They need an explainable view of **which alerts merit technician review**, and whether a related work order is already open.

## Implemented vertical slice
- Joins telemetry events to a vehicle registry and existing maintenance work orders
- Detects high power-drain and thermal anomalies using configurable thresholds
- Records machine-readable reason codes; "high" severity requires both signals
- Deduplicates message IDs and groups recurring alerts by vehicle, sensor and day
- Flags existing open work orders to avoid redundant escalation by an operator
- Rejects unknown assets and malformed events; never sends a real ticket
- Six tests covering detection, duplicates, false positives, missing assets and escalation state

## Architecture

~~~mermaid
flowchart LR
  A["Vehicle telemetry"] --> C["Normalizer + de-dup"]
  B["Asset registry + service work orders"] --> D["Context join"]
  C --> D
  D --> E["Threshold and severity policy"]
  E --> F["Explainable operator incident queue"]
  F -. "future, approved adapter" .-> G["Service ticketing system"]
~~~

## Run
Python 3.9+ standard library only.

~~~bash
python app.py sample_fleet.json
python -m unittest test_app.py -v
~~~

The CLI returns a machine-readable incident queue, rejected events, and zero sent tickets.

## FDE engagement story
- **Discovery:** operators report duplicated tickets and unexplained battery drain.
- **Integration:** align vehicle IDs across a telemetry feed, fleet registry, and ticketing service.
- **Operational guardrails:** avoid direct vehicle commands; never auto-escalate without an operator.
- **Success criteria:** zero duplicate events in the output, explainable severity, existing-ticket awareness.
- **Handoff:** document thresholds, false-positive review, dashboard ownership, alert runbooks and rollback.

## Future production work
Add streaming ingestion, calibrated per-model baselines, durable state and idempotency, authentication, human acknowledgment, connector retries, monitoring, and technician feedback. A rule-based prototype does not demonstrate validated predictive maintenance or real-world business impact.

**Portfolio owner:** [Venkatesh Thota](https://github.com/venkatesh2022)
