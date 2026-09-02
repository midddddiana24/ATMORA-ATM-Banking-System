"""
ATMORA - Utility Functions
===========================
Helper functions used throughout the application.
Demonstrates: functions, string formatting, datetime handling.
Course: CIT 240 – Open Source Programming
"""

import uuid
import random
import string
from datetime import datetime


# ============================================================
# CURRENCY FORMATTING
# ============================================================

def format_currency(amount: float) -> str:
    """
    Format a float as Philippine Peso currency string.
    
    Example:
        format_currency(50000.0) → '₱50,000.00'
        format_currency(-1500.5) → '-₱1,500.50'
    
    Uses Python's built-in string formatting with comma separator.
    """
    # Decision structure: handle negative amounts specially
    if amount < 0:
        return f"-₱{abs(amount):,.2f}"
    else:
        return f"₱{amount:,.2f}"


def format_amount_with_sign(amount: float, txn_type: str) -> str:
    """
    Format amount with +/- sign based on transaction type.
    
    Decision structure used to determine sign.
    """
    # Determine sign based on transaction type
    if txn_type in ('deposit', 'transfer_in'):
        return f"+₱{amount:,.2f}"
    elif txn_type in ('withdrawal', 'transfer', 'transfer_out'):
        return f"-₱{amount:,.2f}"
    else:
        return f"₱{amount:,.2f}"


# ============================================================
# ACCOUNT NUMBER FORMATTING
# ============================================================

def mask_account(account_number: str) -> str:
    """
    Mask account number for security display.
    
    Shows only last 4 digits.
    Example: '10010001' → '•••• 0001'
    """
    # Validation: check if account number is long enough
    if len(account_number) <= 4:
        return account_number

    last_four = account_number[-4:]
    return f"•••• {last_four}"


def mask_pin(pin: str) -> str:
    """Mask PIN completely for security."""
    return '•' * len(pin)


# ============================================================
# DATE & TIME FORMATTING
# ============================================================

def format_datetime(dt_string: str) -> str:
    """
    Format a datetime string for display.
    
    Input:  '2026-09-02 08:30:00'
    Output: 'Sep 02, 2026 08:30 AM'
    """
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y %I:%M %p")
    except (ValueError, TypeError):
        return dt_string or "Unknown"


def format_date_short(dt_string: str) -> str:
    """
    Format datetime string to short date.
    
    Output: '09/02/26'
    """
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%m/%d/%y")
    except (ValueError, TypeError):
        return ""


def get_current_timestamp() -> str:
    """Return current timestamp as formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_greeting() -> str:
    """
    Return time-appropriate greeting.
    
    Demonstrates: decision structure (if/elif/else)
    """
    hour = datetime.now().hour

    # if/elif/else decision structure
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    elif hour < 21:
        return "Good evening"
    else:
        return "Good night"


# ============================================================
# TRANSACTION ID GENERATION
# ============================================================

def generate_txn_id() -> str:
    """
    Generate a unique transaction ID.
    
    Format: TXN-YYYYMMDD-XXXXXXXX
    Example: TXN-20260902-A3F7B2C1
    
    Demonstrates: string formatting, random generation
    """
    date_part = datetime.now().strftime("%Y%m%d")
    # Generate 8 random hex characters for uniqueness
    random_part = uuid.uuid4().hex[:8].upper()
    return f"TXN-{date_part}-{random_part}"


# ============================================================
# INPUT SANITIZATION
# ============================================================

def sanitize_amount_input(text: str) -> str:
    """
    Remove non-numeric characters from amount input.
    Allows digits and decimal point only.
    """
    result = ""
    # for loop demonstration: iterate through each character
    for char in text:
        if char.isdigit() or char == '.':
            result += char
    return result


def clean_account_number(account: str) -> str:
    """Strip whitespace and non-digit characters from account number."""
    result = ""
    for char in account.strip():
        if char.isdigit():
            result += char
    return result


# ============================================================
# DISPLAY HELPERS
# ============================================================

def truncate_text(text: str, max_length: int = 30) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text


def get_txn_type_display(txn_type: str) -> str:
    """Convert transaction type code to display label."""
    labels = {
        'deposit':     'Deposit',
        'withdrawal':  'Withdrawal',
        'transfer':    'Transfer Out',
        'transfer_in': 'Transfer In',
    }
    return labels.get(txn_type.lower(), txn_type.title())


def get_txn_icon(txn_type: str) -> str:
    """Return an emoji icon for the transaction type."""
    icons = {
        'deposit':     '📥',
        'withdrawal':  '📤',
        'transfer':    '🔄',
        'transfer_in': '📨',
    }
    return icons.get(txn_type.lower(), '💳')


def get_txn_color(txn_type: str) -> str:
    """Return color string for transaction type."""
    colors = {
        'deposit':     '#4CAF50',
        'withdrawal':  '#F44336',
        'transfer':    '#FF9800',
        'transfer_in': '#29B6F6',
    }
    return colors.get(txn_type.lower(), '#90A4AE')
