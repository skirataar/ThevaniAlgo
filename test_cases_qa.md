# Algorithm v0.1 - Comprehensive Test Cases

## Test Case 1: IAS_v1 Hard Failure - Negative Amount
**TEST CASE ID:** TC-IAS-001  
**Description:** Invoice with negative amount should fail IAS validation and result in REJECT

**Input:**
- Seller: Not applicable (not validated in current implementation)
- Buyer:
  - buyer_id: "BUYER-001"
  - name: "Test Corp"
  - registration_number: "REG-12345"
  - tax_id: "TAX-12345"
- Invoice:
  - invoice_id: "INV-001"
  - invoice_number: "INV-2024-001"
  - amount: -1000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-001"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Invoice amount must be positive"
- BRI_v1:
  - Risk Band: HIGH (due to missing identifiers check, but will be overridden by IAS failure)
  - Reasons: "Buyer missing both registration number and tax ID" (Note: This is incorrect classification, but BRI runs regardless)
- BFE_v1:
  - Decision: FAILED (if timing/exposure checks fail) or PASSED (if they pass)
  - Reasons: Depends on timing and exposure values

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Invoice amount must be positive"

**Notes:**
- IAS failure takes precedence - UDF_v1 should REJECT immediately
- BRI_v1 and BFE_v1 may still execute but their outputs are irrelevant once IAS fails

---

## Test Case 2: IAS_v1 Hard Failure - Invalid Date Range
**TEST CASE ID:** TC-IAS-002  
**Description:** Invoice where due date is before or equal to issue date should fail IAS validation

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-002"
  - name: "Test Corp 2"
  - registration_number: "REG-67890"
  - tax_id: "TAX-67890"
- Invoice:
  - invoice_id: "INV-002"
  - invoice_number: "INV-2024-002"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-02-01 10:00:00
  - due_date: 2024-01-01 10:00:00 (before issue date)
  - buyer_id: "BUYER-002"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Due date must be after issue date"
- BRI_v1:
  - Risk Band: LOW (amount <= 10000.0)
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: FAILED (due date in past violates timing check)
  - Reasons: "Due date is too soon (X days), minimum required: 7 days" OR "Timing acceptable: X days until due date" (depending on current date)

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Due date must be after issue date"

**Notes:**
- IAS date validation takes precedence
- Even if BFE also fails, IAS failure is checked first in UDF_v1

---

## Test Case 3: IAS_v1 Hard Failure - Expired Invoice
**TEST CASE ID:** TC-IAS-003  
**Description:** Invoice with due date in the past should fail IAS validation

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-003"
  - name: "Test Corp 3"
  - registration_number: "REG-11111"
  - tax_id: "TAX-11111"
- Invoice:
  - invoice_id: "INV-003"
  - invoice_number: "INV-2024-003"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2023-12-01 10:00:00 (in the past)
  - buyer_id: "BUYER-003"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Invoice due date is in the past"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: FAILED (timing check will fail)
  - Reasons: "Due date is too soon (X days), minimum required: 7 days"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Invoice due date is in the past"

**Notes:**
- IAS checks expiration before BFE timing checks
- Both engines may flag the same issue, but IAS takes precedence

---

## Test Case 4: IAS_v1 Hard Failure - Missing Required Fields
**TEST CASE ID:** TC-IAS-004  
**Description:** Invoice missing invoice_number or invoice_id should fail IAS validation

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-004"
  - name: "Test Corp 4"
  - registration_number: "REG-22222"
  - tax_id: "TAX-22222"
- Invoice:
  - invoice_id: "" (empty)
  - invoice_number: "INV-2024-004"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-004"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Invoice missing required fields (invoice_number, invoice_id)"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED (assuming valid dates and exposure)
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Invoice missing required fields (invoice_number, invoice_id)"

**Notes:**
- Empty string fails the `not invoice.invoice_id` check

---

