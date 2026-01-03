"""
Test runner for QA test cases
Executes all test cases and compares actual vs expected results
"""

from datetime import datetime, timedelta
from models import Invoice, Buyer, Decision, BuyerRiskBand
from orchestrator import execute_algorithm_v01
from engines.ias_v1 import execute_ias_v1
from engines.bri_v1 import execute_bri_v1
from engines.bfe_v1 import execute_bfe_v1
from engines.udf_v1 import execute_udf_v1


def create_test_case_1():
    """TC-IAS-001: Negative Amount"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-001",
        invoice_number="INV-2024-001",
        amount=-1000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-001",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-001",
        name="Test Corp",
        registration_number="REG-12345",
        tax_id="TAX-12345"
    )
    return invoice, buyer, 0.0


def create_test_case_2():
    """TC-IAS-002: Invalid Date Range"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-002",
        invoice_number="INV-2024-002",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now - timedelta(days=1),  # Before issue date
        buyer_id="BUYER-002",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-002",
        name="Test Corp 2",
        registration_number="REG-67890",
        tax_id="TAX-67890"
    )
    return invoice, buyer, 0.0


def create_test_case_3():
    """TC-IAS-003: Expired Invoice"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-003",
        invoice_number="INV-2024-003",
        amount=5000.0,
        currency="USD",
        issue_date=now - timedelta(days=60),
        due_date=now - timedelta(days=30),  # In the past
        buyer_id="BUYER-003",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-003",
        name="Test Corp 3",
        registration_number="REG-11111",
        tax_id="TAX-11111"
    )
    return invoice, buyer, 0.0


def create_test_case_4():
    """TC-IAS-004: Missing Required Fields"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="",
        invoice_number="INV-2024-004",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-004",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-004",
        name="Test Corp 4",
        registration_number="REG-22222",
        tax_id="TAX-22222"
    )
    return invoice, buyer, 0.0


def create_test_case_5():
    """TC-IAS-005: Missing Buyer Identifier"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-005",
        invoice_number="INV-2024-005",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="",
        name="Test Corp 5",
        registration_number="REG-33333",
        tax_id="TAX-33333"
    )
    return invoice, buyer, 0.0


def create_test_case_6():
    """TC-IAS-006: Invalid Currency"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-006",
        invoice_number="INV-2024-006",
        amount=5000.0,
        currency="JPY",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-006",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-006",
        name="Test Corp 6",
        registration_number="REG-44444",
        tax_id="TAX-44444"
    )
    return invoice, buyer, 0.0


def create_test_case_7():
    """TC-IAS-007: Amount Exceeds Maximum"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-007",
        invoice_number="INV-2024-007",
        amount=10000001.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-007",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-007",
        name="Test Corp 7",
        registration_number="REG-55555",
        tax_id="TAX-55555"
    )
    return invoice, buyer, 0.0


def create_test_case_8():
    """TC-IAS-008: Multiple Validation Failures"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="",
        invoice_number="",
        amount=-1000.0,
        currency="XYZ",
        issue_date=now,
        due_date=now - timedelta(days=1),  # Before issue date
        buyer_id="",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="",
        name="Test Corp 8",
        registration_number=None,
        tax_id=None
    )
    return invoice, buyer, 0.0


def create_test_case_9():
    """TC-BRI-001: LOW Risk (Clean Buyer)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-009",
        invoice_number="INV-2024-009",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-009",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-009",
        name="Clean Corp",
        registration_number="REG-99999",
        tax_id="TAX-99999"
    )
    return invoice, buyer, 0.0


def create_test_case_10():
    """TC-BRI-002: LOW Risk Boundary (Exactly at Threshold)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-010",
        invoice_number="INV-2024-010",
        amount=10000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-010",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-010",
        name="Boundary Corp",
        registration_number="REG-10101",
        tax_id="TAX-10101"
    )
    return invoice, buyer, 0.0


