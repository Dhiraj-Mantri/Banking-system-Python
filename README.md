# Python Banking System

A Banking System built with Python featuring both CLI and GUI interfaces.

## Features
- Create new bank accounts
- Deposit & Withdraw money
- Transfer funds between accounts
- View balance & transaction history
- Interest Calculation (4% p.a.)
- Loan Management (Apply, EMI, Repay)
- **Tkinter GUI Desktop App**
- Persistent data storage (JSON)
- PIN-based authentication

## How to Run

### GUI Version (Recommended)
```bash
cd Banking-system-Python
python gui.py
```

### CLI Version
```bash
cd Banking-system-Python
python main.py
```

## Project Structure
- `gui.py` — Tkinter GUI application
- `main.py` — CLI entry point
- `bank/account.py` — Account & interest logic
- `bank/loan.py` — Loan management
- `bank/auth.py` — Authentication
- `bank/storage.py` — JSON persistence
- `bank/utils.py` — Helpers

## Version History
- **v1.0** — Basic terminal banking
- **v2.0** — Interest calculation
- **v3.0** — Loan management
- **v4.0** — Tkinter GUI
