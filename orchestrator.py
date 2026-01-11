"""
Orchestrator for Thevani Algorithm v0.1
Controls execution order: upload → buyer accept → IAS_v1 → BRI_v1 → BFE_v1 → UDF_v1 → decision logged
"""

from datetime import datetime
from models import Invoice, Buyer, AlgorithmExecution, Decision
from engines.ias_v1 import execute_ias_v1
from engines.bri_v1 import execute_bri_v1
from engines.bfe_v1 import execute_bfe_v1
from engines.udf_v1 import execute_udf_v1


def execute_algorithm_v01(
    invoice: Invoice,
    buyer: Buyer,
    existing_exposure: float = 0.0
) -> AlgorithmExecution:
    """
    Execute Algorithm v0.1 end-to-end
    
    Flow:
    1. IAS_v1 - validation & authenticity
    2. BRI_v1 - buyer risk classification
    3. BFE_v1 - exposure & timing checks
    4. UDF_v1 - final decision
    
    Returns complete execution context with decision and explanation
    """
    
    execution = AlgorithmExecution(
        invoice=invoice,
        buyer=buyer,
        execution_timestamp=datetime.now()
    )
    
    # Step 1: IAS_v1
    ias_result = execute_ias_v1(invoice, buyer)
    execution.ias_result = ias_result
    
    # Step 2: BRI_v1
    bri_result = execute_bri_v1(invoice, buyer)
    execution.bri_result = bri_result
    
    # Step 3: BFE_v1
    bfe_result = execute_bfe_v1(invoice, buyer, existing_exposure)
    execution.bfe_result = bfe_result
    
    # Step 4: UDF_v1 (only engine that makes final decision)
    udf_result = execute_udf_v1(invoice, buyer, ias_result, bri_result, bfe_result)
    execution.udf_result = udf_result
    
    # Extract final decision
    execution.final_decision = udf_result.decision
    
    # Build explanation
    explanation_parts = [
        f"Algorithm v0.1 Execution",
        f"IAS_v1: {'PASSED' if ias_result.passed else 'FAILED'} - {ias_result.reason}",
        f"BRI_v1: Risk Band = {bri_result.risk_band.value if bri_result.risk_band else 'UNKNOWN'} - {bri_result.reason}",
        f"BFE_v1: {'PASSED' if bfe_result.passed else 'FAILED'} - {bfe_result.reason}",
        f"UDF_v1: Decision = {udf_result.decision.value if udf_result.decision else 'UNKNOWN'} - {udf_result.reason}"
    ]
    
    execution.explanation = "\n".join(explanation_parts)
    
    return execution


def log_decision(execution: AlgorithmExecution) -> None:
    """
    Log the final decision with explanation
    """
    print("=" * 80)
    print("THEVANI ALGORITHM v0.1 - DECISION LOG")
    print("=" * 80)
    print(f"Execution Time: {execution.execution_timestamp}")
    print(f"Invoice ID: {execution.invoice.invoice_id}")
    print(f"Invoice Number: {execution.invoice.invoice_number}")
    print(f"Amount: {execution.invoice.amount} {execution.invoice.currency}")
    print(f"Buyer ID: {execution.buyer.buyer_id}")
    print(f"Buyer Name: {execution.buyer.name}")
    print("-" * 80)
    print("FINAL DECISION:", execution.final_decision.value if execution.final_decision else "UNKNOWN")
    print("-" * 80)
    print("EXPLANATION:")
    print(execution.explanation)
    print("=" * 80)
    print()