## Test Case 5: IAS_v1 Hard Failure - Missing Buyer Identifier
**TEST CASE ID:** TC-IAS-005  
**Description:** Buyer without buyer_id should fail IAS validation

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "" (empty)
  - name: "Test Corp 5"
  - registration_number: "REG-33333"
  - tax_id: "TAX-33333"
- Invoice:
  - invoice_id: "INV-005"
  - invoice_number: "INV-2024-005"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: ""
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Buyer must have buyer_id"
- BRI_v1:
  - Risk Band: LOW (based on amount only)
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Buyer must have buyer_id"

**Notes:**
- Buyer identifier is mandatory in IAS_v1

---

## Test Case 6: IAS_v1 Hard Failure - Invalid Currency
**TEST CASE ID:** TC-IAS-006  
**Description:** Invoice with unsupported currency should fail IAS validation

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-006"
  - name: "Test Corp 6"
  - registration_number: "REG-44444"
  - tax_id: "TAX-44444"
- Invoice:
  - invoice_id: "INV-006"
  - invoice_number: "INV-2024-006"
  - amount: 5000.0
  - currency: "JPY" (not in valid list)
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-006"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Currency JPY not supported"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Currency JPY not supported"

**Notes:**
- Valid currencies: USD, EUR, GBP, INR only

---

## Test Case 7: IAS_v1 Hard Failure - Amount Exceeds Maximum
**TEST CASE ID:** TC-IAS-007  
**Description:** Invoice amount exceeding 10M should fail IAS validation

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-007"
  - name: "Test Corp 7"
  - registration_number: "REG-55555"
  - tax_id: "TAX-55555"
- Invoice:
  - invoice_id: "INV-007"
  - invoice_number: "INV-2024-007"
  - amount: 10000001.0 (exceeds 10M)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-007"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Invoice amount exceeds maximum threshold of 10000000.0"
- BRI_v1:
  - Risk Band: HIGH (amount > 100000.0)
  - Reasons: "Invoice amount (10000001.0) exceeds medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: FAILED (exposure will exceed 500K)
  - Reasons: "Total exposure (10000001.0) exceeds maximum threshold (500000.0)"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Invoice amount exceeds maximum threshold of 10000000.0"

**Notes:**
- IAS maximum amount check: 10000000.0
- Multiple engines may flag this, but IAS takes precedence

---

## Test Case 8: IAS_v1 Hard Failure - Multiple Validation Failures
**TEST CASE ID:** TC-IAS-008  
**Description:** Invoice with multiple IAS validation failures should report all reasons

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "" (empty)
  - name: "Test Corp 8"
  - registration_number: None
  - tax_id: None
- Invoice:
  - invoice_id: "" (empty)
  - invoice_number: "" (empty)
  - amount: -1000.0
  - currency: "XYZ" (invalid)
  - issue_date: 2024-02-01 10:00:00
  - due_date: 2024-01-01 10:00:00 (before issue date)
  - buyer_id: ""
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Invoice amount must be positive; Due date must be after issue date; Invoice missing required fields (invoice_number, invoice_id); Buyer must have buyer_id; Currency XYZ not supported" (all failures concatenated with "; ")
- BRI_v1:
  - Risk Band: HIGH (missing both registration and tax_id)
  - Reasons: "Buyer missing both registration number and tax ID"
- BFE_v1:
  - Decision: FAILED (timing check)
  - Reasons: "Due date is too soon (X days), minimum required: 7 days"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
- Reasons: "IAS validation failed: Invoice amount must be positive; Due date must be after issue date; Invoice missing required fields (invoice_number, invoice_id); Buyer must have buyer_id; Currency XYZ not supported"

**Notes:**
- IAS collects all failures and reports them in reason string
- All validation checks are performed regardless of early failures

---

## Test Case 9: BRI_v1 Risk Band - LOW Risk (Clean Buyer)
**TEST CASE ID:** TC-BRI-001  
**Description:** Buyer with identifiers and small invoice amount should be classified as LOW risk

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-009"
  - name: "Clean Corp"
  - registration_number: "REG-99999"
  - tax_id: "TAX-99999"
