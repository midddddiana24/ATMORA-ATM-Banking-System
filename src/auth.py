"""
ATMORA - Authentication Manager
=================================
Handles user login, session management, and attempt limiting.

Demonstrates:
  - Decision structures (if / elif / else / nested)
  - Repetition structures (while loop concept for attempts)
  - Functions
  - Data validation

Course: CIT 240 – Open Source Programming
"""

from data_manager import DataManager


# ============================================================
# CONSTANTS
# ============================================================

MAX_LOGIN_ATTEMPTS = 3   # Maximum failed login attempts allowed


# ============================================================
# AUTHENTICATION MANAGER
# ============================================================

class AuthManager:
    """
    Manages user authentication and session state.
    
    Tracks login attempts and locks out users after too many failures.
    Demonstrates: decision structures, state management
    """

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.current_user = None        # Currently authenticated account
        self.failed_attempts = 0        # Count of failed login attempts
        self.is_locked = False          # Whether account entry is locked

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    def authenticate(self, account_number: str, pin: str) -> dict:
        """
        Attempt to authenticate a user with account number and PIN.
        
        Returns a result dictionary with:
          - success (bool)
          - message (str)
          - account (dict or None)
          - attempts_remaining (int)
        
        Demonstrates:
          - if / elif / else
          - nested if (account found → then check status → then check PIN)
          - Decision based on attempt count
        """

        # Decision: check if the system is locked (too many attempts)
        if self.is_locked:
            return {
                'success': False,
                'message': (
                    "Too many unsuccessful attempts.\n"
                    "Please restart the application to try again."
                ),
                'account': None,
                'attempts_remaining': 0
            }

        # Validate inputs are not empty
        if not account_number or not account_number.strip():
            return {
                'success': False,
                'message': "Please enter your account number.",
                'account': None,
                'attempts_remaining': MAX_LOGIN_ATTEMPTS - self.failed_attempts
            }

        if not pin or not pin.strip():
            return {
                'success': False,
                'message': "Please enter your PIN.",
                'account': None,
                'attempts_remaining': MAX_LOGIN_ATTEMPTS - self.failed_attempts
            }

        # Look up the account in data
        account = self.data_manager.get_account(account_number.strip())

        # Decision structure: check account existence
        if account is None:
            # Account not found
            self.failed_attempts += 1
            return self._build_failure_result("Account not found.")

        else:
            # Nested if: Account found — check if it is active
            if account.get('status') != 'active':
                return {
                    'success': False,
                    'message': "This account is not active. Please contact support.",
                    'account': None,
                    'attempts_remaining': MAX_LOGIN_ATTEMPTS - self.failed_attempts
                }

            # Nested if: Account active — check PIN
            elif account.get('pin') != pin.strip():
                self.failed_attempts += 1
                return self._build_failure_result("Incorrect PIN.")

            else:
                # All checks passed — authentication successful
                self.current_user = account
                self.failed_attempts = 0  # Reset attempt counter on success
                self.is_locked = False

                return {
                    'success': True,
                    'message': f"Welcome, {account.get('name', 'User')}!",
                    'account': account,
                    'attempts_remaining': MAX_LOGIN_ATTEMPTS
                }

    def _build_failure_result(self, message: str) -> dict:
        """
        Build a failure authentication result.
        Locks the system if max attempts are exceeded.
        
        Demonstrates: decision structure based on counter
        """
        remaining = MAX_LOGIN_ATTEMPTS - self.failed_attempts

        # Decision: Check if we should lock after this failure
        if remaining <= 0:
            self.is_locked = True
            return {
                'success': False,
                'message': (
                    "Too many unsuccessful attempts.\n"
                    "Please restart the application to try again."
                ),
                'account': None,
                'attempts_remaining': 0
            }

        # Build warning message based on remaining attempts
        elif remaining == 1:
            warning = f"{message}\n⚠ 1 attempt remaining."
        else:
            warning = f"{message}\n{remaining} attempts remaining."

        return {
            'success': False,
            'message': warning,
            'account': None,
            'attempts_remaining': remaining
        }

    # --------------------------------------------------------
    # SESSION MANAGEMENT
    # --------------------------------------------------------

    def logout(self):
        """
        Clear the current user session.
        
        Must be called when user logs out to prevent unauthorized access.
        """
        self.current_user = None
        # Note: Do NOT reset failed_attempts on logout
        # (prevents gaming the attempt limit by logging in/out)

    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        return self.current_user is not None

    def get_current_user(self) -> dict:
        """
        Get the currently authenticated user data.
        Returns None if not authenticated.
        """
        return self.current_user

    def get_current_account_number(self) -> str:
        """Get the account number of the current user."""
        if self.current_user:
            return self.current_user.get('account_number', '')
        return ''

    def refresh_current_user(self):
        """
        Refresh current user data from file.
        Called after transactions to get updated balance.
        """
        if self.current_user:
            account_number = self.current_user.get('account_number')
            updated = self.data_manager.get_account(account_number)
            if updated:
                self.current_user = updated

    def reset_attempts(self):
        """Reset failed attempt counter (called on app restart)."""
        self.failed_attempts = 0
        self.is_locked = False
