# ATMORA — Modern ATM Banking System

> **Secure • Simple • Smart Banking**

A Python-based educational ATM simulation built with CustomTkinter, featuring a modern dark UI, full transaction management, and clean academic code structure.

---

## Academic Context

| Field | Details |
|-------|---------|
| **School** | West Visayas State University – Janiuay Campus |
| **Department** | School of Information and Communications Technology |
| **Course** | CIT 240 – Open Source Programming |
| **Activity** | Midterm Laboratory Activity No. 5 |
| **Topic** | Creating an Advanced Python Program Using Decision and Repetition Structures: ATM Banking System |
| **Academic Year** | 1st Semester SY 2026–2027 |

---

## Overview

ATMORA is a desktop ATM banking simulation that demonstrates core Python programming concepts through a realistic and visually polished interface. It is designed to satisfy academic requirements for CIT 240 while also being a professionally structured Python project.

> ⚠ **Disclaimer:** This is an educational simulation. It is NOT a real banking system. No real financial data, credentials, or payment systems are used.

---

## Features

### Core Banking Transactions
- ✅ **Account Authentication** — Account number + PIN with attempt limiting
- ✅ **Balance Inquiry** — Real-time balance display with animated counter
- ✅ **Cash Withdrawal** — With quick amounts (₱500–₱5,000) and denomination validation
- ✅ **Cash Deposit** — With quick amounts (₱500–₱10,000) and minimum validation
- ✅ **Fund Transfer** — With recipient validation, confirmation step, and paired recording
- ✅ **Transaction History** — Filterable by type (All / Deposits / Withdrawals / Transfers)
- ✅ **Account Information** — Secure display (PIN never shown)
- ✅ **Logout** — Session clearing with confirmation

### Technical Features
- 🎨 **Modern UI** — Dark navy + gold banking theme via CustomTkinter
- 🖼 **Custom Logo** — Programmatically generated using Pillow (no external files)
- 💾 **Local Storage** — JSON-based data persistence for accounts and transactions
- 🔒 **Input Validation** — Comprehensive validation with user-friendly feedback
- 🔊 **Sound Effects** — Optional audio with graceful fallback if pygame is missing
- ⚡ **Animations** — Balance count-up, loading progress, smooth screen navigation

---

## Python Concepts Demonstrated

### Decision Structures

The program uses `if`, `elif`, `else`, and **nested if** throughout:

```python
# Authentication — nested decision structure
if account is None:
    return failure_result("Account not found.")
else:
    if account.get('status') != 'active':
        return failure_result("Account is not active.")
    elif account.get('pin') != pin:
        return failure_result("Incorrect PIN.")
    else:
        # All checks passed
        self.current_user = account
        return success_result()

# Withdrawal validation — if / elif / else chain
if amount <= 0:
    return ValidationResult(False, "Amount must be greater than zero.")
elif amount > balance:
    return ValidationResult(False, "Insufficient balance.")
elif amount % 100 != 0:
    return ValidationResult(False, "Amount must be a multiple of ₱100.")
else:
    return ValidationResult(True, "Valid.")
```

### Repetition Structures

**`for` loops** appear throughout:
```python
# Search accounts list
for account in accounts:
    if account.get('account_number') == number:
        return account

# Render transaction history
for txn in transactions:
    self._make_txn_card(scroll, txn)

# Create quick-amount buttons
for i, amount in enumerate([500, 1000, 2000, 5000]):
    make_button(frame, f'₱{amount:,}', ...)

# Calculate transaction totals (accumulator pattern)
for txn in history:
    if txn.get('type') == 'deposit':
        total_deposits += txn.get('amount', 0)
```

**`while` loop concept** — The ATM session loop is represented by the GUI event loop: users can perform unlimited transactions before logging out, returning to the main menu after each one.

### Functions

All logic is organized into well-named functions:
```python
validate_account_number()   # Validates account format
validate_withdrawal()       # Validates amount + balance
format_currency()           # Formats ₱ values consistently
mask_account()             # Masks account number for security
generate_txn_id()           # Creates unique transaction IDs
get_greeting()              # Returns time-appropriate greeting
```

