"""
UDF_v1 - Unified Decision Framework
Deterministic final decision tree
Only engine that can return APPROVE, HOLD, or REJECT
"""

from models import Invoice, Buyer, IASResult, BRIResult, BFEResult, UDFResult, Decision, BuyerRiskBand


def execute_udf_v1(
    invoice: Invoice,
    buyer: Buyer,
    ias_result: IASResult,
    bri_result: BRIResult,
    bfe_result: BFEResult
) -> UDFResult:
    """
    UDF_v1: Deterministic final decision tree
    
    Rules:
    - Only engine that returns APPROVE, HOLD, or REJECT
    - Decision based on results from IAS, BRI, BFE
    - Hard if/else logic - no optimization
    """
    
    decision = None
    reason_parts = []
    
    # Rule 1: IAS must pass - if not, REJECT
    if not ias_result.passed:
        decision = Decision.REJECT
        reason_parts.append(f"IAS validation failed: {ias_result.reason}")
    
    # Rule 2: If IAS passed, check BFE
    elif not bfe_result.passed:
        decision = Decision.REJECT
        reason_parts.append(f"BFE checks failed: {bfe_result.reason}")
    
    # Rule 3: If IAS and BFE passed, check risk band
    elif bri_result.risk_band == BuyerRiskBand.HIGH:
        # High risk = HOLD (requires manual review)
        decision = Decision.HOLD
        reason_parts.append(f"Buyer classified as HIGH risk: {bri_result.reason}")
        reason_parts.append("Requires manual review")
    
    # Rule 4: Medium risk with high exposure = HOLD
    elif bri_result.risk_band == BuyerRiskBand.MEDIUM:
        # Check if exposure is high relative to invoice
        EXPOSURE_RATIO_THRESHOLD = 0.8  # 80% of max exposure
        if bfe_result.exposure_amount and bfe_result.exposure_amount > (500000.0 * EXPOSURE_RATIO_THRESHOLD):
            decision = Decision.HOLD
            reason_parts.append(f"Buyer classified as MEDIUM risk with high exposure: {bfe_result.exposure_amount}")
            reason_parts.append("Requires manual review")
        else:
            decision = Decision.APPROVE
            reason_parts.append(f"Buyer classified as MEDIUM risk: {bri_result.reason}")
            reason_parts.append("All checks passed")
    
    # Rule 5: Low risk = APPROVE
    elif bri_result.risk_band == BuyerRiskBand.LOW:
        decision = Decision.APPROVE
        reason_parts.append(f"Buyer classified as LOW risk: {bri_result.reason}")
        reason_parts.append("All checks passed")
    
    # Rule 6: Fallback (should not happen)
    else:
        decision = Decision.HOLD
        reason_parts.append("Unable to determine risk band - requires manual review")
    
    reason = " | ".join(reason_parts)
    
    return UDFResult(
        engine_name="UDF_v1",
        passed=(decision == Decision.APPROVE),
        reason=reason,
        decision=decision,
        details={
            "ias_passed": ias_result.passed,
            "bfe_passed": bfe_result.passed,
            "risk_band": bri_result.risk_band.value if bri_result.risk_band else None
        }
    )

