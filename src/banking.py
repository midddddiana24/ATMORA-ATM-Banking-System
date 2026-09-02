"""
ATMORA - Banking Operations
=============================
Core banking transaction logic: withdrawal, deposit, fund transfer.

Demonstrates:
  - Functions
  - Decision structures (if / elif / else / nested)
  - Data validation and error handling
  - Transaction safety flow

Transaction Safety Pattern:
  Validate → Confirm → Process → Update Balance → Record → Show Result

Course: CIT 240 – Open Source Programming
"""

from data_manager import DataManager
from transaction_manager import TransactionManager
from validation import validate_withdrawal, validate_deposit, validate_transfer
from utils import get_current_timestamp, generate_txn_id


# ============================================================
# BANKING SYSTEM CLASS
# ============================================================

class BankingSystem:
    """
    Handles all core banking operations.
    
    Every transaction follows the safety pattern:
    1. Validate input
    2. Check business rules
    3. Process transaction
    4. Update balance
    5. Record transaction
    6. Return result
    """

    def __init__(self, data_manager: DataManager, txn_manager: TransactionManager):
        self.data_manager = data_manager
        self.txn_manager = txn_manager

    # --------------------------------------------------------
    # BALANCE INQUIRY
    # --------------------------------------------------------

    def get_balance(self, account_number: str) -> float:
        """
        Get the current balance for an account.
        
        Demonstrates: data retrieval, decision structure
        """
        account = self.data_manager.get_account(account_number)

        # Decision: check if account exists
        if account is None:
            return 0.0
        else:
            return float(account.get('balance', 0.0))

    # --------------------------------------------------------
    # CASH WITHDRAWAL
    # --------------------------------------------------------

    def withdraw(self, account_number: str, amount_str: str) -> dict:
        """
        Process a cash withdrawal.
        
        Flow: Validate → Process → Update Balance → Record → Return Result
        
        Demonstrates:
          - Input validation
          - Decision structure (if / else)
          - Balance update
          - Transaction recording
        
        Returns:
            dict with 'success', 'message', 'amount', 'new_balance', 'txn_id'
        """
        # Step 1: Get current balance
        account = self.data_manager.get_account(account_number)

        if account is None:
            return {'success': False, 'message': "Account not found."}

        current_balance = float(account.get('balance', 0.0))

        # Step 2: Validate withdrawal
        validation = validate_withdrawal(amount_str, current_balance)

        # Decision: check validation result
        if not validation.valid:
            return {
                'success': False,
                'message': validation.message
            }

        # Step 3: Process — calculate new balance
        amount = float(amount_str.strip())
        new_balance = current_balance - amount

        # Step 4: Update account balance in data file
        updated = self.data_manager.update_balance(account_number, new_balance)

        if not updated:
            return {
                'success': False,
                'message': "Transaction failed. Please try again."
            }

        # Step 5: Record the transaction
        txn_id = generate_txn_id()
        self.txn_manager.record(
            account_number=account_number,
            txn_type='withdrawal',
            amount=amount,
            balance_after=new_balance,
            txn_id=txn_id,
            description=f"ATM Cash Withdrawal"
        )

        # Step 6: Return success result
        return {
            'success': True,
            'message': "Withdrawal successful!",
            'amount': amount,
            'new_balance': new_balance,
            'txn_id': txn_id
        }

    # --------------------------------------------------------
    # CASH DEPOSIT
    # --------------------------------------------------------

    def deposit(self, account_number: str, amount_str: str) -> dict:
        """
        Process a cash deposit.
        
        Flow: Validate → Process → Update Balance → Record → Return Result
        
        Demonstrates:
          - Input validation
          - Balance addition
          - Transaction recording
        """
        # Step 1: Get current account and balance
        account = self.data_manager.get_account(account_number)

        if account is None:
            return {'success': False, 'message': "Account not found."}

        current_balance = float(account.get('balance', 0.0))

        # Step 2: Validate deposit amount
        validation = validate_deposit(amount_str)

        if not validation.valid:
            return {
                'success': False,
                'message': validation.message
            }

        # Step 3: Calculate new balance
        amount = float(amount_str.strip())
        new_balance = current_balance + amount

        # Step 4: Update account balance
        updated = self.data_manager.update_balance(account_number, new_balance)

        if not updated:
            return {
                'success': False,
                'message': "Transaction failed. Please try again."
            }

        # Step 5: Record the transaction
        txn_id = generate_txn_id()
        self.txn_manager.record(
            account_number=account_number,
            txn_type='deposit',
            amount=amount,
            balance_after=new_balance,
            txn_id=txn_id,
            description="ATM Cash Deposit"
        )

        # Step 6: Return success result
        return {
            'success': True,
            'message': "Deposit successful!",
            'amount': amount,
            'new_balance': new_balance,
            'txn_id': txn_id
        }

    # --------------------------------------------------------
    # FUND TRANSFER
    # --------------------------------------------------------

    def transfer(
        self,
        sender_account: str,
        recipient_account: str,
        amount_str: str,
        note: str = ""
    ) -> dict:
        """
        Process a fund transfer between accounts.
        
        Flow: Validate → Get Sender → Get Recipient →
              Deduct Sender → Credit Recipient → Record Both → Return Result
        
        Demonstrates:
          - Complex validation with multiple accounts
          - Two-step balance update (sender + recipient)
          - Paired transaction recording
          - Nested decision structures
        """
        # Step 1: Get sender account
        sender = self.data_manager.get_account(sender_account)

        if sender is None:
            return {'success': False, 'message': "Your account could not be found."}

        sender_balance = float(sender.get('balance', 0.0))

        # Step 2: Load all accounts for validation
        all_accounts = self.data_manager.load_accounts()

        # Step 3: Validate transfer
        validation = validate_transfer(
            amount_str=amount_str,
            balance=sender_balance,
            recipient_account=recipient_account,
            sender_account=sender_account,
            accounts_list=all_accounts
        )

        if not validation.valid:
            return {
                'success': False,
                'message': validation.message
            }

        # Step 4: Process transfer
        amount = float(amount_str.strip())

        # Get recipient account data
        recipient = self.data_manager.get_account(recipient_account.strip())

        if recipient is None:
            return {
                'success': False,
                'message': "Recipient account not found."
            }

        recipient_balance = float(recipient.get('balance', 0.0))

        # Step 5: Calculate new balances
        sender_new_balance = sender_balance - amount
        recipient_new_balance = recipient_balance + amount

        # Step 6: Update sender balance
        updated_sender = self.data_manager.update_balance(sender_account, sender_new_balance)

        if not updated_sender:
            return {
                'success': False,
                'message': "Transfer failed. Sender balance could not be updated."
            }

        # Step 7: Update recipient balance
        updated_recipient = self.data_manager.update_balance(
            recipient_account.strip(), recipient_new_balance
        )

        # Decision: if recipient update fails, rollback sender
        if not updated_recipient:
            # Rollback: restore sender's original balance
            self.data_manager.update_balance(sender_account, sender_balance)
            return {
                'success': False,
                'message': "Transfer failed. Please try again."
            }

        # Step 8: Record transaction for sender (deduction)
        txn_id = generate_txn_id()
        description = f"Transfer to {recipient_account.strip()}"
        if note:
            description += f" — {note}"

        self.txn_manager.record(
            account_number=sender_account,
            txn_type='transfer',
            amount=amount,
            balance_after=sender_new_balance,
            txn_id=txn_id,
            description=description,
            reference=recipient_account.strip()
        )

        # Step 9: Record transaction for recipient (credit)
        recipient_txn_id = generate_txn_id()
        self.txn_manager.record(
            account_number=recipient_account.strip(),
            txn_type='transfer_in',
            amount=amount,
            balance_after=recipient_new_balance,
            txn_id=recipient_txn_id,
            description=f"Transfer from {sender_account}",
            reference=sender_account
        )

        # Step 10: Return success
        return {
            'success': True,
            'message': "Transfer successful!",
            'amount': amount,
            'recipient': recipient.get('name', recipient_account),
            'recipient_account': recipient_account.strip(),
            'new_balance': sender_new_balance,
            'txn_id': txn_id
        }

    # --------------------------------------------------------
    # ACCOUNT INFO
    # --------------------------------------------------------

    def get_account_info(self, account_number: str) -> dict:
        """
        Get full account information (excluding PIN).
        
        Demonstrates: data retrieval, selective field access
        """
        account = self.data_manager.get_account(account_number)

        # Decision: check if account was found
        if account is None:
            return {}

        # Return account info — NEVER include PIN
        return {
            'name': account.get('name', 'Unknown'),
            'account_number': account.get('account_number', ''),
            'balance': float(account.get('balance', 0.0)),
            'status': account.get('status', 'unknown').title(),
            'account_type': account.get('account_type', 'Savings'),
        }