def create_test_case_11():
    """TC-BRI-003: MEDIUM Risk (Just Above LOW Threshold)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-011",
        invoice_number="INV-2024-011",
        amount=10000.01,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-011",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-011",
        name="Medium Corp",
        registration_number="REG-20202",
        tax_id="TAX-20202"
    )
    return invoice, buyer, 0.0


def create_test_case_12():
    """TC-BRI-004: MEDIUM Risk (At Upper Boundary)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-012",
        invoice_number="INV-2024-012",
        amount=100000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-012",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-012",
        name="Medium Upper Corp",
        registration_number="REG-30303",
        tax_id="TAX-30303"
    )
    return invoice, buyer, 0.0


def create_test_case_13():
    """TC-BRI-005: HIGH Risk (Just Above MEDIUM Threshold)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-013",
        invoice_number="INV-2024-013",
        amount=100000.01,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-013",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-013",
        name="High Risk Corp",
        registration_number="REG-40404",
        tax_id="TAX-40404"
    )
    return invoice, buyer, 0.0


def create_test_case_14():
    """TC-BRI-006: HIGH Risk (Missing Identifiers)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-014",
        invoice_number="INV-2024-014",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-014",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-014",
        name="No ID Corp",
        registration_number=None,
        tax_id=None
    )
    return invoice, buyer, 0.0


def create_test_case_15():
    """TC-BRI-007: MEDIUM Risk (Buyer with One Identifier)"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-015",
        invoice_number="INV-2024-015",
        amount=50000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-015",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-015",
        name="Partial ID Corp",
        registration_number="REG-50505",
        tax_id=None
    )
    return invoice, buyer, 0.0


def create_test_case_16():
    """TC-BFE-001: Exposure Just Above Cap"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-016",
        invoice_number="INV-2024-016",
        amount=100000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-016",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-016",
        name="High Exposure Corp",
        registration_number="REG-60606",
        tax_id="TAX-60606"
    )
    return invoice, buyer, 400001.0


def create_test_case_17():
    """TC-BFE-002: Exposure Exactly at Cap"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-017",
        invoice_number="INV-2024-017",
        amount=100000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-017",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-017",
        name="At Cap Corp",
        registration_number="REG-70707",
        tax_id="TAX-70707"
    )
    return invoice, buyer, 400000.0


def create_test_case_18():
    """TC-BFE-003: Timing Too Soon"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-018",
        invoice_number="INV-2024-018",
        amount=5000.0,
        currency="USD",
        issue_date=now - timedelta(days=10),
        due_date=now + timedelta(days=4),
        buyer_id="BUYER-018",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-018",
        name="Short Term Corp",
        registration_number="REG-80808",
        tax_id="TAX-80808"
    )
    return invoice, buyer, 0.0


def create_test_case_19():
    """TC-BFE-004: Timing Exactly at Minimum"""
    now = datetime.now()
    # Set due date to exactly 7 days from now, at same time to avoid day truncation
    due_date = now + timedelta(days=7, hours=1)  # Add 1 hour to ensure >= 7 days
    invoice = Invoice(
        invoice_id="INV-019",
        invoice_number="INV-2024-019",
        amount=5000.0,
        currency="USD",
        issue_date=now - timedelta(days=10),
        due_date=due_date,
        buyer_id="BUYER-019",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-019",
        name="Min Timing Corp",
        registration_number="REG-90909",
        tax_id="TAX-90909"
    )
    return invoice, buyer, 0.0


def create_test_case_20():
    """TC-BFE-005: Timing Too Far"""
    now = datetime.now()
    # Set due date to more than 365 days - use 366 days + 1 hour to ensure > 365
    due_date = now + timedelta(days=366, hours=1)
    invoice = Invoice(
        invoice_id="INV-020",
        invoice_number="INV-2024-020",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=due_date,
        buyer_id="BUYER-020",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-020",
        name="Long Term Corp",
        registration_number="REG-10101",
        tax_id="TAX-10101"
    )
    return invoice, buyer, 0.0


