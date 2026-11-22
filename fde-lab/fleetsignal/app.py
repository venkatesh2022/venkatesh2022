"""FleetSignal: synthetic vehicle telemetry correlation and service escalation.
This local, deterministic reference implementation sends no alerts or tickets.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

DEFAULT_LIMITS = {"drain_pct_per_hour": 8.0, "temperature_c": 65.0}


def analyze(payload):
    """Join telemetry to asset registry and service state; report traceable decisions."""
    assets = {a["vehicle_id"]: a for a in payload.get("assets", [])}
    open_orders = {
        (w["vehicle_id"], w["sensor_id"])
        for w in payload.get("work_orders", [])
        if w.get("status") == "open"
    }
    limits = {**DEFAULT_LIMITS, **payload.get("limits", {})}
    seen_messages = set()
    incidents = {}
    rejected = []
    for event in payload.get("telemetry", []):
        msg = event.get("message_id")
        if not msg or msg in seen_messages:
            rejected.append({"message_id": msg, "reason": "missing_or_duplicate_message_id"})
            continue
        seen_messages.add(msg)
        vehicle_id, sensor_id = event.get("vehicle_id"), event.get("sensor_id")
        if not vehicle_id or not sensor_id or vehicle_id not in assets:
            rejected.append({"message_id": msg, "reason": "unknown_asset_or_sensor"})
            continue
        try:
            ts = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
            drain = float(event["battery_drain_pct_per_hour"])
            temp = float(event["temperature_c"])
        except (ValueError, TypeError, KeyError):
            rejected.append({"message_id": msg, "reason": "invalid_measurement"})
            continue
        hit_drain = drain >= limits["drain_pct_per_hour"]
        hit_temp = temp >= limits["temperature_c"]
        if not (hit_drain or hit_temp):
            continue
        incident_key = f"{vehicle_id}:{sensor_id}:{ts.date().isoformat()}"
        severity = "high" if hit_drain and hit_temp else "medium"
        reasons = []
        if hit_drain:
            reasons.append("high_battery_drain")
        if hit_temp:
            reasons.append("high_temperature")
        candidate = {
            "incident_key": incident_key,
            "vehicle_id": vehicle_id,
            "sensor_id": sensor_id,
            "asset_class": assets[vehicle_id].get("class", "unspecified"),
            "severity": severity,
            "signal_reasons": reasons,
            "source_message_id": msg,
            "open_work_order_exists": (vehicle_id, sensor_id) in open_orders,
            "recommended_next_step": "review_telemetry_and_request_technician_inspection",
            "simulated_ticket_only": True,
        }
        previous = incidents.get(incident_key)
        if previous is None or (previous["severity"] == "medium" and severity == "high"):
            incidents[incident_key] = candidate
    return {
        "incidents": sorted(incidents.values(), key=lambda x: x["incident_key"]),
        "rejected_events": rejected,
        "unique_messages_processed": len(seen_messages),
        "tickets_sent": 0,
    }


def main():
    p = argparse.ArgumentParser(description="FleetSignal synthetic incident correlation")
    p.add_argument("scenario", help="JSON scenario containing asset, service and telemetry data")
    args = p.parse_args()
    result = analyze(json.loads(Path(args.scenario).read_text()))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