- Invoice:
  - invoice_id: "INV-009"
  - invoice_number: "INV-2024-009"
  - amount: 5000.0 (<= 10000.0)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-009"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED (passed=True)
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
- Reasons: "Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed"

**Notes:**
- LOW risk threshold: <= 10000.0
- Requires buyer to have at least one identifier (registration_number or tax_id)

---

## Test Case 10: BRI_v1 Risk Band - LOW Risk Boundary (Exactly at Threshold)
**TEST CASE ID:** TC-BRI-002  
**Description:** Invoice amount exactly at LOW risk threshold (10000.0) should be classified as LOW

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-010"
  - name: "Boundary Corp"
  - registration_number: "REG-10101"
  - tax_id: "TAX-10101"
- Invoice:
  - invoice_id: "INV-010"
  - invoice_number: "INV-2024-010"
  - amount: 10000.0 (exactly at threshold)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-010"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (10000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (10000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
- Reasons: "Buyer classified as LOW risk: Invoice amount (10000.0) within low risk threshold (10000.0) | All checks passed"

**Notes:**
- Boundary condition: amount <= 10000.0 is LOW (inclusive)

---

## Test Case 11: BRI_v1 Risk Band - MEDIUM Risk (Just Above LOW Threshold)
**TEST CASE ID:** TC-BRI-003  
**Description:** Invoice amount just above LOW threshold should be classified as MEDIUM risk

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-011"
  - name: "Medium Corp"
  - registration_number: "REG-20202"
  - tax_id: "TAX-20202"
- Invoice:
  - invoice_id: "INV-011"
  - invoice_number: "INV-2024-011"
  - amount: 10000.01 (just above LOW threshold)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-011"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (10000.01) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (10000.01) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE (assuming exposure < 400K)
  - Reasons: "Buyer classified as MEDIUM risk: Invoice amount (10000.01) within medium risk threshold (100000.0) | All checks passed"

**Notes:**
- MEDIUM risk: 10000.0 < amount <= 100000.0

---

## Test Case 12: BRI_v1 Risk Band - MEDIUM Risk (At Upper Boundary)
**TEST CASE ID:** TC-BRI-004  
**Description:** Invoice amount exactly at MEDIUM risk upper threshold (100000.0) should be classified as MEDIUM

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-012"
  - name: "Medium Upper Corp"
  - registration_number: "REG-30303"
  - tax_id: "TAX-30303"
- Invoice:
  - invoice_id: "INV-012"
  - invoice_number: "INV-2024-012"
  - amount: 100000.0 (exactly at MEDIUM upper threshold)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-012"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (100000.0) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (100000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE (assuming exposure < 400K)
  - Reasons: "Buyer classified as MEDIUM risk: Invoice amount (100000.0) within medium risk threshold (100000.0) | All checks passed"

**Notes:**
- Boundary condition: amount <= 100000.0 is MEDIUM (inclusive)

---

## Test Case 13: BRI_v1 Risk Band - HIGH Risk (Just Above MEDIUM Threshold)
**TEST CASE ID:** TC-BRI-005  
**Description:** Invoice amount just above MEDIUM threshold should be classified as HIGH risk

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-013"
  - name: "High Risk Corp"
  - registration_number: "REG-40404"
  - tax_id: "TAX-40404"
- Invoice:
  - invoice_id: "INV-013"
  - invoice_number: "INV-2024-013"
  - amount: 100000.01 (just above MEDIUM threshold)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-013"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: HIGH
  - Reasons: "Invoice amount (100000.01) exceeds medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (100000.01) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: HOLD
  - Reasons: "Buyer classified as HIGH risk: Invoice amount (100000.01) exceeds medium risk threshold (100000.0) | Requires manual review"

**Notes:**
- HIGH risk: amount > 100000.0
- HIGH risk always results in HOLD

