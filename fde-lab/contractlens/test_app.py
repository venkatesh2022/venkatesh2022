import unittest
from app import audit_batch

MAPPING = {
    "po": "order_id", "product_code": "sku", "units": "quantity",
    "amount": "unit_price", "ordered_on": "order_date",
}

def batch(records, mapping=None):
    return {"field_mapping": mapping if mapping is not None else MAPPING, "records": records}

def record(**overrides):
    return {
        **{"po": "PO-10", "product_code": "SKU-2", "units": "2",
           "amount": "19.95", "ordered_on": "2026-11-22"},
        **overrides,
    }

class ContractLensTests(unittest.TestCase):
    def test_valid_dry_run_reconciles(self):
        output = audit_batch(batch([record()]))
        self.assertEqual(output["status"], "validated_dry_run")
        self.assertEqual(output["reconciliation"]["accepted_gross_value"], "39.90")
        self.assertEqual(output["writes_performed"], 0)

    def test_schema_addition_requires_review(self):
        output = audit_batch(batch([record(fulfillment_code="A")]))
        self.assertEqual(output["status"], "review_required")
        self.assertIn("fulfillment_code", output["schema_drift"]["unmapped_vendor_fields"])

    def test_bad_quantity_blocks(self):
        output = audit_batch(batch([record(units="-2")]))
        self.assertEqual(output["status"], "blocked")
        self.assertEqual(output["reconciliation"]["rejected_records"], 1)

    def test_duplicate_order_line_blocks(self):
        output = audit_batch(batch([record(), record()]))
        self.assertEqual(output["status"], "blocked")
        self.assertEqual(output["reconciliation"]["accepted_records"], 1)

    def test_missing_field_mapping_blocks(self):
        output = audit_batch(batch([record()], {"po": "order_id"}))
        self.assertEqual(output["status"], "blocked")
        self.assertIn("sku", output["schema_drift"]["missing_canonical_mappings"])

    def test_bad_date_blocks(self):
        self.assertEqual(audit_batch(batch([record(ordered_on="yesterday")]))["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
