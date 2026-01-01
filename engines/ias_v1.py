"""
IAS_v1 - Identity & Authenticity Service
Strict validation & authenticity checks
"""

from datetime import datetime
from models import Invoice, Buyer, IASResult


def execute_ias_v1(invoice: Invoice, buyer: Buyer) -> IASResult:
    """
    IAS_v1: Strict validation & authenticity checks
    
    Rules:
    - Invoice must have valid structure
    - Buyer must have required identifiers
    - Dates must be valid
    - Amount must be positive
    - No ML, no scoring - just hard checks
    """
    
    validation_checks = {}
    reasons = []
    
    # Check 1: Invoice amount validation
    if invoice.amount <= 0:
        validation_checks["amount_positive"] = False
        reasons.append("Invoice amount must be positive")
    else:
        validation_checks["amount_positive"] = True
    
    # Check 2: Invoice dates validation
    if invoice.issue_date >= invoice.due_date:
        validation_checks["dates_valid"] = False
        reasons.append("Due date must be after issue date")
    else:
        validation_checks["dates_valid"] = True
    
    # Check 3: Invoice not expired (due date in future)
    if invoice.due_date < datetime.now():
        validation_checks["not_expired"] = False
        reasons.append("Invoice due date is in the past")
    else:
        validation_checks["not_expired"] = True
    
    # Check 4: Invoice has required fields
    if not invoice.invoice_number or not invoice.invoice_id:
        validation_checks["required_fields"] = False
        reasons.append("Invoice missing required fields (invoice_number, invoice_id)")
    else:
        validation_checks["required_fields"] = True
    
    # Check 5: Buyer has identifier
    if not buyer.buyer_id:
        validation_checks["buyer_identifier"] = False
        reasons.append("Buyer must have buyer_id")
    else:
        validation_checks["buyer_identifier"] = True
    
    # Check 6: Currency validation
    valid_currencies = ["USD", "EUR", "GBP", "INR"]
    if invoice.currency not in valid_currencies:
        validation_checks["currency_valid"] = False
        reasons.append(f"Currency {invoice.currency} not supported")
    else:
        validation_checks["currency_valid"] = True
    
    # Check 7: Amount within reasonable bounds (hard threshold)
    MAX_INVOICE_AMOUNT = 10000000.0  # 10M
    if invoice.amount > MAX_INVOICE_AMOUNT:
        validation_checks["amount_within_bounds"] = False
        reasons.append(f"Invoice amount exceeds maximum threshold of {MAX_INVOICE_AMOUNT}")
    else:
        validation_checks["amount_within_bounds"] = True
    
    # All checks must pass
    all_passed = all(validation_checks.values())
    
    if all_passed:
        reason = "All validation checks passed"
    else:
        reason = "; ".join(reasons)
    
    return IASResult(
        engine_name="IAS_v1",
        passed=all_passed,
        reason=reason,
        validation_checks=validation_checks,
        details={"checks_performed": len(validation_checks)}
    )

