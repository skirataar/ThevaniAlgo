"""
Data models for Thevani Algorithm v0.1
Phase 2 - Data Model (LOCKED)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class Decision(Enum):
    """Final decision types"""
    APPROVE = "APPROVE"
    HOLD = "HOLD"
    REJECT = "REJECT"


class BuyerRiskBand(Enum):
    """Buyer risk classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass
class Invoice:
    """Invoice entity"""
    invoice_id: str
    invoice_number: str
    amount: float
    currency: str
    issue_date: datetime
    due_date: datetime
    buyer_id: str
    seller_id: str
    status: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Buyer:
    """Buyer entity"""
    buyer_id: str
    name: str
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    risk_band: Optional[BuyerRiskBand] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EngineResult:
    """Base result structure for all engines"""
    engine_name: str
    passed: bool
    reason: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class IASResult(EngineResult):
    """IAS engine result"""
    authenticity_score: Optional[float] = None
    validation_checks: Optional[Dict[str, bool]] = None


@dataclass
class BRIResult(EngineResult):
    """BRI engine result"""
    risk_band: Optional[BuyerRiskBand] = None


@dataclass
class BFEResult(EngineResult):
    """BFE engine result"""
    exposure_ok: bool = True
    timing_ok: bool = True
    exposure_amount: Optional[float] = None


@dataclass
class UDFResult(EngineResult):
    """UDF engine result - only engine that can return final decision"""
    decision: Optional[Decision] = None


@dataclass
class AlgorithmExecution:
    """Complete execution context"""
    invoice: Invoice
    buyer: Buyer
    ias_result: Optional[IASResult] = None
    bri_result: Optional[BRIResult] = None
    bfe_result: Optional[BFEResult] = None
    udf_result: Optional[UDFResult] = None
    final_decision: Optional[Decision] = None
    explanation: Optional[str] = None
    execution_timestamp: Optional[datetime] = None