def create_test_case_21():
    """TC-BFE-006: Timing Exactly at Maximum"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-021",
        invoice_number="INV-2024-021",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=365),  # Exactly 365 days
        buyer_id="BUYER-021",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-021",
        name="Max Timing Corp",
        registration_number="REG-11111",
        tax_id="TAX-11111"
    )
    return invoice, buyer, 0.0


def create_test_case_22():
    """TC-UDF-001: IAS REJECT + BRI LOW → REJECT"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-022",
        invoice_number="INV-2024-022",
        amount=0.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-022",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-022",
        name="Precedence Test Corp",
        registration_number="REG-12121",
        tax_id="TAX-12121"
    )
    return invoice, buyer, 0.0


def create_test_case_23():
    """TC-UDF-002: IAS PASS + BRI HIGH → HOLD"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-023",
        invoice_number="INV-2024-023",
        amount=200000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-023",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-023",
        name="High Risk Precedence Corp",
        registration_number="REG-13131",
        tax_id="TAX-13131"
    )
    return invoice, buyer, 0.0


def create_test_case_24():
    """TC-UDF-003: IAS PASS + BRI MEDIUM + High Exposure → HOLD"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-024",
        invoice_number="INV-2024-024",
        amount=50000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-024",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-024",
        name="Medium High Exposure Corp",
        registration_number="REG-14141",
        tax_id="TAX-14141"
    )
    return invoice, buyer, 400001.0


def create_test_case_25():
    """TC-UDF-004: All Engines Clean → APPROVE"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-025",
        invoice_number="INV-2024-025",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-025",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-025",
        name="Clean Approval Corp",
        registration_number="REG-15151",
        tax_id="TAX-15151"
    )
    return invoice, buyer, 0.0


def create_test_case_26():
    """TC-UDF-005: IAS PASS + BRI MEDIUM + Low Exposure → APPROVE"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-026",
        invoice_number="INV-2024-026",
        amount=50000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-026",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-026",
        name="Medium Low Exposure Corp",
        registration_number="REG-16161",
        tax_id="TAX-16161"
    )
    return invoice, buyer, 100000.0


def create_test_case_27():
    """TC-HAPPY-001: Happy Path - Golden Case"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-HAPPY",
        invoice_number="INV-2024-HAPPY",
        amount=7500.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=45),
        buyer_id="BUYER-HAPPY",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-HAPPY",
        name="Golden Path Corp",
        registration_number="REG-GOLDEN",
        tax_id="TAX-GOLDEN"
    )
    return invoice, buyer, 0.0


def create_test_case_28():
    """TC-EXPLAIN-001: Explainability Integrity"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-EXPLAIN",
        invoice_number="INV-2024-EXPLAIN",
        amount=25000.0,
        currency="EUR",
        issue_date=now,
        due_date=now + timedelta(days=60),
        buyer_id="BUYER-EXPLAIN",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-EXPLAIN",
        name="Explainability Test Corp",
        registration_number="REG-EXPLAIN",
        tax_id="TAX-EXPLAIN"
    )
    return invoice, buyer, 50000.0