---

## Test Case 14: BRI_v1 Risk Band - HIGH Risk (Missing Identifiers)
**TEST CASE ID:** TC-BRI-006  
**Description:** Buyer missing both registration_number and tax_id should be classified as HIGH risk regardless of amount

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-014"
  - name: "No ID Corp"
  - registration_number: None
  - tax_id: None
- Invoice:
  - invoice_id: "INV-014"
  - invoice_number: "INV-2024-014"
  - amount: 5000.0 (small amount, but missing IDs)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-014"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: HIGH
  - Reasons: "Buyer missing both registration number and tax ID"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: HOLD
  - Reasons: "Buyer classified as HIGH risk: Buyer missing both registration number and tax ID | Requires manual review"

**Notes:**
- Missing identifiers override amount-based classification
- Empty strings are treated as missing (after strip())

---

## Test Case 15: BRI_v1 Risk Band - MEDIUM Risk (Buyer with One Identifier)
**TEST CASE ID:** TC-BRI-007  
**Description:** Buyer with only registration_number (no tax_id) and medium amount should be classified as MEDIUM

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-015"
  - name: "Partial ID Corp"
  - registration_number: "REG-50505"
  - tax_id: None
- Invoice:
  - invoice_id: "INV-015"
  - invoice_number: "INV-2024-015"
  - amount: 50000.0 (MEDIUM range)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-015"
  - seller_id: "SELLER-001"
  - status: "pending"

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (50000.0) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (50000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE (assuming exposure < 400K)
  - Reasons: "Buyer classified as MEDIUM risk: Invoice amount (50000.0) within medium risk threshold (100000.0) | All checks passed"

**Notes:**
- Having at least one identifier (registration_number OR tax_id) allows amount-based classification
- Only missing BOTH identifiers triggers HIGH risk

---

## Test Case 16: BFE_v1 HOLD Condition - Exposure Just Above Cap
**TEST CASE ID:** TC-BFE-001  
**Description:** Total exposure exceeding 500K should fail BFE and result in REJECT

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-016"
  - name: "High Exposure Corp"
  - registration_number: "REG-60606"
  - tax_id: "TAX-60606"
- Invoice:
  - invoice_id: "INV-016"
  - invoice_number: "INV-2024-016"
  - amount: 100000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-016"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 400001.0 (total = 500001.0, exceeds 500K)

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (100000.0) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Total exposure (500001.0) exceeds maximum threshold (500000.0); Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
  - Reasons: "BFE checks failed: Total exposure (500001.0) exceeds maximum threshold (500000.0); Timing acceptable: 31 days until due date"

**Notes:**
- BFE exposure threshold: 500000.0 (exclusive, > 500K fails)
- BFE failure results in REJECT (not HOLD)

---

## Test Case 17: BFE_v1 PASSED - Exposure Exactly at Cap
**TEST CASE ID:** TC-BFE-002  
**Description:** Total exposure exactly at 500K should pass BFE exposure check

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-017"
  - name: "At Cap Corp"
  - registration_number: "REG-70707"
  - tax_id: "TAX-70707"
- Invoice:
  - invoice_id: "INV-017"
  - invoice_number: "INV-2024-017"
  - amount: 100000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-017"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 400000.0 (total = 500000.0, exactly at cap)

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (100000.0) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED (passed=True)
  - Reasons: "Total exposure (500000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: HOLD (exposure = 500K, which is 100% of max, exceeds 80% threshold of 400K)
  - Reasons: "Buyer classified as MEDIUM risk with high exposure: 500000.0 | Requires manual review"

**Notes:**
- BFE threshold: <= 500000.0 passes (inclusive)
- UDF_v1 checks if exposure > 400000.0 (80% of 500K) for MEDIUM risk → HOLD

---

## Test Case 18: BFE_v1 HOLD Condition - Timing Too Soon
**TEST CASE ID:** TC-BFE-003  
**Description:** Invoice due date less than 7 days away should fail BFE timing check

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-018"
  - name: "Short Term Corp"
  - registration_number: "REG-80808"
  - tax_id: "TAX-80808"
- Invoice:
  - invoice_id: "INV-018"
  - invoice_number: "INV-2024-018"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-01-05 10:00:00 (4 days away, less than 7)
  - buyer_id: "BUYER-018"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Total exposure (5000.0) within acceptable limits; Due date is too soon (4 days), minimum required: 7 days"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
  - Reasons: "BFE checks failed: Total exposure (5000.0) within acceptable limits; Due date is too soon (4 days), minimum required: 7 days"

**Notes:**
- BFE timing minimum: 7 days (exclusive, < 7 fails)
- BFE failure results in REJECT

---

## Test Case 19: BFE_v1 PASSED - Timing Exactly at Minimum
**TEST CASE ID:** TC-BFE-004  
**Description:** Invoice due date exactly 7 days away should pass BFE timing check

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-019"
  - name: "Min Timing Corp"
  - registration_number: "REG-90909"
  - tax_id: "TAX-90909"
- Invoice:
  - invoice_id: "INV-019"
  - invoice_number: "INV-2024-019"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-01-08 10:00:00 (exactly 7 days away)
  - buyer_id: "BUYER-019"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 7 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
  - Reasons: "Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed"

**Notes:**
- BFE timing minimum: >= 7 days passes (inclusive)

---

## Test Case 20: BFE_v1 HOLD Condition - Timing Too Far
**TEST CASE ID:** TC-BFE-005  
**Description:** Invoice due date more than 365 days away should fail BFE timing check

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-020"
  - name: "Long Term Corp"
  - registration_number: "REG-10101"
  - tax_id: "TAX-10101"
- Invoice:
  - invoice_id: "INV-020"
  - invoice_number: "INV-2024-020"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2025-01-10 10:00:00 (more than 365 days away)
  - buyer_id: "BUYER-020"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Total exposure (5000.0) within acceptable limits; Due date is too far (374 days), maximum allowed: 365 days"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
  - Reasons: "BFE checks failed: Total exposure (5000.0) within acceptable limits; Due date is too far (374 days), maximum allowed: 365 days"

**Notes:**
- BFE timing maximum: 365 days (exclusive, > 365 fails)

---

## Test Case 21: BFE_v1 PASSED - Timing Exactly at Maximum
**TEST CASE ID:** TC-BFE-006  
**Description:** Invoice due date exactly 365 days away should pass BFE timing check

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-021"
  - name: "Max Timing Corp"
  - registration_number: "REG-11111"
  - tax_id: "TAX-11111"
- Invoice:
  - invoice_id: "INV-021"
  - invoice_number: "INV-2024-021"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2025-01-01 10:00:00 (exactly 365 days away)
  - buyer_id: "BUYER-021"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 365 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
  - Reasons: "Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed"

**Notes:**
- BFE timing maximum: <= 365 days passes (inclusive)

---

## Test Case 22: UDF_v1 Decision Precedence - IAS REJECT + BRI LOW → REJECT
**TEST CASE ID:** TC-UDF-001  
**Description:** IAS failure should result in REJECT even if BRI classifies as LOW risk

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-022"
  - name: "Precedence Test Corp"
  - registration_number: "REG-12121"
  - tax_id: "TAX-12121"
- Invoice:
  - invoice_id: "INV-022"
  - invoice_number: "INV-2024-022"
  - amount: 0.0 (IAS failure)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-022"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED (passed=False)
  - Reasons: "Invoice amount must be positive"
- BRI_v1:
  - Risk Band: LOW (amount would be 0.0, but IAS fails first)
  - Reasons: "Invoice amount (0.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (0.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
  - Reasons: "IAS validation failed: Invoice amount must be positive"

**Notes:**
- UDF_v1 Rule 1: IAS failure → REJECT (checked first)
- BRI and BFE outputs are irrelevant once IAS fails

---

## Test Case 23: UDF_v1 Decision Precedence - IAS PASS + BRI HIGH → HOLD
**TEST CASE ID:** TC-UDF-002  
**Description:** HIGH risk buyer should result in HOLD even if IAS and BFE pass

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-023"
  - name: "High Risk Precedence Corp"
  - registration_number: "REG-13131"
  - tax_id: "TAX-13131"
- Invoice:
  - invoice_id: "INV-023"
  - invoice_number: "INV-2024-023"
  - amount: 200000.0 (HIGH risk)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-023"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: HIGH
  - Reasons: "Invoice amount (200000.0) exceeds medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (200000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: HOLD
  - Reasons: "Buyer classified as HIGH risk: Invoice amount (200000.0) exceeds medium risk threshold (100000.0) | Requires manual review"

**Notes:**
- UDF_v1 Rule 3: BRI HIGH → HOLD (checked after IAS and BFE pass)
- HIGH risk always results in HOLD, not REJECT

---

## Test Case 24: UDF_v1 Decision Precedence - IAS PASS + BRI MEDIUM + BFE HOLD → HOLD
**TEST CASE ID:** TC-UDF-003  
**Description:** MEDIUM risk with high exposure (> 400K) should result in HOLD

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-024"
  - name: "Medium High Exposure Corp"
  - registration_number: "REG-14141"
  - tax_id: "TAX-14141"
- Invoice:
  - invoice_id: "INV-024"
  - invoice_number: "INV-2024-024"
  - amount: 50000.0 (MEDIUM risk)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-024"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 400001.0 (total = 450001.0, > 400K threshold)

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (50000.0) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED (exposure 450001.0 < 500K, so passes)
  - Reasons: "Total exposure (450001.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: HOLD
  - Reasons: "Buyer classified as MEDIUM risk with high exposure: 450001.0 | Requires manual review"

**Notes:**
- UDF_v1 Rule 4: MEDIUM risk + exposure > 400000.0 (80% of 500K) → HOLD
- BFE passes (450K < 500K), but UDF_v1 checks exposure separately for MEDIUM risk

---

## Test Case 25: UDF_v1 Decision Precedence - All Engines Clean → APPROVE
**TEST CASE ID:** TC-UDF-004  
**Description:** All engines passing with LOW risk should result in APPROVE

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-025"
  - name: "Clean Approval Corp"
  - registration_number: "REG-15151"
  - tax_id: "TAX-15151"
- Invoice:
  - invoice_id: "INV-025"
  - invoice_number: "INV-2024-025"
  - amount: 5000.0 (LOW risk)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-025"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (5000.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
  - Reasons: "Buyer classified as LOW risk: Invoice amount (5000.0) within low risk threshold (10000.0) | All checks passed"

**Notes:**
- UDF_v1 Rule 5: LOW risk → APPROVE
- This is the happy path

---

## Test Case 26: UDF_v1 Decision Precedence - IAS PASS + BRI MEDIUM + Low Exposure → APPROVE
**TEST CASE ID:** TC-UDF-005  
**Description:** MEDIUM risk with low exposure (< 400K) should result in APPROVE

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-026"
  - name: "Medium Low Exposure Corp"
  - registration_number: "REG-16161"
  - tax_id: "TAX-16161"
- Invoice:
  - invoice_id: "INV-026"
  - invoice_number: "INV-2024-026"
  - amount: 50000.0 (MEDIUM risk)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-026"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 100000.0 (total = 150000.0, < 400K threshold)

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (50000.0) within medium risk threshold (100000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (150000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
  - Reasons: "Buyer classified as MEDIUM risk: Invoice amount (50000.0) within medium risk threshold (100000.0) | All checks passed"

**Notes:**
- UDF_v1 Rule 4: MEDIUM risk + exposure <= 400000.0 → APPROVE
- Exposure threshold for MEDIUM risk HOLD: > 400000.0

---

## Test Case 27: Happy Path - Golden Case (Fully Verified)
**TEST CASE ID:** TC-HAPPY-001  
**Description:** Complete happy path with all validations passing

**Input:**
- Seller: Not applicable (Note: Seller verification not implemented in current code)
- Buyer:
  - buyer_id: "BUYER-HAPPY"
  - name: "Golden Path Corp"
  - registration_number: "REG-GOLDEN"
  - tax_id: "TAX-GOLDEN"
- Invoice:
  - invoice_id: "INV-HAPPY"
  - invoice_number: "INV-2024-HAPPY"
  - amount: 7500.0 (LOW risk)
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-15 10:00:00 (45 days, well within limits)
  - buyer_id: "BUYER-HAPPY"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: LOW
  - Reasons: "Invoice amount (7500.0) within low risk threshold (10000.0)"
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (7500.0) within acceptable limits; Timing acceptable: 45 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
  - Reasons: "Buyer classified as LOW risk: Invoice amount (7500.0) within low risk threshold (10000.0) | All checks passed"

**Notes:**
- All engines pass
- LOW risk classification
- Clean explanation with plain English reasons
- **AMBIGUITY FLAGGED:** Test prompt mentions "Fully verified seller" and "Buyer accepted invoice" - these validations are NOT implemented in current code. Seller verification and buyer acceptance checks are missing.

---

## Test Case 28: Explainability Integrity - All Reasons Present
**TEST CASE ID:** TC-EXPLAIN-001  
**Description:** Verify all engines provide non-empty, plain-English reasons

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-EXPLAIN"
  - name: "Explainability Test Corp"
  - registration_number: "REG-EXPLAIN"
  - tax_id: "TAX-EXPLAIN"
- Invoice:
  - invoice_id: "INV-EXPLAIN"
  - invoice_number: "INV-2024-EXPLAIN"
  - amount: 25000.0
  - currency: "EUR"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-03-01 10:00:00 (60 days)
  - buyer_id: "BUYER-EXPLAIN"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 50000.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed" (non-empty, plain English)
- BRI_v1:
  - Risk Band: MEDIUM
  - Reasons: "Invoice amount (25000.0) within medium risk threshold (100000.0)" (non-empty, plain English, maps to rule)
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (75000.0) within acceptable limits; Timing acceptable: 60 days until due date" (non-empty, plain English, maps to rules)

**Expected Final Decision (UDF_v1):**
- Decision: APPROVE
  - Reasons: "Buyer classified as MEDIUM risk: Invoice amount (25000.0) within medium risk threshold (100000.0) | All checks passed" (non-empty, plain English, maps to decision tree)

**Notes:**
- All reasons must be non-empty strings
- All reasons must be plain English (no codes, no scores)
- All reasons must map directly to rule checks
- UDF_v1 reasons must explain final decision clearly

---

## Test Case 29: Explainability Integrity - Multiple Failure Reasons
**TEST CASE ID:** TC-EXPLAIN-002  
**Description:** Verify multiple IAS failures are all reported in reason string

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "" (empty)
  - name: "Multi Fail Corp"
  - registration_number: None
  - tax_id: None
- Invoice:
  - invoice_id: "" (empty)
  - invoice_number: "" (empty)
  - amount: -5000.0
  - currency: "XYZ" (invalid)
  - issue_date: 2024-02-01 10:00:00
  - due_date: 2024-01-01 10:00:00 (before issue date)
  - buyer_id: ""
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: FAILED
  - Reasons: Must contain ALL of the following (separated by "; "):
    - "Invoice amount must be positive"
    - "Due date must be after issue date"
    - "Invoice missing required fields (invoice_number, invoice_id)"
    - "Buyer must have buyer_id"
    - "Currency XYZ not supported"
- BRI_v1:
  - Risk Band: HIGH
  - Reasons: "Buyer missing both registration number and tax ID"
- BFE_v1:
  - Decision: FAILED
  - Reasons: "Due date is too soon (X days), minimum required: 7 days" (or similar timing failure)

**Expected Final Decision (UDF_v1):**
- Decision: REJECT
  - Reasons: "IAS validation failed: [all IAS failure reasons concatenated with '; ']"

**Notes:**
- IAS must report ALL validation failures, not just the first one
- Reason string should be comprehensive and auditable

---

## Test Case 30: UDF_v1 Fallback - Unknown Risk Band
**TEST CASE ID:** TC-UDF-006  
**Description:** UDF_v1 fallback when risk band is None or unexpected value

**Input:**
- Seller: Not applicable
- Buyer:
  - buyer_id: "BUYER-FALLBACK"
  - name: "Fallback Test Corp"
  - registration_number: "REG-FALLBACK"
  - tax_id: "TAX-FALLBACK"
- Invoice:
  - invoice_id: "INV-FALLBACK"
  - invoice_number: "INV-2024-FALLBACK"
  - amount: 5000.0
  - currency: "USD"
  - issue_date: 2024-01-01 10:00:00
  - due_date: 2024-02-01 10:00:00
  - buyer_id: "BUYER-FALLBACK"
  - seller_id: "SELLER-001"
  - status: "pending"
- Existing Exposure: 0.0
- **Note:** This test requires manually setting bri_result.risk_band = None to test fallback

**Expected Engine Outputs:**
- IAS_v1:
  - Decision: PASSED
  - Reasons: "All validation checks passed"
- BRI_v1:
  - Risk Band: None (manually set for test)
  - Reasons: (normal BRI reason, but risk_band is None)
- BFE_v1:
  - Decision: PASSED
  - Reasons: "Total exposure (5000.0) within acceptable limits; Timing acceptable: 31 days until due date"

**Expected Final Decision (UDF_v1):**
- Decision: HOLD
  - Reasons: "Unable to determine risk band - requires manual review"

**Notes:**
- UDF_v1 Rule 6: Fallback when risk_band is None or doesn't match any condition
- This should not happen in normal operation, but fallback exists

---

## AMBIGUITIES AND MISSING FEATURES

The following features mentioned in the test prompt are NOT implemented in the current code:

1. **Seller Authenticity Checks:**
   - KYC verification
   - GST validation
   - Bank account verification
   - Historical defaults tracking
   - Seller verification status

2. **Buyer Acceptance:**
   - "Buyer has not accepted invoice" check
   - Invoice acceptance status validation

3. **Buyer Risk Factors:**
   - "Buyer with minor delays" classification
   - "Buyer with disputes / long delays" classification
   - Historical payment behavior tracking

**Recommendation:** These features should be flagged as ambiguities. The current implementation does not validate seller authenticity or buyer acceptance. If these are required, they should be added to IAS_v1 or a new validation step.

---

## TEST EXECUTION SUMMARY

**Total Test Cases:** 30

**By Category:**
- IAS_v1 Hard Failures: 8 test cases (TC-IAS-001 through TC-IAS-008)
- BRI_v1 Risk Band Boundaries: 7 test cases (TC-BRI-001 through TC-BRI-007)
- BFE_v1 HOLD Conditions: 6 test cases (TC-BFE-001 through TC-BFE-006)
- UDF_v1 Decision Precedence: 6 test cases (TC-UDF-001 through TC-UDF-006)
- Happy Path: 1 test case (TC-HAPPY-001)
- Explainability Integrity: 2 test cases (TC-EXPLAIN-001, TC-EXPLAIN-002)

**Key Thresholds Tested:**
- IAS: Amount > 0, dates valid, currency in list, amount <= 10M
- BRI: LOW <= 10K, MEDIUM <= 100K, HIGH > 100K, missing IDs → HIGH
- BFE: Exposure <= 500K, timing 7-365 days
- UDF: IAS/BFE failure → REJECT, BRI HIGH → HOLD, MEDIUM + exposure > 400K → HOLD, LOW → APPROVE


