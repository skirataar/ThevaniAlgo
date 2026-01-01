"""
BRI_v1 - Buyer Risk Intelligence
Coarse buyer risk bands (LOW, MEDIUM, HIGH)
"""

from models import Invoice, Buyer, BRIResult, BuyerRiskBand


def execute_bri_v1(invoice: Invoice, buyer: Buyer) -> BRIResult:
    """
    BRI_v1: Coarse buyer risk bands
    
    Rules:
    - Classify buyer into LOW, MEDIUM, HIGH risk
    - Based on hard thresholds only
    - No ML, no probabilistic scoring
    """
    
    risk_band = None
    reason = ""
    
    # Rule 1: Check if buyer has registration number (basic authenticity)
    has_registration = buyer.registration_number is not None and buyer.registration_number.strip() != ""
    has_tax_id = buyer.tax_id is not None and buyer.tax_id.strip() != ""
    
    # Rule 2: Risk classification based on invoice amount thresholds
    # Hard thresholds - no optimization
    LOW_RISK_THRESHOLD = 10000.0
    MEDIUM_RISK_THRESHOLD = 100000.0
    
    invoice_amount = invoice.amount
    
    # Rule 3: Determine risk band
    if not has_registration and not has_tax_id:
        # Missing identifiers = HIGH risk
        risk_band = BuyerRiskBand.HIGH
        reason = "Buyer missing both registration number and tax ID"
    elif invoice_amount <= LOW_RISK_THRESHOLD:
        # Small amounts = LOW risk (if has identifiers)
        risk_band = BuyerRiskBand.LOW
        reason = f"Invoice amount ({invoice_amount}) within low risk threshold ({LOW_RISK_THRESHOLD})"
    elif invoice_amount <= MEDIUM_RISK_THRESHOLD:
        # Medium amounts = MEDIUM risk
        risk_band = BuyerRiskBand.MEDIUM
        reason = f"Invoice amount ({invoice_amount}) within medium risk threshold ({MEDIUM_RISK_THRESHOLD})"
    else:
        # Large amounts = HIGH risk
        risk_band = BuyerRiskBand.HIGH
        reason = f"Invoice amount ({invoice_amount}) exceeds medium risk threshold ({MEDIUM_RISK_THRESHOLD})"
    
    # Update buyer with risk band
    buyer.risk_band = risk_band
    
    return BRIResult(
        engine_name="BRI_v1",
        passed=True,  # BRI always "passes" - it's a classification
        reason=reason,
        risk_band=risk_band,
        details={
            "has_registration": has_registration,
            "has_tax_id": has_tax_id,
            "invoice_amount": invoice_amount
        }
    )

