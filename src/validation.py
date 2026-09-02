"""
ATMORA - Validation Module
===========================
All input validation functions for the ATM system.

This module demonstrates:
  - Functions
  - Decision structures (if / elif / else / nested if)
  - Input validation patterns

Course: CIT 240 – Open Source Programming
"""


# ============================================================
# RESULT CONTAINER
# ============================================================

class ValidationResult:
    """
    Contains the outcome of a validation check.
    
    Attributes:
        valid (bool): Whether validation passed
        message (str): Feedback message for the user
    """
    def __init__(self, valid: bool, message: str = ""):
        self.valid = valid
        self.message = message

    def __bool__(self):
        return self.valid


# ============================================================
# ACCOUNT & PIN VALIDATION
# ============================================================

def validate_account_number(account_number: str) -> ValidationResult:
    """
    Validate ATM account number format.
    
    Rules:
    - Must not be empty
    - Must contain only digits
    - Must be between 6 and 12 digits long
    
    Demonstrates: if / elif / else decision structure
    """
    # Clean input
    account = account_number.strip()

    # if: Check for empty input
    if not account:
        return ValidationResult(False, "Account number cannot be empty.")

    # elif: Check for numeric characters only
    elif not account.isdigit():
        return ValidationResult(False, "Account number must contain digits only.")

    # elif: Check length range
    elif len(account) < 6:
        return ValidationResult(False, "Account number must be at least 6 digits.")

    elif len(account) > 12:
        return ValidationResult(False, "Account number must not exceed 12 digits.")

    # else: All checks passed
    else:
        return ValidationResult(True, "Valid account number.")


def validate_pin(pin: str) -> ValidationResult:
    """
    Validate ATM PIN format.
    
    Rules:
    - Must not be empty
    - Must contain only digits
    - Must be 4 to 6 digits long
    
    Demonstrates: nested decision structure
    """
    # Check for empty PIN
    if not pin:
        return ValidationResult(False, "PIN cannot be empty.")

    # Nested if: Further checks only if not empty
    else:
        if not pin.isdigit():
            return ValidationResult(False, "PIN must contain digits only.")
        elif len(pin) < 4:
            return ValidationResult(False, "PIN must be at least 4 digits.")
        elif len(pin) > 6:
            return ValidationResult(False, "PIN must not exceed 6 digits.")
        else:
            return ValidationResult(True, "Valid PIN.")


# ============================================================
# AMOUNT VALIDATION
# ============================================================

def validate_amount(amount_str: str) -> ValidationResult:
    """
    Validate a monetary amount string.
    
    Rules:
    - Must not be empty
    - Must be numeric (allows decimal point)
    - Must be greater than zero
    - Must not exceed ₱999,999.99
    
    Demonstrates: if / elif / else, type conversion, try/except
    """
    # Check for empty input
    if not amount_str or not amount_str.strip():
        return ValidationResult(False, "Please enter an amount.")

    # Try to convert to float (handles invalid characters)
    try:
        amount = float(amount_str.strip())
    except ValueError:
        return ValidationResult(False, "Amount must be a valid number.")

    # Decision structure for amount range
    if amount <= 0:
        return ValidationResult(False, "Amount must be greater than zero.")

    elif amount > 999999.99:
        return ValidationResult(False, "Amount exceeds the maximum limit of ₱999,999.99.")

    else:
        return ValidationResult(True, "Valid amount.")


def validate_withdrawal(amount_str: str, balance: float) -> ValidationResult:
    """
    Validate a cash withdrawal request.
    
    Checks:
    1. Basic amount validity
    2. Sufficient balance
    3. Denomination check (multiples of ₱100)
    
    Demonstrates: nested if, multiple conditions
    """
    # First: validate the amount itself
    amount_result = validate_amount(amount_str)

    if not amount_result.valid:
        return amount_result

    # Convert to float for comparison
    amount = float(amount_str.strip())

    # Nested decision: check balance only if amount is valid
    if amount > balance:
        return ValidationResult(
            False,
            f"Insufficient balance. Available: ₱{balance:,.2f}"
        )

    # Check if amount is a multiple of ₱100 (ATM-style denomination)
    elif amount % 100 != 0:
        return ValidationResult(
            False,
            "Withdrawal amount must be a multiple of ₱100."
        )

    else:
        return ValidationResult(True, "Withdrawal is valid.")


def validate_deposit(amount_str: str) -> ValidationResult:
    """
    Validate a cash deposit amount.
    
    Demonstrates: reusing the base validate_amount function
    """
    # Reuse base validation
    base_result = validate_amount(amount_str)

    if not base_result.valid:
        return base_result

    amount = float(amount_str.strip())

    # Additional deposit-specific rule: minimum ₱100
    if amount < 100:
        return ValidationResult(
            False,
            "Minimum deposit amount is ₱100."
        )
    else:
        return ValidationResult(True, "Deposit is valid.")


def validate_transfer(
    amount_str: str,
    balance: float,
    recipient_account: str,
    sender_account: str,
    accounts_list: list
) -> ValidationResult:
    """
    Validate a fund transfer request.
    
    Checks:
    1. Recipient account format
    2. Recipient exists in system
    3. Cannot transfer to self
    4. Amount validity
    5. Sufficient balance
    
    Demonstrates: multiple conditions, for loop iteration,
                  nested decision structures
    """
    # Step 1: Validate recipient account format
    account_check = validate_account_number(recipient_account)
    if not account_check.valid:
        return ValidationResult(
            False,
            f"Recipient account: {account_check.message}"
        )

    # Step 2: Check if transferring to own account
    if recipient_account.strip() == sender_account.strip():
        return ValidationResult(
            False,
            "Cannot transfer funds to your own account."
        )

    # Step 3: Find recipient in accounts list using a for loop
    recipient_found = False
    recipient_active = False

    # FOR LOOP: Search through all accounts
    for account in accounts_list:
        if account.get('account_number') == recipient_account.strip():
            recipient_found = True
            # Nested if: check if account is active
            if account.get('status') == 'active':
                recipient_active = True
            break  # Stop loop once found

    # Decision: check if recipient exists
    if not recipient_found:
        return ValidationResult(
            False,
            "Recipient account not found in the system."
        )

    # Decision: check if recipient account is active
    if not recipient_active:
        return ValidationResult(
            False,
            "Recipient account is not active."
        )

    # Step 4: Validate transfer amount
    amount_check = validate_amount(amount_str)
    if not amount_check.valid:
        return amount_check

    amount = float(amount_str.strip())

    # Step 5: Check sufficient balance (with minimum ₱1 buffer)
    if amount > balance:
        return ValidationResult(
            False,
            f"Insufficient balance. Available: ₱{balance:,.2f}"
        )

    # All checks passed
    return ValidationResult(True, "Transfer is valid.")
