"""
ATMORA - Transaction Manager
==============================
Records and retrieves transaction history.

Demonstrates:
  - Functions
  - Dictionary construction
  - Data persistence
  - for loop iteration

Course: CIT 240 – Open Source Programming
"""

from data_manager import DataManager
from utils import get_current_timestamp, generate_txn_id


# ============================================================
# TRANSACTION MANAGER CLASS
# ============================================================

class TransactionManager:
    """
    Manages transaction recording and history retrieval.
    
    All transactions are stored in transactions.json
    with full metadata for history display.
    """

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def record(
        self,
        account_number: str,
        txn_type: str,
        amount: float,
        balance_after: float,
        txn_id: str = None,
        description: str = "",
        reference: str = "",
        status: str = "successful"
    ) -> bool:
        """
        Record a new transaction.
        
        Parameters:
            account_number: Account that performed the transaction
            txn_type: 'deposit', 'withdrawal', 'transfer', 'transfer_in'
            amount: Transaction amount (always positive)
            balance_after: Account balance after the transaction
            txn_id: Unique transaction identifier
            description: Human-readable description
            reference: Related account number (for transfers)
            status: 'successful', 'failed', 'pending'
        
        Demonstrates: dictionary creation, data recording
        """
        # Generate transaction ID if not provided
        if not txn_id:
            txn_id = generate_txn_id()

        # Build transaction record as a dictionary
        transaction = {
            'id': txn_id,
            'account_number': account_number,
            'type': txn_type,
            'amount': round(float(amount), 2),
            'balance_after': round(float(balance_after), 2),
            'status': status,
            'description': description,
            'reference': reference,
            'timestamp': get_current_timestamp()
        }

        # Save the transaction
        return self.data_manager.record_transaction(transaction)

    def get_history(
        self,
        account_number: str,
        filter_type: str = None,
        limit: int = None
    ) -> list:
        """
        Get transaction history for an account.
        
        Parameters:
            account_number: Account to get history for
            filter_type: Optional type filter ('deposit', 'withdrawal', 'transfer')
            limit: Maximum number of transactions to return
        
        Demonstrates:
          - for loop iteration
          - Conditional filtering (if/elif)
          - List building
        """
        all_txns = self.data_manager.load_transactions()
        filtered = []

        # FOR LOOP: Iterate through all transactions and filter
        for txn in all_txns:
            # Decision: Check account number match
            if txn.get('account_number') != account_number:
                continue  # Skip transactions for other accounts

            # Decision: Apply type filter if specified
            if filter_type is None:
                # No filter — include all types
                filtered.append(txn)

            elif filter_type == 'deposit' and txn.get('type') in ('deposit',):
                filtered.append(txn)

            elif filter_type == 'withdrawal' and txn.get('type') in ('withdrawal',):
                filtered.append(txn)

            elif filter_type == 'transfer' and txn.get('type') in ('transfer', 'transfer_in'):
                filtered.append(txn)

        # Apply limit if specified
        if limit is not None and limit > 0:
            filtered = filtered[:limit]

        return filtered

    def get_recent(self, account_number: str, count: int = 5) -> list:
        """Get the most recent transactions."""
        return self.get_history(account_number, limit=count)

    def get_transaction_by_id(self, txn_id: str) -> dict:
        """
        Find a transaction by its ID.
        
        Demonstrates: for loop search with early exit
        """
        all_txns = self.data_manager.load_transactions()

        # FOR LOOP: Search for matching transaction
        for txn in all_txns:
            if txn.get('id') == txn_id:
                return txn  # Found — return immediately

        return None  # Not found

    def get_summary(self, account_number: str) -> dict:
        """
        Calculate transaction summary statistics.
        
        Returns totals for deposits, withdrawals, and transfers.
        
        Demonstrates:
          - for loop with accumulator pattern
          - Decision structure inside loop
        """
        history = self.get_history(account_number)

        # Initialize accumulators
        total_deposits = 0.0
        total_withdrawals = 0.0
        total_transfers = 0.0
        count = len(history)

        # FOR LOOP: Calculate totals using accumulator pattern
        for txn in history:
            txn_type = txn.get('type', '')
            amount = float(txn.get('amount', 0))

            # Decision structure to categorize each transaction
            if txn_type == 'deposit':
                total_deposits += amount
            elif txn_type == 'withdrawal':
                total_withdrawals += amount
            elif txn_type in ('transfer', 'transfer_in'):
                total_transfers += amount

        return {
            'total_transactions': count,
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'total_transfers': total_transfers
        }
