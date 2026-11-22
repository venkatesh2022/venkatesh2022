import unittest
from app import analyze

def scenario(events, work_orders=None):
    return {
        "assets": [{"vehicle_id": "EV-10", "class": "delivery-ev"}],
        "work_orders": work_orders or [],
        "telemetry": events,
    }

def event(message_id, drain=9, temp=69, vehicle_id="EV-10"):
    return {
        "message_id": message_id, "vehicle_id": vehicle_id,
        "sensor_id": "BAT-1", "timestamp": "2026-11-22T10:15:00Z",
        "battery_drain_pct_per_hour": drain, "temperature_c": temp,
    }

class FleetSignalTests(unittest.TestCase):
    def test_correlated_high_severity(self):
        incident = analyze(scenario([event("e1")]))["incidents"][0]
        self.assertEqual(incident["severity"], "high")
        self.assertEqual(len(incident["signal_reasons"]), 2)

    def test_duplicate_message_is_rejected(self):
        out = analyze(scenario([event("e1"), event("e1")]))
        self.assertEqual(len(out["incidents"]), 1)
        self.assertEqual(len(out["rejected_events"]), 1)

    def test_normal_reading_is_not_incident(self):
        self.assertEqual(analyze(scenario([event("e2", 2, 45)]))["incidents"], [])

    def test_unknown_asset_is_rejected(self):
        out = analyze(scenario([event("e3", vehicle_id="EV-99")]))
        self.assertEqual(out["rejected_events"][0]["reason"], "unknown_asset_or_sensor")

    def test_open_ticket_is_exposed_to_operator(self):
        orders = [{"vehicle_id": "EV-10", "sensor_id": "BAT-1", "status": "open"}]
        incident = analyze(scenario([event("e4")], orders))["incidents"][0]
        self.assertTrue(incident["open_work_order_exists"])

    def test_never_sends_tickets(self):
        self.assertEqual(analyze(scenario([event("e5")]))["tickets_sent"], 0)


if __name__ == "__main__":
    unittest.main()
