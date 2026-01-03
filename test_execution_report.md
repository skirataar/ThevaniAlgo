# Algorithm v0.1 - Test Execution Report

**Generated:** 2026-01-03 16:22:21

## Summary

- **Total Test Cases:** 30
- **Passed:** 30 ✅
- **Failed:** 0 ❌
- **Pass Rate:** 100.0%

---

## Detailed Results

### Test Case 1: TC-IAS-001 - IAS_v1 Hard Failure - Negative Amount

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Invoice amount must be positive`
- Actual Reason: `IAS validation failed: Invoice amount must be positive`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice amount must be positive`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (-1000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (-1000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 2: TC-IAS-002 - IAS_v1 Hard Failure - Invalid Date Range

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Due date must be after issue date`
- Actual Reason: `IAS validation failed: Due date must be after issue date; Invoice due date is in the past`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Due date must be after issue date; Invoice due date is in the past`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (5000.0) within acceptable limits; Due date is too soon (-2 days), minimum required: 7 days`

---

### Test Case 3: TC-IAS-003 - IAS_v1 Hard Failure - Expired Invoice

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Invoice due date is in the past`
- Actual Reason: `IAS validation failed: Invoice due date is in the past`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice due date is in the past`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (5000.0) within acceptable limits; Due date is too soon (-31 days), minimum required: 7 days`

---

### Test Case 4: TC-IAS-004 - IAS_v1 Hard Failure - Missing Required Fields

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Invoice missing required fields (invoice_number, invoice_id)`
- Actual Reason: `IAS validation failed: Invoice missing required fields (invoice_number, invoice_id)`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice missing required fields (invoice_number, invoice_id)`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 5: TC-IAS-005 - IAS_v1 Hard Failure - Missing Buyer Identifier

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Buyer must have buyer_id`
- Actual Reason: `IAS validation failed: Buyer must have buyer_id`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Buyer must have buyer_id`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 6: TC-IAS-006 - IAS_v1 Hard Failure - Invalid Currency

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Currency JPY not supported`
- Actual Reason: `IAS validation failed: Currency JPY not supported`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Currency JPY not supported`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 7: TC-IAS-007 - IAS_v1 Hard Failure - Amount Exceeds Maximum

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed: Invoice amount exceeds maximum threshold of 10000000.0`
- Actual Reason: `IAS validation failed: Invoice amount exceeds maximum threshold of 10000000.0`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice amount exceeds maximum threshold of 10000000.0`

**BRI_v1:**
- Risk Band: `HIGH`
- Reason: `Invoice amount (10000001.0) exceeds medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (10000001.0) exceeds maximum threshold (500000.0); Timing acceptable: 29 days until due date`

---

### Test Case 8: TC-IAS-008 - IAS_v1 Hard Failure - Multiple Validation Failures

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Actual Reason: `IAS validation failed: Invoice amount must be positive; Due date must be after issue date; Invoice due date is in the past; Invoice missing required fields (invoice_number, invoice_id); Buyer must have buyer_id; Currency XYZ not supported`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice amount must be positive; Due date must be after issue date; Invoice due date is in the past; Invoice missing required fields (invoice_number, invoice_id); Buyer must have buyer_id; Currency XYZ not supported`

**BRI_v1:**
- Risk Band: `HIGH`
- Reason: `Buyer missing both registration number and tax ID`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (-1000.0) within acceptable limits; Due date is too soon (-2 days), minimum required: 7 days`

---

### Test Case 9: TC-BRI-001 - BRI_v1 Risk Band - LOW Risk (Clean Buyer)

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 10: TC-BRI-002 - BRI_v1 Risk Band - LOW Risk Boundary

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (10000.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (10000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (10000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 11: TC-BRI-003 - BRI_v1 Risk Band - MEDIUM Risk (Just Above LOW)

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk`
- Actual Reason: `Buyer classified as MEDIUM risk: Invoice amount (10000.01) within medium risk threshold (100000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (10000.01) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (10000.01) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 12: TC-BRI-004 - BRI_v1 Risk Band - MEDIUM Risk (At Upper Boundary)

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk`
- Actual Reason: `Buyer classified as MEDIUM risk: Invoice amount (100000.0) within medium risk threshold (100000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (100000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (100000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 13: TC-BRI-005 - BRI_v1 Risk Band - HIGH Risk (Just Above MEDIUM)

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `HOLD`
- Actual: `HOLD`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as HIGH risk`
- Actual Reason: `Buyer classified as HIGH risk: Invoice amount (100000.01) exceeds medium risk threshold (100000.0) | Requires manual review`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `HIGH`
- Reason: `Invoice amount (100000.01) exceeds medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (100000.01) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 14: TC-BRI-006 - BRI_v1 Risk Band - HIGH Risk (Missing Identifiers)

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `HOLD`
- Actual: `HOLD`

**Reason Match:** ✅
- Expected Keyword: `Buyer missing both registration number and tax ID`
- Actual Reason: `Buyer classified as HIGH risk: Buyer missing both registration number and tax ID | Requires manual review`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `HIGH`
- Reason: `Buyer missing both registration number and tax ID`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 15: TC-BRI-007 - BRI_v1 Risk Band - MEDIUM Risk (One Identifier)

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk`
- Actual Reason: `Buyer classified as MEDIUM risk: Invoice amount (50000.0) within medium risk threshold (100000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (50000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (50000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 16: TC-BFE-001 - BFE_v1 HOLD Condition - Exposure Just Above Cap

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `BFE checks failed`
- Actual Reason: `BFE checks failed: Total exposure (500001.0) exceeds maximum threshold (500000.0); Timing acceptable: 29 days until due date`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (100000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (500001.0) exceeds maximum threshold (500000.0); Timing acceptable: 29 days until due date`

---

### Test Case 17: TC-BFE-002 - BFE_v1 PASSED - Exposure Exactly at Cap

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `HOLD`
- Actual: `HOLD`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk with high exposure`
- Actual Reason: `Buyer classified as MEDIUM risk with high exposure: 500000.0 | Requires manual review`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (100000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (500000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 18: TC-BFE-003 - BFE_v1 HOLD Condition - Timing Too Soon

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `BFE checks failed`
- Actual Reason: `BFE checks failed: Total exposure (5000.0) within acceptable limits; Due date is too soon (3 days), minimum required: 7 days`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (5000.0) within acceptable limits; Due date is too soon (3 days), minimum required: 7 days`

---

### Test Case 19: TC-BFE-004 - BFE_v1 PASSED - Timing Exactly at Minimum

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 7 days until due date`

---

### Test Case 20: TC-BFE-005 - BFE_v1 HOLD Condition - Timing Too Far

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `BFE checks failed`
- Actual Reason: `BFE checks failed: Total exposure (5000.0) within acceptable limits; Due date is too far (366 days), maximum allowed: 365 days`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (5000.0) within acceptable limits; Due date is too far (366 days), maximum allowed: 365 days`

---

### Test Case 21: TC-BFE-006 - BFE_v1 PASSED - Timing Exactly at Maximum

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 364 days until due date`

---

### Test Case 22: TC-UDF-001 - UDF_v1 Decision Precedence - IAS REJECT + BRI LOW → REJECT

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed`
- Actual Reason: `IAS validation failed: Invoice amount must be positive`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice amount must be positive`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (0.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (0.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 23: TC-UDF-002 - UDF_v1 Decision Precedence - IAS PASS + BRI HIGH → HOLD

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `HOLD`
- Actual: `HOLD`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as HIGH risk`
- Actual Reason: `Buyer classified as HIGH risk: Invoice amount (200000.0) exceeds medium risk threshold (100000.0) | Requires manual review`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `HIGH`
- Reason: `Invoice amount (200000.0) exceeds medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (200000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 24: TC-UDF-003 - UDF_v1 Decision Precedence - MEDIUM + High Exposure → HOLD

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `HOLD`
- Actual: `HOLD`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk with high exposure`
- Actual Reason: `Buyer classified as MEDIUM risk with high exposure: 450001.0 | Requires manual review`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (50000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (450001.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 25: TC-UDF-004 - UDF_v1 Decision Precedence - All Engines Clean → APPROVE

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 26: TC-UDF-005 - UDF_v1 Decision Precedence - MEDIUM + Low Exposure → APPROVE

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk`
- Actual Reason: `Buyer classified as MEDIUM risk: Invoice amount (50000.0) within medium risk threshold (100000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (50000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (150000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---

### Test Case 27: TC-HAPPY-001 - Happy Path - Golden Case

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (7500.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (7500.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (7500.0) within acceptable limits; Timing acceptable: 44 days until due date`

---

### Test Case 28: TC-EXPLAIN-001 - Explainability Integrity - All Reasons Present

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as MEDIUM risk`
- Actual Reason: `Buyer classified as MEDIUM risk: Invoice amount (25000.0) within medium risk threshold (100000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `MEDIUM`
- Reason: `Invoice amount (25000.0) within medium risk threshold (100000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (75000.0) within acceptable limits; Timing acceptable: 59 days until due date`

---

### Test Case 29: TC-EXPLAIN-002 - Explainability Integrity - Multiple Failure Reasons

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `REJECT`
- Actual: `REJECT`

**Reason Match:** ✅
- Expected Keyword: `IAS validation failed`
- Actual Reason: `IAS validation failed: Invoice amount must be positive; Due date must be after issue date; Invoice due date is in the past; Invoice missing required fields (invoice_number, invoice_id); Buyer must have buyer_id; Currency XYZ not supported`

**Engine Outputs:**

**IAS_v1:**
- Passed: `False`
- Reason: `Invoice amount must be positive; Due date must be after issue date; Invoice due date is in the past; Invoice missing required fields (invoice_number, invoice_id); Buyer must have buyer_id; Currency XYZ not supported`

**BRI_v1:**
- Risk Band: `HIGH`
- Reason: `Buyer missing both registration number and tax ID`

**BFE_v1:**
- Passed: `False`
- Reason: `Total exposure (-5000.0) within acceptable limits; Due date is too soon (-2 days), minimum required: 7 days`

---

### Test Case 30: TC-UDF-006 - UDF_v1 Fallback - Unknown Risk Band

**Status:** ✅ PASS

**Final Decision:** ✅
- Expected: `APPROVE`
- Actual: `APPROVE`

**Reason Match:** ✅
- Expected Keyword: `Buyer classified as LOW risk`
- Actual Reason: `Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed`

**Engine Outputs:**

**IAS_v1:**
- Passed: `True`
- Reason: `All validation checks passed`

**BRI_v1:**
- Risk Band: `LOW`
- Reason: `Invoice amount (5000.0) within low risk threshold (10000.0)`

**BFE_v1:**
- Passed: `True`
- Reason: `Total exposure (5000.0) within acceptable limits; Timing acceptable: 29 days until due date`

---
