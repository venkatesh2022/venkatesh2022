"""ContractLens: vendor order schema drift and reconciliation dry-run.
Standard-library-only portfolio prototype. Never connects to a real database.
"""
import argparse
import json
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = {"order_id", "sku", "quantity", "unit_price", "order_date"}


def audit_batch(batch):
    mapping = batch.get("field_mapping", {})
    rows = batch.get("records", [])
    mapped = set(mapping.values())
    missing_mapping = sorted(REQUIRED - mapped)
    incoming_fields = set().union(*(set(row) for row in rows)) if rows else set()
    unexpected = sorted(incoming_fields - set(mapping))
    missing_source = sorted(set(mapping) - incoming_fields)
    validated = []
    rejected = []
    seen = set()
    units = 0
    value = Decimal("0.00")

    for index, source in enumerate(rows, 1):
        record = {canonical: source.get(vendor) for vendor, canonical in mapping.items()}
        errors = []
        if missing_mapping:
            errors.append("required_canonical_mapping_missing")
        if any(record.get(k) in (None, "") for k in REQUIRED):
            errors.append("required_value_missing")
        try:
            quantity = int(record["quantity"])
            if str(record["quantity"]).strip() != str(quantity) or quantity <= 0:
                raise ValueError
        except (ValueError, TypeError, KeyError):
            errors.append("invalid_quantity")
            quantity = None
        try:
            price = Decimal(str(record["unit_price"]))
            if not price.is_finite() or price < 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError, KeyError):
            errors.append("invalid_unit_price")
            price = None
        try:
            date.fromisoformat(str(record["order_date"]))
        except (ValueError, TypeError, KeyError):
            errors.append("invalid_order_date")
        key = (record.get("order_id"), record.get("sku"))
        if all(key) and key in seen:
            errors.append("duplicate_order_line")
        if all(key):
            seen.add(key)
        if errors:
            rejected.append({"row_number": index, "reason_codes": sorted(set(errors))})
            continue
        units += quantity
        value += quantity * price
        validated.append({
            "order_id": str(record["order_id"]),
            "sku": str(record["sku"]),
            "quantity": quantity,
            "unit_price": str(price),
            "order_date": str(record["order_date"]),
        })
    if missing_mapping or missing_source or rejected:
        status = "blocked"
    elif unexpected:
        status = "review_required"
    else:
        status = "validated_dry_run"
    return {
        "status": status,
        "dry_run": True,
        "schema_drift": {
            "missing_canonical_mappings": missing_mapping,
            "missing_source_fields": missing_source,
            "unmapped_vendor_fields": unexpected,
        },
        "reconciliation": {
            "incoming_records": len(rows),
            "accepted_records": len(validated),
            "rejected_records": len(rejected),
            "accepted_units": units,
            "accepted_gross_value": str(value.quantize(Decimal("0.01"))),
        },
        "rejected": rejected,
        "canonical_preview": validated[:5],
        "writes_performed": 0,
    }


def main():
    p = argparse.ArgumentParser(description="ContractLens order-contract dry-run")
    p.add_argument("batch_json", help="Path to synthetic vendor batch JSON")
    args = p.parse_args()
    print(json.dumps(audit_batch(json.loads(Path(args.batch_json).read_text())), indent=2))


if __name__ == "__main__":
    main()