### Validation System

Every transaction validates before processing:
```
Enter Amount → validate_amount() → validate_withdrawal() → Process → Record → Show Result
```

Validations check: empty input, non-numeric, zero, negative, exceeds balance, below minimum, wrong denomination, invalid recipient, inactive account.

### Data Handling

Local JSON files store all data:
- `data/accounts.json` — Account records
- `data/transactions.json` — Transaction history

```python
# Load accounts
with open(ACCOUNTS_FILE, 'r') as f:
    data = json.load(f)

# Update balance after transaction
self.data_manager.update_balance(account_number, new_balance)

# Record transaction
self.txn_manager.record(account_number, 'withdrawal', amount, new_balance, txn_id)
```

---

## Project Structure

```
ATMORA-ATM-Banking-System/
│
├── main.py                   # Entry point — run this to start
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── branding/             # Auto-generated logo files
│   │   ├── atmora_logo.png
│   │   ├── atmora_logo_small.png
│   │   └── atmora_icon.png
│   └── sounds/               # Optional WAV sound files
│       ├── click.wav
│       ├── success.wav
│       ├── error.wav
│       ├── transaction.wav
│       └── logout.wav
│
├── data/
│   ├── accounts.json         # Demo account data
│   └── transactions.json     # Transaction history (auto-managed)
│
├── src/
│   ├── __init__.py
│   ├── app.py                # Main GUI application (all screens)
│   ├── auth.py               # Authentication manager
│   ├── banking.py            # Banking operations
│   ├── transaction_manager.py# Transaction recording & history
│   ├── data_manager.py       # JSON data read/write
│   ├── validation.py         # Input validation functions
│   ├── theme.py              # Colors, fonts, sizes
│   ├── logo_generator.py     # Programmatic logo creation
│   ├── audio_manager.py      # Optional sound effects
│   └── utils.py              # Helper functions
│
└── docs/
    └── SOURCES.md            # Open-source acknowledgments
```

---

## Demo Account

> ⚠ These are **dummy classroom credentials** — not real banking information.

| Field | Value |
|-------|-------|
| Account Number | `10010001` |
| PIN | `1234` |
| Name | Roberto Mediana |
| Balance | ₱50,000.00 |
| Type | Demo Savings |

A second account is available for testing fund transfers:

| Field | Value |
|-------|-------|
| Account Number | `10010002` |
| PIN | `5678` |
| Name | Demo Recipient |
| Balance | ₱25,000.00 |

---

## Installation

### Requirements
- Python 3.8 or later
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/midddddiana24/ATMORA-ATM-Banking-System.git
cd ATMORA-ATM-Banking-System

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Install sound support
pip install pygame
```

### How to Run

```bash
python main.py
```

---

## Security Disclaimer

ATMORA is an **academic simulation** built for the CIT 240 course at WVSU–Janiuay Campus. It is explicitly **not** a real banking system:

- PIN data is stored in plain text in `data/accounts.json` for academic simplicity
- No encryption, HTTPS, or banking-grade security is implemented
- No real financial transactions occur
- No connection to any bank, payment network, or financial API

Do not use this system with real account numbers, PINs, or financial information.

---

## Open-Source Acknowledgments

| Resource | Creator | License |
|----------|---------|---------|
| CustomTkinter | Tom Schimansky | MIT |
| Pillow (PIL) | Alex Clark & Contributors | HPND |
| pygame (optional) | Pygame Community | LGPL |
| Python Standard Library | Python Software Foundation | PSF |

Full attribution: [`docs/SOURCES.md`](docs/SOURCES.md)

---

## Developer

**Roberto Mediana Jr**
Developer / Programmer — BSIT
West Visayas State University – Janiuay Campus

GitHub: [@midddddiana24](https://github.com/midddddiana24)

---

## License

This project is licensed under the [MIT License](LICENSE).

External libraries retain their respective licenses as documented in [`docs/SOURCES.md`](docs/SOURCES.md).
