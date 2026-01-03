"""
Sample test cases and end-to-end execution for Algorithm v0.1
"""

from datetime import datetime, timedelta
from models import Invoice, Buyer
from orchestrator import execute_algorithm_v01, log_decision


def test_case_1_approve_low_risk():
    """Test case: Low risk buyer, small amount - should APPROVE"""
    print("\n" + "="*80)
    print("TEST CASE 1: Low Risk Buyer - Small Amount")
    print("="*80)
    
    invoice = Invoice(
        invoice_id="INV-001",
        invoice_number="INV-2024-001",
        amount=5000.0,
        currency="USD",
        issue_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        buyer_id="BUYER-001",
        seller_id="SELLER-001",
        status="pending"
    )
    
    buyer = Buyer(
        buyer_id="BUYER-001",
        name="ABC Corporation",
        registration_number="REG-12345",
        tax_id="TAX-12345"
    )
    
    execution = execute_algorithm_v01(invoice, buyer, existing_exposure=0.0)
    log_decision(execution)
    
    assert execution.final_decision.value == "APPROVE", "Expected APPROVE"
    print("✓ TEST CASE 1 PASSED\n")


def test_case_2_reject_ias_failure():
    """Test case: IAS validation failure - should REJECT"""
    print("\n" + "="*80)
    print("TEST CASE 2: IAS Validation Failure")
    print("="*80)
    
    invoice = Invoice(
        invoice_id="INV-002",
        invoice_number="INV-2024-002",
        amount=-1000.0,  # Invalid: negative amount
        currency="USD",
        issue_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        buyer_id="BUYER-002",
        seller_id="SELLER-001",
        status="pending"
    )
    
    buyer = Buyer(
        buyer_id="BUYER-002",
        name="XYZ Corp",
        registration_number="REG-67890",
        tax_id="TAX-67890"
    )
    
    execution = execute_algorithm_v01(invoice, buyer, existing_exposure=0.0)
    log_decision(execution)
    
    assert execution.final_decision.value == "REJECT", "Expected REJECT"
    print("✓ TEST CASE 2 PASSED\n")


def test_case_3_hold_high_risk():
    """Test case: High risk buyer - should HOLD"""
    print("\n" + "="*80)
    print("TEST CASE 3: High Risk Buyer")
    print("="*80)
    
    invoice = Invoice(
        invoice_id="INV-003",
        invoice_number="INV-2024-003",
        amount=200000.0,  # Large amount = HIGH risk
        currency="USD",
        issue_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        buyer_id="BUYER-003",
        seller_id="SELLER-001",
        status="pending"
    )
    
    buyer = Buyer(
        buyer_id="BUYER-003",
        name="High Risk Corp",
        registration_number="REG-99999",
        tax_id="TAX-99999"
    )
    
    execution = execute_algorithm_v01(invoice, buyer, existing_exposure=0.0)
    log_decision(execution)
    
    assert execution.final_decision.value == "HOLD", "Expected HOLD"
    print("✓ TEST CASE 3 PASSED\n")


def test_case_4_reject_bfe_failure():
    """Test case: BFE exposure failure - should REJECT"""
    print("\n" + "="*80)
    print("TEST CASE 4: BFE Exposure Failure")
    print("="*80)
    
    invoice = Invoice(
        invoice_id="INV-004",
        invoice_number="INV-2024-004",
        amount=100000.0,
        currency="USD",
        issue_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        buyer_id="BUYER-004",
        seller_id="SELLER-001",
        status="pending"
    )
    
    buyer = Buyer(
        buyer_id="BUYER-004",
        name="Exposure Test Corp",
        registration_number="REG-11111",
        tax_id="TAX-11111"
    )
    
    # Existing exposure already at limit
    execution = execute_algorithm_v01(invoice, buyer, existing_exposure=450000.0)
    log_decision(execution)
    
    assert execution.final_decision.value == "REJECT", "Expected REJECT"
    print("✓ TEST CASE 4 PASSED\n")


def test_case_5_reject_timing_failure():
    """Test case: BFE timing failure - should REJECT"""
    print("\n" + "="*80)
    print("TEST CASE 5: BFE Timing Failure")
    print("="*80)
    
    invoice = Invoice(
        invoice_id="INV-005",
        invoice_number="INV-2024-005",
        amount=5000.0,
        currency="USD",
        issue_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=3),  # Too soon - less than 7 days
        buyer_id="BUYER-005",
        seller_id="SELLER-001",
        status="pending"
    )
    
    buyer = Buyer(
        buyer_id="BUYER-005",
        name="Timing Test Corp",
        registration_number="REG-22222",
        tax_id="TAX-22222"
    )
    
    execution = execute_algorithm_v01(invoice, buyer, existing_exposure=0.0)
    log_decision(execution)
    
    assert execution.final_decision.value == "REJECT", "Expected REJECT"
    print("✓ TEST CASE 5 PASSED\n")


def test_case_6_hold_medium_risk_high_exposure():
    """Test case: Medium risk with high exposure - should HOLD"""
    print("\n" + "="*80)
    print("TEST CASE 6: Medium Risk with High Exposure")
    print("="*80)
    
    invoice = Invoice(
        invoice_id="INV-006",
        invoice_number="INV-2024-006",
        amount=50000.0,  # Medium risk band
        currency="USD",
        issue_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        buyer_id="BUYER-006",
        seller_id="SELLER-001",
        status="pending"
    )
    
    buyer = Buyer(
        buyer_id="BUYER-006",
        name="Medium Risk Corp",
        registration_number="REG-33333",
        tax_id="TAX-33333"
    )
    
    # High existing exposure
    execution = execute_algorithm_v01(invoice, buyer, existing_exposure=400000.0)
    log_decision(execution)
    
    assert execution.final_decision.value == "HOLD", "Expected HOLD"
    print("✓ TEST CASE 6 PASSED\n")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*80)
    print("THEVANI ALGORITHM v0.1 - TEST SUITE")
    print("="*80)
    
    test_case_1_approve_low_risk()
    test_case_2_reject_ias_failure()
    test_case_3_hold_high_risk()
    test_case_4_reject_bfe_failure()
    test_case_5_reject_timing_failure()
    test_case_6_hold_medium_risk_high_exposure()
    
    print("\n" + "="*80)
    print("ALL TEST CASES PASSED")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_all_tests()


