"""
ATMORA - Data Manager
======================
Handles all JSON file read/write operations for accounts and transactions.

Demonstrates:
  - Functions
  - File I/O with JSON
  - Error handling
  - Data iteration with for loops

Course: CIT 240 – Open Source Programming
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCOUNTS_FILE = os.path.join(BASE_DIR, 'data', 'accounts.json')
TRANSACTIONS_FILE = os.path.join(BASE_DIR, 'data', 'transactions.json')

# Default demo account data (used if file is missing)
DEFAULT_ACCOUNTS = {
    "accounts": [
        {
            "account_number": "10010001",
            "name": "Roberto Mediana",
            "pin": "1234",
            "balance": 50000.00,
            "status": "active",
            "account_type": "Demo Savings"
        },
        {
            "account_number": "10010002",
            "name": "Demo Recipient",
            "pin": "5678",
            "balance": 25000.00,
            "status": "active",
            "account_type": "Demo Savings"
        }
    ]
}

DEFAULT_TRANSACTIONS = {"transactions": []}


# ============================================================
# DATA MANAGER CLASS
# ============================================================

class DataManager:
    """
    Manages all data persistence for the ATMORA application.
    
    Handles:
    - Loading and saving accounts.json
    - Loading and saving transactions.json
    - Account lookup and updates
    - Transaction recording
    """

    def __init__(self):
        """Initialize data manager and ensure data files exist."""
        self._ensure_data_directory()
        self._ensure_accounts_file()
        self._ensure_transactions_file()

    # --------------------------------------------------------
    # SETUP
    # --------------------------------------------------------

    def _ensure_data_directory(self):
        """Create the data directory if it doesn't exist."""
        data_dir = os.path.join(BASE_DIR, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _ensure_accounts_file(self):
        """Create accounts.json with demo data if it doesn't exist."""
        if not os.path.exists(ACCOUNTS_FILE):
            self._write_json(ACCOUNTS_FILE, DEFAULT_ACCOUNTS)

    def _ensure_transactions_file(self):
        """Create transactions.json if it doesn't exist."""
        if not os.path.exists(TRANSACTIONS_FILE):
            self._write_json(TRANSACTIONS_FILE, DEFAULT_TRANSACTIONS)

    # --------------------------------------------------------
    # JSON FILE OPERATIONS
    # --------------------------------------------------------

    def _read_json(self, filepath: str) -> dict:
        """
        Read and parse a JSON file safely.
        Returns empty dict if file is missing or corrupted.
        
        Demonstrates: try/except error handling
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            # File exists but is corrupted — return defaults
            print(f"Warning: Could not parse {filepath}. Using defaults.")
            return {}
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return {}

    def _write_json(self, filepath: str, data: dict) -> bool:
        """
        Write data to a JSON file safely.
        Returns True if successful, False otherwise.
        
        Demonstrates: try/except, file I/O
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    # --------------------------------------------------------
    # ACCOUNT OPERATIONS
    # --------------------------------------------------------

    def load_accounts(self) -> list:
        """
        Load all accounts from accounts.json.
        Returns list of account dictionaries.
        
        Demonstrates: data access, default handling
        """
        data = self._read_json(ACCOUNTS_FILE)

        # Decision: check if data loaded correctly
        if not data or 'accounts' not in data:
            return DEFAULT_ACCOUNTS['accounts']

        return data['accounts']

    def save_accounts(self, accounts: list) -> bool:
        """
        Save all accounts back to accounts.json.
        
        Demonstrates: data persistence
        """
        data = {'accounts': accounts}
        return self._write_json(ACCOUNTS_FILE, data)

    def get_account(self, account_number: str) -> Optional[dict]:
        """
        Find and return a specific account by account number.
        
        Returns None if account not found.
        
        Demonstrates: for loop iteration, decision structure
        """
        accounts = self.load_accounts()

        # FOR LOOP: Search through accounts list
        for account in accounts:
            if account.get('account_number') == account_number.strip():
                return account  # Return matching account

        # Account not found
        return None

    def update_account(self, account_number: str, updates: dict) -> bool:
        """
        Update specific fields for an account.
        
        Demonstrates: for loop, enumerate, dictionary update
        """
        accounts = self.load_accounts()

        # FOR LOOP with enumerate: find and update account
        for i, account in enumerate(accounts):
            if account.get('account_number') == account_number:
                # Update only the specified fields
                for key, value in updates.items():
                    accounts[i][key] = value
                # Save updated accounts list
                return self.save_accounts(accounts)

        return False  # Account not found

    def update_balance(self, account_number: str, new_balance: float) -> bool:
        """
        Update the balance for a specific account.
        
        Demonstrates: function calls, data update
        """
        return self.update_account(account_number, {'balance': round(new_balance, 2)})

    # --------------------------------------------------------
    # TRANSACTION OPERATIONS
    # --------------------------------------------------------

    def load_transactions(self) -> list:
        """
        Load all transactions from transactions.json.
        Returns list of transaction dictionaries.
        """
        data = self._read_json(TRANSACTIONS_FILE)

        if not data or 'transactions' not in data:
            return []

        return data['transactions']

    def save_transactions(self, transactions: list) -> bool:
        """Save all transactions to transactions.json."""
        data = {'transactions': transactions}
        return self._write_json(TRANSACTIONS_FILE, data)

    def record_transaction(self, transaction: dict) -> bool:
        """
        Add a new transaction record to transactions.json.
        
        Demonstrates: list operations, data persistence
        """
        transactions = self.load_transactions()

        # Add the new transaction to the beginning (newest first)
        transactions.insert(0, transaction)

        return self.save_transactions(transactions)

    def get_account_transactions(
        self, 
        account_number: str,
        txn_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> list:
        """
        Get transactions for a specific account.
        
        Optional filtering by transaction type.
        Optional limit on number of results.
        
        Demonstrates: for loop, conditional filtering,
                      multiple conditions with if/elif
        """
        all_transactions = self.load_transactions()
        account_txns = []

        # FOR LOOP: Filter transactions for this account
        for txn in all_transactions:
            # Decision: check account match
            if txn.get('account_number') == account_number:
                # Nested if: apply type filter if specified
                if txn_type is None:
                    account_txns.append(txn)
                elif txn.get('type') == txn_type:
                    account_txns.append(txn)

        # Apply limit if specified
        if limit is not None:
            account_txns = account_txns[:limit]

        return account_txns

    def get_recent_transactions(self, account_number: str, count: int = 5) -> list:
        """Get the most recent transactions for an account."""
        return self.get_account_transactions(account_number, limit=count)
