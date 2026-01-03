# Thevani Algorithm v0.1

Fintech underwriting system - Algorithm v0.1 execution implementation.

## Architecture

### Engines (v0.1 - Implemented)
- **IAS_v1**: Identity & Authenticity Service - strict validation & authenticity checks
- **BRI_v1**: Buyer Risk Intelligence - coarse buyer risk bands (LOW, MEDIUM, HIGH)
- **BFE_v1**: Buyer Financial Exposure - exposure & timing stress checks
- **UDF_v1**: Unified Decision Framework - deterministic final decision tree (only engine that returns APPROVE/HOLD/REJECT)

### Engines (v0.1 - Stubs)
- **ACE**: Advanced Credit Engine - SKIPPED
- **REGE**: Regulatory Engine - SKIPPED
- **PRE**: Pricing Engine - SKIPPED

## Execution Flow

```
upload → buyer accept → IAS_v1 → BRI_v1 → BFE_v1 → UDF_v1 → decision logged
```

## Usage

```python
from datetime import datetime, timedelta
from models import Invoice, Buyer
from orchestrator import execute_algorithm_v01, log_decision

# Create invoice and buyer
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

# Execute algorithm
execution = execute_algorithm_v01(invoice, buyer, existing_exposure=0.0)

# Log decision
log_decision(execution)
```

## Running Tests

```bash
python test_execution.py
```

## Design Principles

- **NO machine learning**
- **NO probabilistic scoring**
- **NO weights or optimization**
- **Hard thresholds and if/else logic only**
- **Simple, explicit, readable code**
- **One-pass execution**
- **Fully explainable decisions**