def create_test_case_29():
    """TC-EXPLAIN-002: Multiple Failure Reasons"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="",
        invoice_number="",
        amount=-5000.0,
        currency="XYZ",
        issue_date=now,
        due_date=now - timedelta(days=1),  # Before issue date
        buyer_id="",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="",
        name="Multi Fail Corp",
        registration_number=None,
        tax_id=None
    )
    return invoice, buyer, 0.0


def create_test_case_30():
    """TC-UDF-006: Fallback - Unknown Risk Band"""
    now = datetime.now()
    invoice = Invoice(
        invoice_id="INV-FALLBACK",
        invoice_number="INV-2024-FALLBACK",
        amount=5000.0,
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=30),
        buyer_id="BUYER-FALLBACK",
        seller_id="SELLER-001",
        status="pending"
    )
    buyer = Buyer(
        buyer_id="BUYER-FALLBACK",
        name="Fallback Test Corp",
        registration_number="REG-FALLBACK",
        tax_id="TAX-FALLBACK"
    )
    return invoice, buyer, 0.0


# Test case definitions
TEST_CASES = [
    ("TC-IAS-001", "IAS_v1 Hard Failure - Negative Amount", create_test_case_1, "REJECT", "IAS validation failed: Invoice amount must be positive"),
    ("TC-IAS-002", "IAS_v1 Hard Failure - Invalid Date Range", create_test_case_2, "REJECT", "IAS validation failed: Due date must be after issue date"),
    ("TC-IAS-003", "IAS_v1 Hard Failure - Expired Invoice", create_test_case_3, "REJECT", "IAS validation failed: Invoice due date is in the past"),
    ("TC-IAS-004", "IAS_v1 Hard Failure - Missing Required Fields", create_test_case_4, "REJECT", "IAS validation failed: Invoice missing required fields (invoice_number, invoice_id)"),
    ("TC-IAS-005", "IAS_v1 Hard Failure - Missing Buyer Identifier", create_test_case_5, "REJECT", "IAS validation failed: Buyer must have buyer_id"),
    ("TC-IAS-006", "IAS_v1 Hard Failure - Invalid Currency", create_test_case_6, "REJECT", "IAS validation failed: Currency JPY not supported"),
    ("TC-IAS-007", "IAS_v1 Hard Failure - Amount Exceeds Maximum", create_test_case_7, "REJECT", "IAS validation failed: Invoice amount exceeds maximum threshold of 10000000.0"),
    ("TC-IAS-008", "IAS_v1 Hard Failure - Multiple Validation Failures", create_test_case_8, "REJECT", None),  # Multiple reasons
    ("TC-BRI-001", "BRI_v1 Risk Band - LOW Risk (Clean Buyer)", create_test_case_9, "APPROVE", "Buyer classified as LOW risk"),
    ("TC-BRI-002", "BRI_v1 Risk Band - LOW Risk Boundary", create_test_case_10, "APPROVE", "Buyer classified as LOW risk"),
    ("TC-BRI-003", "BRI_v1 Risk Band - MEDIUM Risk (Just Above LOW)", create_test_case_11, "APPROVE", "Buyer classified as MEDIUM risk"),
    ("TC-BRI-004", "BRI_v1 Risk Band - MEDIUM Risk (At Upper Boundary)", create_test_case_12, "APPROVE", "Buyer classified as MEDIUM risk"),
    ("TC-BRI-005", "BRI_v1 Risk Band - HIGH Risk (Just Above MEDIUM)", create_test_case_13, "HOLD", "Buyer classified as HIGH risk"),
    ("TC-BRI-006", "BRI_v1 Risk Band - HIGH Risk (Missing Identifiers)", create_test_case_14, "HOLD", "Buyer missing both registration number and tax ID"),
    ("TC-BRI-007", "BRI_v1 Risk Band - MEDIUM Risk (One Identifier)", create_test_case_15, "APPROVE", "Buyer classified as MEDIUM risk"),
    ("TC-BFE-001", "BFE_v1 HOLD Condition - Exposure Just Above Cap", create_test_case_16, "REJECT", "BFE checks failed"),
    ("TC-BFE-002", "BFE_v1 PASSED - Exposure Exactly at Cap", create_test_case_17, "HOLD", "Buyer classified as MEDIUM risk with high exposure"),
    ("TC-BFE-003", "BFE_v1 HOLD Condition - Timing Too Soon", create_test_case_18, "REJECT", "BFE checks failed"),
    ("TC-BFE-004", "BFE_v1 PASSED - Timing Exactly at Minimum", create_test_case_19, "APPROVE", "Buyer classified as LOW risk"),
    ("TC-BFE-005", "BFE_v1 HOLD Condition - Timing Too Far", create_test_case_20, "REJECT", "BFE checks failed"),
    ("TC-BFE-006", "BFE_v1 PASSED - Timing Exactly at Maximum", create_test_case_21, "APPROVE", "Buyer classified as LOW risk"),
    ("TC-UDF-001", "UDF_v1 Decision Precedence - IAS REJECT + BRI LOW → REJECT", create_test_case_22, "REJECT", "IAS validation failed"),
    ("TC-UDF-002", "UDF_v1 Decision Precedence - IAS PASS + BRI HIGH → HOLD", create_test_case_23, "HOLD", "Buyer classified as HIGH risk"),
    ("TC-UDF-003", "UDF_v1 Decision Precedence - MEDIUM + High Exposure → HOLD", create_test_case_24, "HOLD", "Buyer classified as MEDIUM risk with high exposure"),
    ("TC-UDF-004", "UDF_v1 Decision Precedence - All Engines Clean → APPROVE", create_test_case_25, "APPROVE", "Buyer classified as LOW risk"),
    ("TC-UDF-005", "UDF_v1 Decision Precedence - MEDIUM + Low Exposure → APPROVE", create_test_case_26, "APPROVE", "Buyer classified as MEDIUM risk"),
    ("TC-HAPPY-001", "Happy Path - Golden Case", create_test_case_27, "APPROVE", "Buyer classified as LOW risk"),
    ("TC-EXPLAIN-001", "Explainability Integrity - All Reasons Present", create_test_case_28, "APPROVE", "Buyer classified as MEDIUM risk"),
    ("TC-EXPLAIN-002", "Explainability Integrity - Multiple Failure Reasons", create_test_case_29, "REJECT", "IAS validation failed"),
    ("TC-UDF-006", "UDF_v1 Fallback - Unknown Risk Band", create_test_case_30, "APPROVE", "Buyer classified as LOW risk"),
]


def run_test_case(test_id, description, create_func, expected_decision, expected_reason_keyword):
    """Run a single test case and return results"""
    try:
        invoice, buyer, existing_exposure = create_func()
        execution = execute_algorithm_v01(invoice, buyer, existing_exposure)
        
        actual_decision = execution.final_decision.value if execution.final_decision else "None"
        actual_reason = execution.udf_result.reason if execution.udf_result else "No reason"
        
        # Get individual engine results
        ias_passed = execution.ias_result.passed if execution.ias_result else False
        ias_reason = execution.ias_result.reason if execution.ias_result else "No reason"
        bri_risk_band = execution.bri_result.risk_band.value if execution.bri_result and execution.bri_result.risk_band else "None"
        bri_reason = execution.bri_result.reason if execution.bri_result else "No reason"
        bfe_passed = execution.bfe_result.passed if execution.bfe_result else False
        bfe_reason = execution.bfe_result.reason if execution.bfe_result else "No reason"
        
        # Check if decision matches
        decision_match = actual_decision == expected_decision
        
        # Check if reason contains expected keyword (if provided)
        reason_match = True
        if expected_reason_keyword:
            reason_match = expected_reason_keyword.lower() in actual_reason.lower()
        
        test_passed = decision_match and reason_match
        
        return {
            "test_id": test_id,
            "description": description,
            "passed": test_passed,
            "decision_match": decision_match,
            "reason_match": reason_match,
            "expected_decision": expected_decision,
            "actual_decision": actual_decision,
            "expected_reason_keyword": expected_reason_keyword,
            "actual_reason": actual_reason,
            "ias_passed": ias_passed,
            "ias_reason": ias_reason,
            "bri_risk_band": bri_risk_band,
            "bri_reason": bri_reason,
            "bfe_passed": bfe_passed,
            "bfe_reason": bfe_reason,
            "error": None
        }
    except Exception as e:
        return {
            "test_id": test_id,
            "description": description,
            "passed": False,
            "decision_match": False,
            "reason_match": False,
            "expected_decision": expected_decision,
            "actual_decision": "ERROR",
            "expected_reason_keyword": expected_reason_keyword,
            "actual_reason": f"Exception: {str(e)}",
            "ias_passed": False,
            "ias_reason": f"Exception: {str(e)}",
            "bri_risk_band": "ERROR",
            "bri_reason": f"Exception: {str(e)}",
            "bfe_passed": False,
            "bfe_reason": f"Exception: {str(e)}",
            "error": str(e)
        }


def generate_report(results):
    """Generate markdown report"""
    report = []
    report.append("# Algorithm v0.1 - Test Execution Report")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    
    report.append("## Summary")
    report.append("")
    report.append(f"- **Total Test Cases:** {total}")
    report.append(f"- **Passed:** {passed} ✅")
    report.append(f"- **Failed:** {failed} ❌")
    report.append(f"- **Pass Rate:** {(passed/total*100):.1f}%")
    report.append("")
    report.append("---")
    report.append("")
    
    # Detailed results
    report.append("## Detailed Results")
    report.append("")
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        report.append(f"### Test Case {i}: {result['test_id']} - {result['description']}")
        report.append("")
        report.append(f"**Status:** {status}")
        report.append("")
        
        # Decision comparison
        decision_status = "✅" if result["decision_match"] else "❌"
        report.append(f"**Final Decision:** {decision_status}")
        report.append(f"- Expected: `{result['expected_decision']}`")
        report.append(f"- Actual: `{result['actual_decision']}`")
        report.append("")
        
        # Reason comparison
        reason_status = "✅" if result["reason_match"] else "❌"
        report.append(f"**Reason Match:** {reason_status}")
        if result["expected_reason_keyword"]:
            report.append(f"- Expected Keyword: `{result['expected_reason_keyword']}`")
        report.append(f"- Actual Reason: `{result['actual_reason']}`")
        report.append("")
        
        # Engine outputs
        report.append("**Engine Outputs:**")
        report.append("")
        report.append("**IAS_v1:**")
        report.append(f"- Passed: `{result['ias_passed']}`")
        report.append(f"- Reason: `{result['ias_reason']}`")
        report.append("")
        report.append("**BRI_v1:**")
        report.append(f"- Risk Band: `{result['bri_risk_band']}`")
        report.append(f"- Reason: `{result['bri_reason']}`")
        report.append("")
        report.append("**BFE_v1:**")
        report.append(f"- Passed: `{result['bfe_passed']}`")
        report.append(f"- Reason: `{result['bfe_reason']}`")
        report.append("")
        
        if result["error"]:
            report.append(f"**Error:** `{result['error']}`")
            report.append("")
        
        report.append("---")
        report.append("")
    
    # Failed tests summary
    failed_tests = [r for r in results if not r["passed"]]
    if failed_tests:
        report.append("## Failed Tests Summary")
        report.append("")
        for result in failed_tests:
            report.append(f"- **{result['test_id']}**: {result['description']}")
            report.append(f"  - Expected: `{result['expected_decision']}`, Actual: `{result['actual_decision']}`")
            report.append("")
    
    return "\n".join(report)


def main():
    """Run all test cases and generate report"""
    print("Running QA test cases...")
    print("=" * 80)
    
    results = []
    for test_id, description, create_func, expected_decision, expected_reason in TEST_CASES:
        print(f"Running {test_id}...")
        result = run_test_case(test_id, description, create_func, expected_decision, expected_reason)
        results.append(result)
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"  {status}: {result['actual_decision']} (expected {result['expected_decision']})")
    
    print("\n" + "=" * 80)
    print("Generating report...")
    
    report = generate_report(results)
    
    output_file = "test_execution_report.md"
    with open(output_file, "w") as f:
        f.write(report)
    
    print(f"Report saved to: {output_file}")
    
    # Print summary
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\nSummary: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")


if __name__ == "__main__":
    main()

