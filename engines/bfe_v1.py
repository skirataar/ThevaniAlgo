"""
BFE_v1 - Buyer Financial Exposure
Exposure & timing stress checks
"""

from datetime import datetime, timedelta
from models import Invoice, Buyer, BFEResult


def execute_bfe_v1(invoice: Invoice, buyer: Buyer, existing_exposure: float = 0.0) -> BFEResult:
    """
    BFE_v1: Exposure & timing stress checks
    
    Rules:
    - Check total exposure against buyer
    - Check timing stress (days until due date)
    - Hard thresholds only
    """
    
    exposure_ok = True
    timing_ok = True
    reasons = []
    
    # Calculate total exposure (existing + new invoice)
    total_exposure = existing_exposure + invoice.amount
    exposure_amount = total_exposure
    
    # Rule 1: Exposure threshold check
    # Hard threshold - no optimization
    MAX_EXPOSURE_THRESHOLD = 500000.0  # 500K
    
    if total_exposure > MAX_EXPOSURE_THRESHOLD:
        exposure_ok = False
        reasons.append(f"Total exposure ({total_exposure}) exceeds maximum threshold ({MAX_EXPOSURE_THRESHOLD})")
    else:
        reasons.append(f"Total exposure ({total_exposure}) within acceptable limits")
    
    # Rule 2: Timing stress check
    # Check days until due date
    days_until_due = (invoice.due_date - datetime.now()).days
    
    # Hard thresholds for timing
    MIN_DAYS_THRESHOLD = 7  # At least 7 days until due
    MAX_DAYS_THRESHOLD = 365  # Not more than 1 year
    
    if days_until_due < MIN_DAYS_THRESHOLD:
        timing_ok = False
        reasons.append(f"Due date is too soon ({days_until_due} days), minimum required: {MIN_DAYS_THRESHOLD} days")
    elif days_until_due > MAX_DAYS_THRESHOLD:
        timing_ok = False
        reasons.append(f"Due date is too far ({days_until_due} days), maximum allowed: {MAX_DAYS_THRESHOLD} days")
    else:
        reasons.append(f"Timing acceptable: {days_until_due} days until due date")
    
    # BFE passes if both exposure and timing are OK
    passed = exposure_ok and timing_ok
    
    reason = "; ".join(reasons)
    
    return BFEResult(
        engine_name="BFE_v1",
        passed=passed,
        reason=reason,
        exposure_ok=exposure_ok,
        timing_ok=timing_ok,
        exposure_amount=exposure_amount,
        details={
            "days_until_due": days_until_due,
            "existing_exposure": existing_exposure,
            "new_invoice_amount": invoice.amount
        }
    )

