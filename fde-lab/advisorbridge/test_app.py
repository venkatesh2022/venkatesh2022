import unittest
from app import AuditLog, evaluate

REQUEST = {
    "request_id": "REQ-001",
    "customer_ref": "DEMO-0042",
    "requested_by": {"id": "ops-7", "role": "ops"},
    "action": "release_packet",
    "evidence": [
        {"kind": "identity_verification", "verified": True},
        {"kind": "customer_consent", "verified": True},
    ],
}


class AdvisorBridgeTests(unittest.TestCase):
    def test_requires_independent_approval(self):
        self.assertEqual(evaluate(REQUEST)["status"], "awaiting_approval")

    def test_compliance_can_approve(self):
        approval = {"role": "compliance", "approver_id": "risk-2", "request_id": "REQ-001"}
        self.assertEqual(evaluate(REQUEST, approval)["status"], "approved_for_simulation")

    def test_self_approval_is_blocked(self):
        approval = {"role": "compliance", "approver_id": "ops-7", "request_id": "REQ-001"}
        self.assertEqual(evaluate(REQUEST, approval)["status"], "blocked")

    def test_missing_evidence_blocks(self):
        bad = {**REQUEST, "evidence": []}
        self.assertEqual(evaluate(bad)["status"], "blocked")

    def test_unknown_action_blocks(self):
        bad = {**REQUEST, "action": "transfer_funds"}
        self.assertEqual(evaluate(bad)["status"], "blocked")

    def test_audit_idempotency_and_minimization(self):
        log = AuditLog()
        d = evaluate(REQUEST)
        first, created = log.record(REQUEST, d)
        second, created_again = log.record(REQUEST, d)
        self.assertTrue(created)
        self.assertFalse(created_again)
        self.assertEqual(first, second)
        self.assertNotIn("DEMO-0042", str(first))


if __name__ == "__main__":
    unittest.main()
