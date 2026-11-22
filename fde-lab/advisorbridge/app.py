"""AdvisorBridge: auditable, synthetic advisor-operations approval simulation.

This is a local reference implementation. It does not connect to client systems,
provide financial advice, or send documents to external recipients.
"""
import argparse
import hashlib
import json
from pathlib import Path

POLICY = {
    "prepare_packet": {"ops", "compliance"},
    "release_packet": {"compliance", "ops"},
}
REQUIRED_EVIDENCE = {"identity_verification", "customer_consent"}


def evaluate(request, approval=None):
    """Return a deterministic policy decision without changing external systems."""
    reasons = []
    action = request.get("action")
    requester = request.get("requested_by", {})
    role = requester.get("role")
    if action not in POLICY:
        reasons.append("unknown_action")
    elif role not in POLICY[action]:
        reasons.append("requester_role_not_permitted")
    evidence = {
        e.get("kind") for e in request.get("evidence", [])
        if isinstance(e, dict) and e.get("verified") is True
    }
    missing = sorted(REQUIRED_EVIDENCE - evidence)
    if missing:
        reasons.append("missing_verified_evidence:" + ",".join(missing))
    if not request.get("request_id") or not request.get("customer_ref"):
        reasons.append("missing_request_or_customer_reference")
    if reasons:
        status = "blocked"
    elif action == "release_packet":
        if approval is None:
            status = "awaiting_approval"
            reasons.append("independent_compliance_approval_required")
        elif (
            approval.get("role") != "compliance"
            or not approval.get("approver_id")
            or approval.get("approver_id") == requester.get("id")
            or approval.get("request_id") != request.get("request_id")
        ):
            status = "blocked"
            reasons.append("invalid_or_nonindependent_approval")
        else:
            status = "approved_for_simulation"
    else:
        status = "ready_for_simulation"
    return {"request_id": request.get("request_id"), "status": status, "reasons": reasons}


class AuditLog:
    def __init__(self):
        self._events = {}

    def record(self, request, decision):
        """Idempotent, minimized audit records. No customer PII or documents."""
        key = request.get("request_id")
        if not key:
            raise ValueError("request_id is required")
        if key in self._events:
            return self._events[key], False
        masked = hashlib.sha256(str(request.get("customer_ref", "")).encode()).hexdigest()[:12]
        event = {
            "request_id": key,
            "customer_hash_prefix": masked,
            "action": request.get("action"),
            "decision": decision["status"],
            "reasons": decision["reasons"],
            "simulation_only": True,
        }
        self._events[key] = event
        return event, True


def main():
    parser = argparse.ArgumentParser(description="AdvisorBridge policy simulator")
    parser.add_argument("request_json", help="Path to synthetic request JSON")
    parser.add_argument("--approve", help="Synthetic compliance approver ID (no external action)")
    args = parser.parse_args()
    request = json.loads(Path(args.request_json).read_text())
    approval = None
    if args.approve:
        approval = {
            "role": "compliance",
            "approver_id": args.approve,
            "request_id": request.get("request_id"),
        }
    decision = evaluate(request, approval)
    audit, _ = AuditLog().record(request, decision)
    print(json.dumps({"decision": decision, "audit": audit}, indent=2))


if __name__ == "__main__":
    main()
