# THEVANI Shadow Pilot - UI

Minimal UI for Shadow Pilot v1.1 - Manual-first, insight-driven invoice tracking system.

## Setup

```bash
cd ui
npm install
npm run dev
```

The application will be available at `http://localhost:5173`

## Features

### Core Functionality
- ✅ Create & View Buyers (name, industry, notes)
- ✅ Create & View MSMEs (name, GSTIN, linked buyer, notes)
- ✅ Create & View Invoices (core screen with all required fields)
- ✅ Add Invoice Events (most important feature)
- ✅ Dark/Light Mode Toggle
- ✅ CSV Export (optional but useful)

### Invoice Events
Supported event types (locked):
- INVOICE_ACKNOWLEDGED
- QUERY_RAISED
- DISPUTE_RAISED
- PARTIAL_PAYMENT
- PAYMENT_RECEIVED

(INVOICE_ISSUED is implicit - invoice creation = issued)

## Design Principles

- Desktop-first, mobile usable
- Plain tables, zero animations
- Tailwind defaults
- Zero theming beyond dark/light mode
- No scoring, recommendations, dashboards, alerts, automation
- Store truth, reduce memory load, let humans reason

## Data Storage

Currently uses browser localStorage for simplicity. No backend required.

All data is stored locally in the browser:
- `thevani_buyers` - Buyer records
- `thevani_msmes` - MSME records
- `thevani_invoices` - Invoice records
- `thevani_events` - Invoice event records
- `thevani_theme` - Theme preference (dark/light)

## Build

```bash
npm run build
```

Output will be in `dist/` directory.

