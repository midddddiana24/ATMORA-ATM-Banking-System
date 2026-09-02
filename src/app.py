"""
ATMORA — Modern ATM Banking System
=====================================
Main GUI Application

Implements all screens and navigation for the ATMORA ATM simulation.

Screens:
  1. Splash Screen
  2. Login Screen
  3. Dashboard
  4. Balance Inquiry
  5. Cash Withdrawal
  6. Cash Deposit
  7. Fund Transfer
  8. Transaction History
  9. Account Information
  10. About
  11. Credits / Developer

Demonstrates:
  - Decision structures (if / elif / else / nested)
  - Repetition structures (while / for loops)
  - Functions and classes
  - GUI design with customtkinter
  - Input validation
  - Transaction feedback

Developer:  Roberto Mediana Jr
GitHub:     https://github.com/midddddiana24
Course:     CIT 240 – Open Source Programming
School:     West Visayas State University – Janiuay Campus
"""

import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import webbrowser
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from theme import COLORS as C, FONTS as F, SIZES as S
from data_manager import DataManager
from auth import AuthManager
from banking import BankingSystem
from transaction_manager import TransactionManager
from audio_manager import AudioManager
from logo_generator import get_logo
from utils import (
    format_currency, mask_account, format_datetime, format_date_short,
    get_greeting, get_txn_type_display, get_txn_icon, get_txn_color,
    format_amount_with_sign
)

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_font(size_key: str, bold: bool = False) -> ctk.CTkFont:
    """Create a CTkFont from theme settings."""
    size = F.get(size_key, 13)
    weight = 'bold' if bold else 'normal'
    return ctk.CTkFont(family=F['family'], size=size, weight=weight)


def make_label(parent, text, size='body', bold=False, color=None, **kwargs):
    """Create a consistently styled CTkLabel."""
    return ctk.CTkLabel(
        parent,
        text=text,
        font=make_font(size, bold),
        text_color=color or C['text'],
        **kwargs
    )


def make_button(parent, text, command, style='primary', width=None, height=None, **kwargs):
    """
    Create a consistently styled CTkButton.
    Styles: 'primary', 'secondary', 'danger', 'success', 'ghost'
    """
    styles = {
        'primary':   (C['btn_primary'], C['btn_primary_hover']),
        'secondary': (C['bg_elevated'], C['bg_hover']),
        'danger':    (C['btn_danger'], '#D32F2F'),
        'success':   (C['btn_success'], '#388E3C'),
        'ghost':     ('transparent', C['bg_card']),
        'gold':      (C['accent_dark'], C['accent']),
    }
    bg, hover = styles.get(style, styles['primary'])
    h = height or S['btn_height']
    w = width or S['btn_width']

    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=bg,
        hover_color=hover,
        text_color=C['text'],
        font=make_font('body', bold=True),
        corner_radius=S['btn_radius'],
        height=h,
        width=w,
        **kwargs
    )


def make_entry(parent, placeholder='', show='', **kwargs):
    """Create a consistently styled CTkEntry."""
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        placeholder_text_color=C['text_muted'],
        fg_color=C['input_bg'],
        border_color=C['input_border'],
        text_color=C['text'],
        font=make_font('body'),
        corner_radius=S['btn_radius'],
        height=S['input_height'],
        show=show,
        **kwargs
    )


def make_card(parent, **kwargs):
    """Create a card-style frame."""
    return ctk.CTkFrame(
        parent,
        fg_color=C['bg_card'],
        corner_radius=S['card_radius'],
        border_width=1,
        border_color=C['border'],
        **kwargs
    )


def make_divider(parent):
    """Create a thin horizontal divider line."""
    return ctk.CTkFrame(parent, height=1, fg_color=C['divider'])


# ============================================================
# BASE SCREEN CLASS
# ============================================================

class BaseScreen(ctk.CTkFrame):
    """
    Base class for all application screens.
    Provides common structure: header bar, content area, footer.
    
    Subclasses override:
      - build()     : Create screen widgets
      - on_show()   : Update dynamic content when screen appears
      - on_hide()   : Cleanup when screen is hidden
    """

    def __init__(self, parent, app):
        super().__init__(
            parent,
            fg_color=C['bg_dark'],
            corner_radius=0
        )
        self.app = app
        self.build()

    def build(self):
        """Override in subclass to build screen widgets."""
        pass

    def on_show(self):
        """Called when screen becomes visible. Override for dynamic updates."""
        pass

    def on_hide(self):
        """Called when screen is hidden."""
        pass

    def navigate_to(self, screen_name: str):
        """Navigate to a named screen."""
        self.app.navigate_to(screen_name)

    def go_back(self):
        """Return to previous screen."""
        self.app.go_back()

    def play(self, sound: str):
        """Play a sound effect."""
        self.app.audio.play(sound)

    def build_header(self, parent, title: str, show_back: bool = True,
                     show_brand: bool = False):
        """
        Build a consistent screen header.
        
        Parameters:
            parent: Parent widget
            title: Screen title text
            show_back: Whether to show ← Back button
            show_brand: Whether to show ATMORA brand in header
        """
        header = ctk.CTkFrame(parent, fg_color=C['bg_elevated'], height=S['header_height'],
                              corner_radius=0)
        header.pack(fill='x')
        header.pack_propagate(False)

        # Brand (left side)
        if show_brand:
            brand = make_label(header, 'ATMORA', size='heading', bold=True,
                               color=C['accent'])
            brand.pack(side='left', padx=20, pady=0)

        # Screen title (center-ish or left if no brand)
        title_lbl = make_label(header, title, size='heading', bold=True)
        if show_brand:
            title_lbl.pack(side='left', padx=8)
        else:
            title_lbl.pack(side='left', padx=24)

        # Back button (right side)
        if show_back:
            back_btn = ctk.CTkButton(
                header,
                text='← Back',
                command=self.go_back,
                fg_color='transparent',
                hover_color=C['bg_hover'],
                text_color=C['text_secondary'],
                font=make_font('small'),
                width=80,
                height=36,
                corner_radius=6
            )
            back_btn.pack(side='right', padx=16)

        return header

    def build_footer(self, parent):
        """Build the consistent app footer."""
        footer = ctk.CTkFrame(parent, fg_color=C['bg_medium'], height=S['footer_height'],
                              corner_radius=0)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)

        make_label(
            footer,
            'ATMORA  •  ATM Banking System  •  Developed by Roberto Mediana Jr  '
            '•  CIT 240  •  2026',
            size='tiny',
            color=C['text_muted']
        ).pack(pady=8)

        return footer

    def show_message(self, parent, msg: str, msg_type: str = 'info'):
        """
        Display an inline status message.
        msg_type: 'success', 'error', 'warning', 'info'
        
        Demonstrates: decision structure for color selection
        """
        colors = {
            'success': (C['success_bg'], C['text_success'], '✓'),
            'error':   (C['error_bg'],   C['text_error'],   '✕'),
            'warning': (C['warning_bg'], C['warning'],      '⚠'),
            'info':    (C['bg_card'],    C['text_secondary'],'ℹ'),
        }
        bg, fg, icon = colors.get(msg_type, colors['info'])

        frame = ctk.CTkFrame(parent, fg_color=bg, corner_radius=8)
        frame.pack(fill='x', padx=24, pady=(0, 8))

        make_label(frame, f"{icon}  {msg}", size='small', color=fg).pack(
            padx=12, pady=8
        )
        return frame


# ============================================================
# SCREEN 1: SPLASH SCREEN
# ============================================================

class SplashScreen(BaseScreen):
    """
    Initial splash screen shown when the app starts.
    Features: Logo animation, loading progress bar.
    """

    def build(self):
        self.configure(fg_color=C['bg_darkest'])

        # Center container
        center = ctk.CTkFrame(self, fg_color='transparent')
        center.place(relx=0.5, rely=0.45, anchor='center')

        # Logo image
        logo_pil = get_logo(120)
        self._logo_ctk = ctk.CTkImage(
            light_image=logo_pil, dark_image=logo_pil, size=(120, 120)
        )
        self.logo_lbl = ctk.CTkLabel(center, image=self._logo_ctk, text='')
        self.logo_lbl.pack(pady=(0, 16))

        # App name
        make_label(center, 'ATMORA', size='logo', bold=True,
                   color=C['text']).pack()

        # Tagline
        make_label(
            center,
            'Secure  •  Simple  •  Smart Banking',
            size='body', color=C['text_secondary']
        ).pack(pady=(4, 28))

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            center, width=220, height=4,
            fg_color=C['bg_elevated'],
            progress_color=C['accent']
        )
        self.progress.pack(pady=(0, 8))
        self.progress.set(0)

        # Loading text
        self.loading_lbl = make_label(
            center, 'Loading...', size='small', color=C['text_muted']
        )
        self.loading_lbl.pack()

        # Version tag
        make_label(
            self,
            'v1.0  •  Academic Edition',
            size='tiny', color=C['text_muted']
        ).place(relx=0.5, rely=0.95, anchor='center')

    def on_show(self):
        """Start loading animation when splash is shown."""
        self.after(100, lambda: self._animate(0))

    def _animate(self, step: int):
        """
        Animate the loading progress bar.
        
        Demonstrates: recursion-style animation with after(),
                      decision structure for completion check
        """
        total_steps = 50
        progress = step / total_steps

        # Update progress bar
        self.progress.set(progress)

        # Update loading dots
        dots = '.' * (step % 4)
        self.loading_lbl.configure(text=f'Loading{dots}')

        # Decision: check if animation is complete
        if step < total_steps:
            # Continue animation
            self.after(30, lambda: self._animate(step + 1))
        else:
            # Animation done — go to login
            self.after(400, lambda: self.navigate_to('login'))


# ============================================================
# SCREEN 2: LOGIN SCREEN
# ============================================================

class LoginScreen(BaseScreen):
    """
    User authentication screen.
    
    Features:
      - Account number input
      - PIN input (masked)
      - Attempt limiting (max 3 failures)
      - Input validation
      - Error feedback
    """

    def build(self):
        self.configure(fg_color=C['bg_dark'])

        # Subtle background pattern
        bg_label = make_label(
            self, '◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈ ◈',
            size='title', color='#0C1A2E'
        )
        bg_label.place(relx=0.5, rely=0.15, anchor='center')

        # Main card
        card = make_card(self, width=380, height=480)
        card.place(relx=0.5, rely=0.5, anchor='center')

        # --- Card Content ---
        # Logo
        logo_pil = get_logo(72)
        self._logo_ctk = ctk.CTkImage(
            light_image=logo_pil, dark_image=logo_pil, size=(72, 72)
        )
        make_label(card, '', image=self._logo_ctk).pack(pady=(28, 6))

        # App name
        make_label(card, 'ATMORA', size='title', bold=True,
                   color=C['accent']).pack()
        make_label(card, 'ATM Banking System', size='small',
                   color=C['text_secondary']).pack(pady=(0, 4))

        make_divider(card).pack(fill='x', padx=24, pady=12)

        make_label(card, 'Welcome Back', size='subtitle', bold=True).pack(pady=(0, 16))

        # Account Number Field
        acc_frame = ctk.CTkFrame(card, fg_color='transparent')
        acc_frame.pack(fill='x', padx=28, pady=(0, 8))
        make_label(acc_frame, 'Account Number', size='label',
                   color=C['text_secondary']).pack(anchor='w', pady=(0, 4))
        self.acc_entry = make_entry(acc_frame, placeholder='Enter account number')
        self.acc_entry.pack(fill='x')

        # PIN Field
        pin_frame = ctk.CTkFrame(card, fg_color='transparent')
        pin_frame.pack(fill='x', padx=28, pady=(0, 6))
        make_label(pin_frame, 'PIN', size='label',
                   color=C['text_secondary']).pack(anchor='w', pady=(0, 4))
        self.pin_entry = make_entry(pin_frame, placeholder='Enter PIN', show='●')
        self.pin_entry.pack(fill='x')

        # Message area
        self.msg_var = tk.StringVar(value='')
        self.msg_lbl = ctk.CTkLabel(
            card,
            textvariable=self.msg_var,
            font=make_font('small'),
            text_color=C['text_error'],
            wraplength=300
        )
        self.msg_lbl.pack(pady=(4, 0))

        # Login Button
        btn_frame = ctk.CTkFrame(card, fg_color='transparent')
        btn_frame.pack(fill='x', padx=28, pady=(8, 0))

        make_button(btn_frame, 'Login', self._login,
                    style='primary', width=None, height=46).pack(fill='x')

        make_button(btn_frame, 'Clear', self._clear,
                    style='ghost', width=None, height=36).pack(fill='x', pady=(6, 0))

        # Footer note
        make_label(
            card,
            '🔒 Secured ATM Terminal',
            size='tiny', color=C['text_muted']
        ).pack(pady=(12, 16))

        # Bind Enter key to login
        self.acc_entry.bind('<Return>', lambda e: self.pin_entry.focus())
        self.pin_entry.bind('<Return>', lambda e: self._login())

        # Bottom footer
        self.build_footer(self)

    def on_show(self):
        """Clear fields when screen appears."""
        self.acc_entry.delete(0, 'end')
        self.pin_entry.delete(0, 'end')
        self.msg_var.set('')
        self.acc_entry.focus()

    def _login(self):
        """
        Handle login button press.
        
        Demonstrates:
          - Decision structure (if/elif/else)
          - Function calls for validation and auth
        """
        self.play('click')

        account_number = self.acc_entry.get()
        pin = self.pin_entry.get()

        # Attempt authentication
        result = self.app.auth.authenticate(account_number, pin)

        # Decision: handle authentication result
        if result['success']:
            # Successful login
            self.msg_var.set('')
            self.app.audio.success()
            self.navigate_to('dashboard')
        else:
            # Failed login — show error
            self.msg_var.set(result['message'])
            self.pin_entry.delete(0, 'end')

            # Decision: check if system is locked
            if result['attempts_remaining'] <= 0:
                self.acc_entry.configure(state='disabled')
                self.pin_entry.configure(state='disabled')
            self.app.audio.error()

    def _clear(self):
        """Clear all input fields."""
        self.play('click')
        self.acc_entry.delete(0, 'end')
        self.pin_entry.delete(0, 'end')
        self.msg_var.set('')
        self.acc_entry.focus()


# ============================================================
# SCREEN 3: DASHBOARD
# ============================================================

class DashboardScreen(BaseScreen):
    """
    Main dashboard shown after successful authentication.
    
    Displays:
      - Personalized greeting
      - Account balance card
      - Quick action buttons
      - Recent transactions
      - Sound toggle
    """

    def build(self):
        self.configure(fg_color=C['bg_dark'])

        # ---- Header ----
        self.header = ctk.CTkFrame(self, fg_color=C['bg_elevated'], height=S['header_height'],
                                   corner_radius=0)
        self.header.pack(fill='x')
        self.header.pack_propagate(False)

        # Logo + Brand
        logo_pil = get_logo(32)
        self._logo_sm = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(32, 32))
        ctk.CTkLabel(self.header, image=self._logo_sm, text='').pack(side='left', padx=(16, 4))
        make_label(self.header, 'ATMORA', size='heading', bold=True,
                   color=C['accent']).pack(side='left', padx=(0, 4))
        make_label(self.header, '|', size='body',
                   color=C['text_muted']).pack(side='left', padx=4)
        make_label(self.header, 'ATM Banking System', size='small',
                   color=C['text_secondary']).pack(side='left')

        # Right side controls
        self.sound_btn = ctk.CTkButton(
            self.header, text='🔊', command=self._toggle_sound,
            fg_color='transparent', hover_color=C['bg_hover'],
            width=40, height=36, font=make_font('heading')
        )
        self.sound_btn.pack(side='right', padx=(0, 8))

        make_button(
            self.header, 'Logout', self._logout,
            style='ghost', width=80, height=36
        ).pack(side='right', padx=(0, 8))

        # ---- Scrollable Content ----
        self.content = ctk.CTkScrollableFrame(
            self, fg_color=C['bg_dark'], scrollbar_button_color=C['bg_card']
        )
        self.content.pack(fill='both', expand=True, padx=0, pady=0)

        # Greeting section
        greet_frame = ctk.CTkFrame(self.content, fg_color='transparent')
        greet_frame.pack(fill='x', padx=28, pady=(20, 8))

        self.greeting_lbl = make_label(greet_frame, '', size='title', bold=True)
        self.greeting_lbl.pack(anchor='w')

        acc_row = ctk.CTkFrame(greet_frame, fg_color='transparent')
        acc_row.pack(anchor='w', pady=(2, 0))
        self.acc_lbl = make_label(acc_row, '', size='small', color=C['text_secondary'])
        self.acc_lbl.pack(side='left')
        self.status_lbl = make_label(acc_row, '  ● Active', size='small', color=C['success'])
        self.status_lbl.pack(side='left')

        # ---- Balance Card ----
        bal_card = make_card(self.content)
        bal_card.pack(fill='x', padx=28, pady=(8, 16))

        make_label(bal_card, 'Available Balance', size='label',
                   color=C['text_secondary']).pack(pady=(18, 4))

        self.balance_lbl = make_label(
            bal_card, '₱0.00',
            size='balance', bold=True, color=C['accent']
        )
        self.balance_lbl.pack(pady=(0, 16))

        # ---- Quick Actions (2x2 grid) ----
        make_label(self.content, 'Quick Actions', size='label',
                   color=C['text_secondary']).pack(anchor='w', padx=28, pady=(0, 8))

        grid1 = ctk.CTkFrame(self.content, fg_color='transparent')
        grid1.pack(fill='x', padx=28, pady=(0, 6))
        grid1.columnconfigure([0, 1], weight=1, uniform='g')

        actions_row1 = [
            ('💰\nBalance\nInquiry',  'balance'),
            ('📤\nCash\nWithdrawal', 'withdrawal'),
        ]
        actions_row2 = [
            ('📥\nCash\nDeposit',   'deposit'),
            ('🔄\nFund\nTransfer',  'transfer'),
        ]

        # Row 1 buttons - FOR LOOP demonstration
        for col, (label, screen) in enumerate(actions_row1):
            self._make_action_card(grid1, label, screen, row=0, col=col)

        grid2 = ctk.CTkFrame(self.content, fg_color='transparent')
        grid2.pack(fill='x', padx=28, pady=(0, 6))
        grid2.columnconfigure([0, 1], weight=1, uniform='g')

        # Row 2 buttons - FOR LOOP
        for col, (label, screen) in enumerate(actions_row2):
            self._make_action_card(grid2, label, screen, row=0, col=col)

        # Secondary actions row
        sec_frame = ctk.CTkFrame(self.content, fg_color='transparent')
        sec_frame.pack(fill='x', padx=28, pady=(0, 16))
        sec_frame.columnconfigure([0, 1, 2], weight=1, uniform='s')

        secondary = [
            ('📋\nHistory',  'history'),
            ('👤\nAccount\nInfo', 'account_info'),
            ('ℹ\nAbout',   'about'),
        ]
        # FOR LOOP: create secondary buttons
        for col, (label, screen) in enumerate(secondary):
            btn = ctk.CTkButton(
                sec_frame, text=label,
                command=lambda s=screen: (self.play('click'), self.navigate_to(s)),
                fg_color=C['bg_card'],
                hover_color=C['bg_hover'],
                text_color=C['text_secondary'],
                font=make_font('small'),
                height=68,
                corner_radius=S['card_radius'],
                border_width=1,
                border_color=C['border']
            )
            btn.grid(row=0, column=col, padx=4, pady=0, sticky='ew')

        # ---- Recent Transactions ----
        make_divider(self.content).pack(fill='x', padx=28, pady=(4, 12))
        make_label(self.content, 'Recent Transactions', size='label',
                   color=C['text_secondary']).pack(anchor='w', padx=28, pady=(0, 6))

        self.recent_frame = ctk.CTkFrame(self.content, fg_color='transparent')
        self.recent_frame.pack(fill='x', padx=28, pady=(0, 12))

        # Credits link at bottom
        cred_btn = ctk.CTkButton(
            self.content, text='Developer Credits',
            command=lambda: (self.play('click'), self.navigate_to('credits')),
            fg_color='transparent', hover_color='transparent',
            text_color=C['text_muted'],
            font=make_font('tiny'),
            height=24
        )
        cred_btn.pack(pady=(4, 0))

        # Footer
        self.build_footer(self)

    def _make_action_card(self, parent, label: str, screen: str, row: int, col: int):
        """Create a main action button card."""
        btn = ctk.CTkButton(
            parent, text=label,
            command=lambda s=screen: (self.play('click'), self.navigate_to(s)),
            fg_color=C['bg_card'],
            hover_color=C['bg_elevated'],
            text_color=C['text'],
            font=make_font('small', bold=True),
            height=90,
            corner_radius=S['card_radius'],
            border_width=1,
            border_color=C['border']
        )
        btn.grid(row=row, column=col, padx=4, pady=4, sticky='ew')

    def on_show(self):
        """
        Refresh dashboard with current user data.
        
        Demonstrates: decision structure for null check,
                      data retrieval and display
        """
        # Refresh current user data from file
        self.app.auth.refresh_current_user()
        user = self.app.auth.get_current_user()

        # Decision: check if user is logged in
        if user is None:
            self.navigate_to('login')
            return

        # Update greeting with time-appropriate message
        greeting = get_greeting()
        first_name = user.get('name', 'User').split()[0]
        self.greeting_lbl.configure(text=f"{greeting}, {first_name}")

        # Update account info
        acc_num = user.get('account_number', '')
        self.acc_lbl.configure(text=f"Account: {mask_account(acc_num)}")

        # Update account status label
        status = user.get('status', 'unknown').title()
        if status == 'Active':
            self.status_lbl.configure(text='  ● Active', text_color=C['success'])
        else:
            self.status_lbl.configure(text=f'  ● {status}', text_color=C['warning'])

        # Animate balance count-up
        balance = float(user.get('balance', 0))
        self._animate_balance(0, balance, 30)

        # Update sound button icon
        icon = '🔊' if self.app.sound_enabled else '🔇'
        self.sound_btn.configure(text=icon)

        # Load recent transactions
        self._load_recent_transactions(user.get('account_number'))

    def _animate_balance(self, current: float, target: float, steps_left: int):
        """
        Animate balance number counting up from 0 to target.
        
        Demonstrates: recursion-style loop using after(),
                      decision structure for completion
        """
        if steps_left <= 0:
            self.balance_lbl.configure(text=format_currency(target))
            return

        # Calculate step value
        step_amount = (target - current) / steps_left
        new_amount = current + step_amount

        self.balance_lbl.configure(text=format_currency(new_amount))
        self.after(20, lambda: self._animate_balance(new_amount, target, steps_left - 1))

    def _load_recent_transactions(self, account_number: str):
        """
        Load and display recent transactions.
        
        Demonstrates: for loop iteration, widget creation loop,
                      decision structure for empty state
        """
        # Clear existing transaction widgets
        for widget in self.recent_frame.winfo_children():
            widget.destroy()

        # Get recent transactions
        recent = self.app.txn_manager.get_recent(account_number, count=4)

        # Decision: handle empty state
        if not recent:
            make_label(
                self.recent_frame,
                'No transactions yet.',
                size='small', color=C['text_muted']
            ).pack(pady=8)
            return

        # FOR LOOP: Display each recent transaction
        for txn in recent:
            self._make_txn_row(self.recent_frame, txn)

    def _make_txn_row(self, parent, txn: dict):
        """Create a compact transaction row for the dashboard."""
        row = ctk.CTkFrame(parent, fg_color=C['bg_card'], corner_radius=8,
                           border_width=1, border_color=C['border'])
        row.pack(fill='x', pady=2)

        txn_type = txn.get('type', '')
        amount = float(txn.get('amount', 0))
        color = get_txn_color(txn_type)
        icon = get_txn_icon(txn_type)
        label = get_txn_type_display(txn_type)
        amount_str = format_amount_with_sign(amount, txn_type)
        date_str = format_date_short(txn.get('timestamp', ''))

        # Icon + type label
        make_label(row, f"{icon} {label}", size='small', bold=True).pack(
            side='left', padx=12, pady=8
        )

        # Date
        make_label(row, date_str, size='tiny', color=C['text_muted']).pack(
            side='left', padx=4
        )

        # Amount (right side)
        make_label(row, amount_str, size='small', bold=True, color=color).pack(
            side='right', padx=12
        )

    def _toggle_sound(self):
        """Toggle sound on/off."""
        self.app.sound_enabled = self.app.audio.toggle()
        icon = '🔊' if self.app.sound_enabled else '🔇'
        self.sound_btn.configure(text=icon)

    def _logout(self):
        """
        Log out the current user and return to login screen.
        
        Demonstrates: decision structure (confirmation prompt),
                      session clearing
        """
        # Show confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title('Logout')
        dialog.geometry('320x180')
        dialog.grab_set()
        dialog.configure(fg_color=C['bg_card'])
        dialog.resizable(False, False)

        # Center dialog
        dialog.update_idletasks()
        x = self.app.root.winfo_x() + (S['window_width'] - 320) // 2
        y = self.app.root.winfo_y() + (S['window_height'] - 180) // 2
        dialog.geometry(f'+{x}+{y}')

        make_label(dialog, 'Logout', size='subtitle', bold=True).pack(pady=(20, 4))
        make_label(dialog, 'Are you sure you want to logout?',
                   size='small', color=C['text_secondary']).pack()

        btns = ctk.CTkFrame(dialog, fg_color='transparent')
        btns.pack(pady=20)

        def confirm():
            self.play('logout')
            dialog.destroy()
            self.app.auth.logout()
            self.navigate_to('login')

        make_button(btns, 'Cancel', dialog.destroy, style='secondary', width=120).pack(
            side='left', padx=8
        )
        make_button(btns, 'Logout', confirm, style='danger', width=120).pack(side='left', padx=8)


# ============================================================
# SCREEN 4: BALANCE INQUIRY
# ============================================================

class BalanceScreen(BaseScreen):
    """Dedicated balance inquiry screen."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Balance Inquiry', show_back=True, show_brand=True)

        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=40, pady=40)

        # Balance card
        card = make_card(content)
        card.pack(fill='x')

        make_label(card, '💰', size='logo').pack(pady=(24, 8))
        make_label(card, 'Available Balance', size='label',
                   color=C['text_secondary']).pack()

        self.balance_lbl = make_label(
            card, '₱0.00',
            size='balance', bold=True, color=C['accent']
        )
        self.balance_lbl.pack(pady=(8, 20))

        make_divider(card).pack(fill='x', padx=24, pady=0)

        # Account details
        info_frame = ctk.CTkFrame(card, fg_color='transparent')
        info_frame.pack(padx=24, pady=16, fill='x')
        info_frame.columnconfigure([0, 1], weight=1)

        self.name_lbl = make_label(info_frame, '', size='body', bold=True)
        self.name_lbl.grid(row=0, column=0, sticky='w')
        make_label(info_frame, 'Account Holder', size='tiny',
                   color=C['text_muted']).grid(row=1, column=0, sticky='w')

        self.acc_lbl = make_label(info_frame, '', size='body', bold=True)
        self.acc_lbl.grid(row=0, column=1, sticky='e')
        make_label(info_frame, 'Account Number', size='tiny',
                   color=C['text_muted']).grid(row=1, column=1, sticky='e')

        make_label(card, '● Account Active', size='small',
                   color=C['success']).pack(pady=(0, 20))

        make_button(content, '← Back to Menu', self.go_back,
                    style='secondary', width=200).pack(pady=20)

        self.build_footer(self)

    def on_show(self):
        user = self.app.auth.get_current_user()
        if user:
            self.balance_lbl.configure(
                text=format_currency(float(user.get('balance', 0)))
            )
            self.name_lbl.configure(text=user.get('name', ''))
            self.acc_lbl.configure(
                text=mask_account(user.get('account_number', ''))
            )


# ============================================================
# SCREEN 5: CASH WITHDRAWAL
# ============================================================

class WithdrawalScreen(BaseScreen):
    """
    Cash withdrawal screen.
    
    Features:
      - Amount input with validation
      - Quick amount buttons
      - Real-time balance display
      - Success/failure feedback
    """

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Cash Withdrawal', show_back=True, show_brand=True)

        self.main = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.main.pack(fill='both', expand=True)

        # Balance display
        bal_card = make_card(self.main)
        bal_card.pack(fill='x', padx=28, pady=(16, 12))

        make_label(bal_card, 'Current Balance', size='label',
                   color=C['text_secondary']).pack(pady=(12, 4))
        self.balance_lbl = make_label(
            bal_card, '₱0.00',
            size='amount', bold=True, color=C['accent']
        )
        self.balance_lbl.pack(pady=(0, 12))

        # Input section
        input_card = make_card(self.main)
        input_card.pack(fill='x', padx=28, pady=(0, 12))

        make_label(input_card, 'Enter Withdrawal Amount', size='label',
                   color=C['text_secondary']).pack(pady=(16, 8), padx=20, anchor='w')

        self.amount_entry = make_entry(
            input_card, placeholder='Amount (multiples of ₱100)'
        )
        self.amount_entry.pack(fill='x', padx=20, pady=(0, 4))

        make_label(input_card, 'Amount must be a multiple of ₱100',
                   size='tiny', color=C['text_muted']).pack(padx=20, pady=(0, 8), anchor='w')

        # Quick amount buttons
        make_label(input_card, 'Quick Amounts', size='label',
                   color=C['text_secondary']).pack(padx=20, anchor='w')

        quick_frame = ctk.CTkFrame(input_card, fg_color='transparent')
        quick_frame.pack(fill='x', padx=20, pady=(6, 16))

        # FOR LOOP: Create quick amount buttons
        quick_amounts = [500, 1000, 2000, 5000]
        for i, amt in enumerate(quick_amounts):
            btn = ctk.CTkButton(
                quick_frame,
                text=f'₱{amt:,}',
                command=lambda a=amt: self._set_quick_amount(a),
                fg_color=C['bg_elevated'],
                hover_color=C['bg_hover'],
                text_color=C['text'],
                font=make_font('small', bold=True),
                height=38,
                corner_radius=8,
                width=0
            )
            btn.grid(row=0, column=i, padx=4, pady=0, sticky='ew')
            quick_frame.columnconfigure(i, weight=1)

        # Message area
        self.msg_frame = ctk.CTkFrame(self.main, fg_color='transparent')
        self.msg_frame.pack(fill='x', padx=28)

        # Action buttons
        action_frame = ctk.CTkFrame(self.main, fg_color='transparent')
        action_frame.pack(fill='x', padx=28, pady=(8, 16))

        make_button(action_frame, '📤  Withdraw', self._withdraw,
                    style='primary', height=50, width=None).pack(fill='x', pady=(0, 6))
        make_button(action_frame, 'Clear', self._clear,
                    style='ghost', height=38, width=None).pack(fill='x')

        self.build_footer(self)

    def on_show(self):
        """Refresh balance display when screen opens."""
        self.app.auth.refresh_current_user()
        user = self.app.auth.get_current_user()
        if user:
            self.balance_lbl.configure(
                text=format_currency(float(user.get('balance', 0)))
            )
        self.amount_entry.delete(0, 'end')
        self._clear_msg()

    def _set_quick_amount(self, amount: int):
        """Set the amount field to a quick amount value."""
        self.play('click')
        self.amount_entry.delete(0, 'end')
        self.amount_entry.insert(0, str(amount))

    def _clear(self):
        """Clear the amount field."""
        self.play('click')
        self.amount_entry.delete(0, 'end')
        self._clear_msg()

    def _clear_msg(self):
        """Remove any displayed messages."""
        for w in self.msg_frame.winfo_children():
            w.destroy()

    def _withdraw(self):
        """
        Process the withdrawal.
        
        Demonstrates:
          - Decision structure (if/else)
          - Function calls for validation and processing
          - Transaction feedback
        """
        self.play('click')
        self._clear_msg()

        amount_str = self.amount_entry.get()
        account_number = self.app.auth.get_current_account_number()

        # Execute withdrawal through banking system
        result = self.app.banking.withdraw(account_number, amount_str)

        # Decision: handle result
        if result['success']:
            self.play('success')
            self.app.auth.refresh_current_user()

            # Navigate to success screen
            self.app.success_data = {
                'type': 'Withdrawal',
                'amount': result['amount'],
                'new_balance': result['new_balance'],
                'txn_id': result['txn_id'],
                'icon': '📤',
            }
            self.navigate_to('success')
        else:
            self.play('error')
            self.show_message(self.msg_frame, result['message'], 'error')


# ============================================================
# SCREEN 6: CASH DEPOSIT
# ============================================================

class DepositScreen(BaseScreen):
    """Cash deposit screen."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Cash Deposit', show_back=True, show_brand=True)

        self.main = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.main.pack(fill='both', expand=True)

        # Balance display
        bal_card = make_card(self.main)
        bal_card.pack(fill='x', padx=28, pady=(16, 12))

        make_label(bal_card, 'Current Balance', size='label',
                   color=C['text_secondary']).pack(pady=(12, 4))
        self.balance_lbl = make_label(
            bal_card, '₱0.00',
            size='amount', bold=True, color=C['accent']
        )
        self.balance_lbl.pack(pady=(0, 12))

        # Input section
        input_card = make_card(self.main)
        input_card.pack(fill='x', padx=28, pady=(0, 12))

        make_label(input_card, 'Enter Deposit Amount', size='label',
                   color=C['text_secondary']).pack(pady=(16, 8), padx=20, anchor='w')

        self.amount_entry = make_entry(input_card, placeholder='Amount (min. ₱100)')
        self.amount_entry.pack(fill='x', padx=20, pady=(0, 12))

        # Quick amounts
        make_label(input_card, 'Quick Amounts', size='label',
                   color=C['text_secondary']).pack(padx=20, anchor='w')

        quick_frame = ctk.CTkFrame(input_card, fg_color='transparent')
        quick_frame.pack(fill='x', padx=20, pady=(6, 6))

        # FOR LOOP: quick amounts for deposit
        quick_amounts = [500, 1000, 2000, 5000]
        for i, amt in enumerate(quick_amounts):
            btn = ctk.CTkButton(
                quick_frame, text=f'₱{amt:,}',
                command=lambda a=amt: self._set_quick(a),
                fg_color=C['bg_elevated'], hover_color=C['bg_hover'],
                text_color=C['text'], font=make_font('small', bold=True),
                height=38, corner_radius=8, width=0
            )
            btn.grid(row=0, column=i, padx=4, sticky='ew')
            quick_frame.columnconfigure(i, weight=1)

        quick_frame2 = ctk.CTkFrame(input_card, fg_color='transparent')
        quick_frame2.pack(fill='x', padx=20, pady=(4, 16))

        # Additional quick amounts
        more_amounts = [10000]
        for i, amt in enumerate(more_amounts):
            btn = ctk.CTkButton(
                quick_frame2, text=f'₱{amt:,}',
                command=lambda a=amt: self._set_quick(a),
                fg_color=C['bg_elevated'], hover_color=C['bg_hover'],
                text_color=C['text'], font=make_font('small', bold=True),
                height=38, corner_radius=8, width=0
            )
            btn.grid(row=0, column=i, padx=4, sticky='ew')
            quick_frame2.columnconfigure(i, weight=1)

        # Message area
        self.msg_frame = ctk.CTkFrame(self.main, fg_color='transparent')
        self.msg_frame.pack(fill='x', padx=28)

        # Action buttons
        action_frame = ctk.CTkFrame(self.main, fg_color='transparent')
        action_frame.pack(fill='x', padx=28, pady=(8, 16))

        make_button(action_frame, '📥  Deposit', self._deposit,
                    style='success', height=50, width=None).pack(fill='x', pady=(0, 6))
        make_button(action_frame, 'Clear', self._clear,
                    style='ghost', height=38, width=None).pack(fill='x')

        self.build_footer(self)

    def on_show(self):
        self.app.auth.refresh_current_user()
        user = self.app.auth.get_current_user()
        if user:
            self.balance_lbl.configure(
                text=format_currency(float(user.get('balance', 0)))
            )
        self.amount_entry.delete(0, 'end')
        self._clear_msg()

    def _set_quick(self, amount: int):
        self.play('click')
        self.amount_entry.delete(0, 'end')
        self.amount_entry.insert(0, str(amount))

    def _clear(self):
        self.play('click')
        self.amount_entry.delete(0, 'end')
        self._clear_msg()

    def _clear_msg(self):
        for w in self.msg_frame.winfo_children():
            w.destroy()

    def _deposit(self):
        """
        Process the deposit.
        Demonstrates: validation and transaction processing with decision structure.
        """
        self.play('click')
        self._clear_msg()

        amount_str = self.amount_entry.get()
        account_number = self.app.auth.get_current_account_number()

        result = self.app.banking.deposit(account_number, amount_str)

        # Decision: handle result
        if result['success']:
            self.play('success')
            self.app.auth.refresh_current_user()

            self.app.success_data = {
                'type': 'Deposit',
                'amount': result['amount'],
                'new_balance': result['new_balance'],
                'txn_id': result['txn_id'],
                'icon': '📥',
            }
            self.navigate_to('success')
        else:
            self.play('error')
            self.show_message(self.msg_frame, result['message'], 'error')


# ============================================================
# SCREEN 7: FUND TRANSFER
# ============================================================

class TransferScreen(BaseScreen):
    """Fund transfer screen with confirmation step."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Fund Transfer', show_back=True, show_brand=True)

        self.main = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.main.pack(fill='both', expand=True)

        # Balance display
        bal_card = make_card(self.main)
        bal_card.pack(fill='x', padx=28, pady=(16, 12))

        make_label(bal_card, 'Available Balance', size='label',
                   color=C['text_secondary']).pack(pady=(12, 4))
        self.balance_lbl = make_label(
            bal_card, '₱0.00',
            size='amount', bold=True, color=C['accent']
        )
        self.balance_lbl.pack(pady=(0, 12))

        # Transfer form
        form_card = make_card(self.main)
        form_card.pack(fill='x', padx=28, pady=(0, 12))

        make_label(form_card, 'Transfer Details', size='label',
                   color=C['text_secondary']).pack(pady=(16, 12), padx=20, anchor='w')

        # Recipient Account
        make_label(form_card, 'Recipient Account Number', size='small',
                   color=C['text_secondary']).pack(padx=20, anchor='w')
        self.recipient_entry = make_entry(form_card, placeholder='Account number')
        self.recipient_entry.pack(fill='x', padx=20, pady=(4, 12))

        # Amount
        make_label(form_card, 'Transfer Amount', size='small',
                   color=C['text_secondary']).pack(padx=20, anchor='w')
        self.amount_entry = make_entry(form_card, placeholder='Amount in ₱')
        self.amount_entry.pack(fill='x', padx=20, pady=(4, 12))

        # Note (optional)
        make_label(form_card, 'Note (optional)', size='small',
                   color=C['text_secondary']).pack(padx=20, anchor='w')
        self.note_entry = make_entry(form_card, placeholder='Add a note...')
        self.note_entry.pack(fill='x', padx=20, pady=(4, 16))

        # Message area
        self.msg_frame = ctk.CTkFrame(self.main, fg_color='transparent')
        self.msg_frame.pack(fill='x', padx=28)

        # Action button
        action_frame = ctk.CTkFrame(self.main, fg_color='transparent')
        action_frame.pack(fill='x', padx=28, pady=(8, 16))

        make_button(action_frame, '🔍  Review Transfer', self._review,
                    style='primary', height=50, width=None).pack(fill='x', pady=(0, 6))
        make_button(action_frame, 'Clear', self._clear,
                    style='ghost', height=38, width=None).pack(fill='x')

        self.build_footer(self)

    def on_show(self):
        self.app.auth.refresh_current_user()
        user = self.app.auth.get_current_user()
        if user:
            self.balance_lbl.configure(
                text=format_currency(float(user.get('balance', 0)))
            )
        self._clear()

    def _clear(self):
        self.recipient_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.note_entry.delete(0, 'end')
        self._clear_msg()

    def _clear_msg(self):
        for w in self.msg_frame.winfo_children():
            w.destroy()

    def _review(self):
        """
        Show transfer confirmation dialog before executing.
        Demonstrates: decision structure, confirmation pattern.
        """
        self.play('click')
        self._clear_msg()

        recipient = self.recipient_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        note = self.note_entry.get().strip()
        sender = self.app.auth.get_current_account_number()
        balance = float(self.app.auth.get_current_user().get('balance', 0))
        accounts = self.app.data_manager.load_accounts()

        # Validate using validation module
        from validation import validate_transfer
        result = validate_transfer(amount_str, balance, recipient, sender, accounts)

        if not result.valid:
            self.play('error')
            self.show_message(self.msg_frame, result.message, 'error')
            return

        # Get recipient info for confirmation display
        recipient_info = self.app.data_manager.get_account(recipient)
        recipient_name = recipient_info.get('name', 'Unknown') if recipient_info else 'Unknown'

        amount = float(amount_str)
        self._show_confirmation(sender, recipient, recipient_name, amount, note)

    def _show_confirmation(self, sender, recipient, recipient_name, amount, note):
        """
        Show a confirmation dialog before executing the transfer.
        
        Demonstrates: user confirmation pattern in decision flow.
        """
        dialog = ctk.CTkToplevel(self.app.root)
        dialog.title('Confirm Transfer')
        dialog.geometry('360x320')
        dialog.grab_set()
        dialog.configure(fg_color=C['bg_card'])
        dialog.resizable(False, False)

        # Center dialog
        dialog.update_idletasks()
        x = self.app.root.winfo_x() + (S['window_width'] - 360) // 2
        y = self.app.root.winfo_y() + (S['window_height'] - 320) // 2
        dialog.geometry(f'+{x}+{y}')

        make_label(dialog, '🔄 Confirm Transfer', size='subtitle',
                   bold=True).pack(pady=(20, 16))

        info_card = make_card(dialog)
        info_card.pack(fill='x', padx=20, pady=(0, 16))

        rows = [
            ('From', mask_account(sender)),
            ('To',   f"{recipient_name} ({mask_account(recipient)})"),
            ('Amount', format_currency(amount)),
        ]
        if note:
            rows.append(('Note', note))

        # FOR LOOP: Display transfer details
        for label, value in rows:
            row = ctk.CTkFrame(info_card, fg_color='transparent')
            row.pack(fill='x', padx=16, pady=4)
            make_label(row, label, size='small', color=C['text_muted']).pack(side='left')
            make_label(row, value, size='small', bold=True).pack(side='right')

        btns = ctk.CTkFrame(dialog, fg_color='transparent')
        btns.pack(pady=8)

        def confirm():
            dialog.destroy()
            self._execute_transfer(sender, recipient, str(amount), note)

        make_button(btns, 'Cancel', dialog.destroy, style='secondary', width=140).pack(
            side='left', padx=6
        )
        make_button(btns, '✓ Confirm', confirm, style='primary', width=140).pack(
            side='left', padx=6
        )

    def _execute_transfer(self, sender, recipient, amount_str, note):
        """Execute the confirmed transfer."""
        self.play('click')

        result = self.app.banking.transfer(sender, recipient, amount_str, note)

        if result['success']:
            self.play('success')
            self.app.auth.refresh_current_user()

            self.app.success_data = {
                'type': 'Transfer',
                'amount': result['amount'],
                'new_balance': result['new_balance'],
                'txn_id': result['txn_id'],
                'icon': '🔄',
                'extra': f"To: {result.get('recipient', 'Unknown')}",
            }
            self.navigate_to('success')
        else:
            self.play('error')
            self.show_message(self.msg_frame, result['message'], 'error')


# ============================================================
# SCREEN 8: TRANSACTION SUCCESS
# ============================================================

class SuccessScreen(BaseScreen):
    """Transaction success confirmation screen."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Transaction Complete', show_back=False, show_brand=True)

        self.content = ctk.CTkFrame(self, fg_color='transparent')
        self.content.pack(fill='both', expand=True, padx=40, pady=30)

        # Success card
        self.card = make_card(self.content)
        self.card.pack(fill='x')

        # Dynamic labels
        self.icon_lbl = make_label(self.card, '✓', size='logo', color=C['success'])
        self.icon_lbl.pack(pady=(24, 4))

        self.title_lbl = make_label(self.card, 'Transaction Successful',
                                    size='subtitle', bold=True, color=C['text'])
        self.title_lbl.pack(pady=(0, 16))

        make_divider(self.card).pack(fill='x', padx=24)

        self.details_frame = ctk.CTkFrame(self.card, fg_color='transparent')
        self.details_frame.pack(fill='x', padx=24, pady=16)

        make_button(
            self.content, '🏠  Back to Menu',
            lambda: self.navigate_to('dashboard'),
            style='primary', height=50, width=None
        ).pack(fill='x', pady=(20, 8))

        make_button(
            self.content, 'Another Transaction',
            lambda: self.navigate_to('dashboard'),
            style='secondary', height=44, width=None
        ).pack(fill='x')

        self.build_footer(self)

    def on_show(self):
        """Populate with transaction data."""
        data = getattr(self.app, 'success_data', {})

        # Clear previous details
        for w in self.details_frame.winfo_children():
            w.destroy()

        txn_type = data.get('type', 'Transaction')
        icon = data.get('icon', '✓')
        amount = data.get('amount', 0)
        new_balance = data.get('new_balance', 0)
        txn_id = data.get('txn_id', '')
        extra = data.get('extra', '')

        self.icon_lbl.configure(text=icon)
        self.title_lbl.configure(text=f'{txn_type} Successful')

        # Build detail rows
        details = [
            ('Transaction Type', txn_type),
            ('Amount', format_currency(amount)),
            ('New Balance', format_currency(new_balance)),
            ('Transaction ID', txn_id),
        ]
        if extra:
            details.insert(2, ('Details', extra))

        # FOR LOOP: Display transaction details
        for label, value in details:
            row = ctk.CTkFrame(self.details_frame, fg_color='transparent')
            row.pack(fill='x', pady=4)
            make_label(row, label, size='small',
                       color=C['text_muted']).pack(side='left')
            make_label(row, value, size='small',
                       bold=True).pack(side='right')

        make_label(
            self.details_frame,
            '● Transaction recorded successfully',
            size='tiny', color=C['success']
        ).pack(pady=(8, 0))


# ============================================================
# SCREEN 9: TRANSACTION HISTORY
# ============================================================

class HistoryScreen(BaseScreen):
    """
    Full transaction history with filter tabs.
    
    Demonstrates:
      - for loop for rendering transaction list
      - Decision structure for filter logic
      - Tabbed UI
    """

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Transaction History', show_back=True, show_brand=True)

        # Filter tabs
        self.tab_view = ctk.CTkTabview(
            self,
            fg_color=C['bg_card'],
            segmented_button_fg_color=C['bg_elevated'],
            segmented_button_selected_color=C['primary'],
            segmented_button_selected_hover_color=C['primary_light'],
            segmented_button_unselected_color=C['bg_elevated'],
            segmented_button_unselected_hover_color=C['bg_hover'],
            text_color=C['text'],
        )
        self.tab_view.pack(fill='both', expand=True, padx=16, pady=12)

        # Create tabs
        self.tabs = {}
        tab_names = [
            ('All', None),
            ('Deposits', 'deposit'),
            ('Withdrawals', 'withdrawal'),
            ('Transfers', 'transfer'),
        ]

        for tab_name, filter_val in tab_names:
            tab = self.tab_view.add(tab_name)
            tab.configure(fg_color='transparent')
            self.tabs[tab_name] = (tab, filter_val)

        self.tab_view.configure(command=self._on_tab_change)
        self.build_footer(self)

    def _on_tab_change(self):
        """Reload transactions when tab changes."""
        self.on_show()

    def on_show(self):
        """Load and display transactions for the selected filter."""
        account_number = self.app.auth.get_current_account_number()
        current_tab = self.tab_view.get()
        _, filter_val = self.tabs.get(current_tab, (None, None))

        # Load filtered transactions
        transactions = self.app.txn_manager.get_history(account_number, filter_type=filter_val)

        # Get the current tab's frame
        current_frame = self.tab_view.tab(current_tab)

        # Clear existing content
        for widget in current_frame.winfo_children():
            widget.destroy()

        # Decision: empty state
        if not transactions:
            empty_frame = ctk.CTkFrame(current_frame, fg_color='transparent')
            empty_frame.pack(expand=True, fill='both')

            make_label(
                empty_frame,
                '📋\n\nNo transactions found.',
                size='body', color=C['text_muted']
            ).pack(pady=60)
            return

        # Scrollable list of transactions
        scroll = ctk.CTkScrollableFrame(
            current_frame, fg_color='transparent',
            scrollbar_button_color=C['bg_elevated']
        )
        scroll.pack(fill='both', expand=True, padx=4, pady=4)

        # FOR LOOP: Render each transaction card
        for txn in transactions:
            self._make_txn_card(scroll, txn)

    def _make_txn_card(self, parent, txn: dict):
        """Create a detailed transaction card."""
        txn_type = txn.get('type', '')
        amount = float(txn.get('amount', 0))
        color = get_txn_color(txn_type)
        icon = get_txn_icon(txn_type)
        label = get_txn_type_display(txn_type)
        amount_str = format_amount_with_sign(amount, txn_type)
        date_str = format_datetime(txn.get('timestamp', ''))
        txn_id = txn.get('id', '')
        description = txn.get('description', '')
        bal_after = float(txn.get('balance_after', 0))

        card = ctk.CTkFrame(
            parent, fg_color=C['bg_card'],
            corner_radius=10, border_width=1, border_color=C['border']
        )
        card.pack(fill='x', padx=4, pady=4)

        # Top row: icon + type + amount
        top = ctk.CTkFrame(card, fg_color='transparent')
        top.pack(fill='x', padx=16, pady=(12, 4))

        # Left: icon + label
        left = ctk.CTkFrame(top, fg_color='transparent')
        left.pack(side='left')

        icon_label = make_label(left, icon, size='subtitle')
        icon_label.pack(side='left', padx=(0, 8))

        make_label(left, label, size='body', bold=True).pack(side='left')

        # Right: amount
        make_label(top, amount_str, size='body', bold=True, color=color).pack(side='right')

        # Bottom row: description + date
        bot = ctk.CTkFrame(card, fg_color='transparent')
        bot.pack(fill='x', padx=16, pady=(0, 8))

        if description:
            make_label(bot, description, size='tiny',
                       color=C['text_secondary']).pack(side='left')

        # Date + balance after (right)
        right_info = ctk.CTkFrame(bot, fg_color='transparent')
        right_info.pack(side='right')

        make_label(right_info, date_str, size='tiny',
                   color=C['text_muted']).pack(side='right')

        # Transaction ID (very small)
        make_label(card, txn_id, size='tiny',
                   color=C['text_muted']).pack(padx=16, anchor='w', pady=(0, 6))


# ============================================================
# SCREEN 10: ACCOUNT INFORMATION
# ============================================================

class AccountInfoScreen(BaseScreen):
    """Account information display screen."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Account Information', show_back=True, show_brand=True)

        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=40, pady=30)

        # Profile card
        card = make_card(content)
        card.pack(fill='x')

        make_label(card, '👤', size='logo').pack(pady=(20, 4))
        self.name_lbl = make_label(card, '', size='subtitle', bold=True)
        self.name_lbl.pack()
        self.type_lbl = make_label(card, '', size='small', color=C['text_secondary'])
        self.type_lbl.pack(pady=(2, 16))

        make_divider(card).pack(fill='x', padx=24)

        # Info rows
        self.info_frame = ctk.CTkFrame(card, fg_color='transparent')
        self.info_frame.pack(fill='x', padx=24, pady=16)

        # Status
        self.status_lbl = make_label(card, '● Active', size='small', color=C['success'])
        self.status_lbl.pack(pady=(0, 8))

        # Security note
        note_frame = make_card(content)
        note_frame.pack(fill='x', pady=(16, 0))
        make_label(
            note_frame,
            '🔒  Your PIN is never displayed for security.',
            size='small', color=C['text_muted']
        ).pack(pady=12)

        make_button(content, '← Back to Menu', self.go_back,
                    style='secondary', width=200).pack(pady=20)

        self.build_footer(self)

    def on_show(self):
        """Populate with current user account data."""
        self.app.auth.refresh_current_user()
        user = self.app.auth.get_current_user()
        if not user:
            return

        self.name_lbl.configure(text=user.get('name', ''))
        self.type_lbl.configure(text=user.get('account_type', 'Demo Savings'))

        # Clear and rebuild info rows
        for w in self.info_frame.winfo_children():
            w.destroy()

        rows = [
            ('Account Number', mask_account(user.get('account_number', ''))),
            ('Current Balance', format_currency(float(user.get('balance', 0)))),
            ('Account Type',   user.get('account_type', 'Demo Savings')),
        ]

        # FOR LOOP: Build info rows
        for label, value in rows:
            row = ctk.CTkFrame(self.info_frame, fg_color='transparent')
            row.pack(fill='x', pady=6)

            make_divider(row).pack(fill='x', pady=(0, 6))
            make_label(row, label, size='tiny',
                       color=C['text_muted']).pack(anchor='w')
            make_label(row, value, size='body', bold=True).pack(anchor='w')

        # Status
        status = user.get('status', 'unknown').title()
        if status == 'Active':
            self.status_lbl.configure(text='● Account Active', text_color=C['success'])
        else:
            self.status_lbl.configure(text=f'● {status}', text_color=C['warning'])


# ============================================================
# SCREEN 11: ABOUT
# ============================================================

class AboutScreen(BaseScreen):
    """About page with app info and educational disclaimer."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'About ATMORA', show_back=True, show_brand=True)

        scroll = ctk.CTkScrollableFrame(self, fg_color='transparent')
        scroll.pack(fill='both', expand=True, padx=28, pady=12)

        # App card
        app_card = make_card(scroll)
        app_card.pack(fill='x', pady=(0, 12))

        logo_pil = get_logo(72)
        _logo = ctk.CTkImage(light_image=logo_pil, dark_image=logo_pil, size=(72, 72))
        make_label(app_card, '', image=_logo).pack(pady=(20, 8))
        self._logo_ref = _logo  # Keep reference

        make_label(app_card, 'ATMORA', size='subtitle', bold=True,
                   color=C['accent']).pack()
        make_label(app_card, 'Modern ATM Banking System', size='body',
                   color=C['text_secondary']).pack()
        make_label(app_card, 'Secure  •  Simple  •  Smart Banking', size='small',
                   color=C['text_muted']).pack(pady=(2, 16))

        # Academic info
        info_card = make_card(scroll)
        info_card.pack(fill='x', pady=(0, 12))

        sections = [
            ('📚 Academic Context', [
                ('Course', 'CIT 240 – Open Source Programming'),
                ('Activity', 'Midterm Laboratory Activity No. 5'),
                ('Topic', 'Advanced Python: Decision & Repetition Structures'),
                ('School', 'West Visayas State University – Janiuay Campus'),
                ('Academic Year', '1st Semester SY 2026–2027'),
            ]),
        ]

        for section_title, items in sections:
            make_label(info_card, section_title, size='label', bold=True,
                       color=C['text_secondary']).pack(pady=(16, 8), padx=20, anchor='w')
            for label, value in items:
                row = ctk.CTkFrame(info_card, fg_color='transparent')
                row.pack(fill='x', padx=20, pady=2)
                make_label(row, label, size='small',
                           color=C['text_muted']).pack(side='left')
                make_label(row, value, size='small', bold=True).pack(side='right')

        make_label(info_card, '', size='tiny').pack(pady=4)

        # Features card
        feat_card = make_card(scroll)
        feat_card.pack(fill='x', pady=(0, 12))

        make_label(feat_card, '⚡ Features', size='label', bold=True,
                   color=C['text_secondary']).pack(pady=(16, 8), padx=20, anchor='w')

        features = [
            '✓  Account Authentication with attempt limiting',
            '✓  Balance Inquiry',
            '✓  Cash Withdrawal (with quick amounts)',
            '✓  Cash Deposit (with quick amounts)',
            '✓  Fund Transfer with confirmation',
            '✓  Full Transaction History with filters',
            '✓  Local JSON data persistence',
            '✓  Decision & Repetition structure demos',
        ]
        # FOR LOOP: Display features
        for feat in features:
            make_label(feat_card, feat, size='small',
                       color=C['text_secondary']).pack(padx=20, anchor='w', pady=1)

        make_label(feat_card, '', size='tiny').pack(pady=6)

        # Disclaimer
        disc_card = ctk.CTkFrame(
            scroll, fg_color=C['warning_bg'],
            corner_radius=S['card_radius'], border_width=1, border_color='#5A3A00'
        )
        disc_card.pack(fill='x', pady=(0, 12))

        make_label(disc_card, '⚠  Educational Disclaimer', size='label',
                   bold=True, color=C['warning']).pack(pady=(12, 6), padx=20, anchor='w')
        make_label(
            disc_card,
            'ATMORA is a classroom simulation developed for academic purposes.\n'
            'It does not represent a real banking system.\n'
            'No real financial data or transactions are processed.',
            size='small', color=C['warning'],
            wraplength=600, justify='left'
        ).pack(padx=20, pady=(0, 12), anchor='w')

        make_button(scroll, '← Back to Menu', self.go_back,
                    style='secondary', width=200).pack(pady=16)

        self.build_footer(self)


# ============================================================
# SCREEN 12: CREDITS / DEVELOPER
# ============================================================

class CreditsScreen(BaseScreen):
    """Developer credits and GitHub link screen."""

    def build(self):
        self.configure(fg_color=C['bg_dark'])
        self.build_header(self, 'Developer', show_back=True, show_brand=True)

        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=40, pady=30)

        # Developer card
        card = make_card(content)
        card.pack(fill='x')

        make_label(card, '👨‍💻', size='logo').pack(pady=(24, 8))
        make_label(card, 'Roberto Mediana Jr', size='title', bold=True).pack()
        make_label(card, 'Developer / Programmer', size='body',
                   color=C['text_secondary']).pack(pady=(2, 4))
        make_label(card, 'BSIT — West Visayas State University – Janiuay Campus',
                   size='small', color=C['text_muted']).pack(pady=(0, 16))

        make_divider(card).pack(fill='x', padx=24)

        # GitHub info
        gh_frame = ctk.CTkFrame(card, fg_color='transparent')
        gh_frame.pack(padx=24, pady=16)

        make_label(gh_frame, 'GitHub', size='tiny',
                   color=C['text_muted']).pack(anchor='w')
        make_label(gh_frame, '@midddddiana24', size='subtitle',
                   bold=True, color=C['info']).pack(anchor='w')

        def open_github():
            self.play('click')
            webbrowser.open('https://github.com/midddddiana24')

        make_button(
            card, '  View GitHub Profile  →', open_github,
            style='primary', width=220, height=44
        ).pack(pady=(0, 8))

        make_label(card, 'github.com/midddddiana24', size='small',
                   color=C['text_muted']).pack(pady=(0, 20))

        # Academic info
        acad_card = make_card(content)
        acad_card.pack(fill='x', pady=(16, 0))

        make_label(acad_card, '🎓 Academic Context', size='label',
                   bold=True, color=C['text_secondary']).pack(pady=(12, 8), padx=20, anchor='w')

        acad_info = [
            ('Course', 'CIT 240 – Open Source Programming'),
            ('Activity', 'Midterm Laboratory Activity No. 5'),
            ('School', 'WVSU – Janiuay Campus'),
            ('Year', '1st Semester SY 2026–2027'),
        ]
        # FOR LOOP: Academic info rows
        for label, value in acad_info:
            row = ctk.CTkFrame(acad_card, fg_color='transparent')
            row.pack(fill='x', padx=20, pady=2)
            make_label(row, label, size='small', color=C['text_muted']).pack(side='left')
            make_label(row, value, size='small', bold=True).pack(side='right')

        make_label(acad_card, '', size='tiny').pack(pady=6)

        make_button(content, '← Back', self.go_back,
                    style='secondary', width=160).pack(pady=20)

        self.build_footer(self)


# ============================================================
# MAIN APPLICATION CONTROLLER
# ============================================================

class ATMORAApp:
    """
    Main ATMORA Application.
    
    Manages:
      - Window configuration
      - Screen creation and navigation
      - Service initialization (data, auth, banking, etc.)
      - Session state
      - Sound toggle state
    
    Navigation uses a history stack:
      navigate_to('screen') → pushes to history
      go_back()            → pops from history
    """

    GITHUB_URL = 'https://github.com/midddddiana24'

    def __init__(self):
        # Initialize the root window
        self.root = ctk.CTk()
        self._setup_window()

        # Initialize service layer
        self.data_manager = DataManager()
        self.txn_manager = TransactionManager(self.data_manager)
        self.banking = BankingSystem(self.data_manager, self.txn_manager)
        self.auth = AuthManager(self.data_manager)
        self.audio = AudioManager()

        # Application state
        self.sound_enabled = True
        self.success_data = {}
        self._nav_history = []   # Navigation history stack
        self.current_screen = None

        # Generate and save logo assets
        try:
            from logo_generator import save_logo_assets
            save_logo_assets()
        except Exception:
            pass  # Continue if logo generation fails

        # Create all screens
        self._create_screens()

        # Start with splash screen
        self.navigate_to('splash')

    def _setup_window(self):
        """Configure the main application window."""
        self.root.title('ATMORA | ATM Banking System')
        self.root.geometry(f"{S['window_width']}x{S['window_height']}")
        self.root.resizable(False, False)
        self.root.configure(fg_color=C['bg_darkest'])

        # Set window icon if available
        try:
            icon_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'assets', 'branding', 'atmora_icon.png'
            )
            if os.path.exists(icon_path):
                icon_img = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(True, icon_img)
        except Exception:
            pass

        # Center window on screen
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - S['window_width']) // 2
        y = (sh - S['window_height']) // 2
        self.root.geometry(f"{S['window_width']}x{S['window_height']}+{x}+{y}")

        # Handle window close button
        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

    def _create_screens(self):
        """
        Create all application screens.
        Each screen is a frame placed over the root window.
        
        Demonstrates: dictionary usage, object instantiation
        """
        self.screens = {
            'splash':       SplashScreen(self.root, self),
            'login':        LoginScreen(self.root, self),
            'dashboard':    DashboardScreen(self.root, self),
            'balance':      BalanceScreen(self.root, self),
            'withdrawal':   WithdrawalScreen(self.root, self),
            'deposit':      DepositScreen(self.root, self),
            'transfer':     TransferScreen(self.root, self),
            'success':      SuccessScreen(self.root, self),
            'history':      HistoryScreen(self.root, self),
            'account_info': AccountInfoScreen(self.root, self),
            'about':        AboutScreen(self.root, self),
            'credits':      CreditsScreen(self.root, self),
        }

    def navigate_to(self, screen_name: str):
        """
        Show the named screen and hide all others.
        Pushes current screen to navigation history.
        
        Demonstrates: decision structure, dictionary access
        """
        # Decision: check if screen exists
        if screen_name not in self.screens:
            print(f"Warning: Screen '{screen_name}' not found.")
            return

        # Hide current screen
        if self.current_screen:
            self.current_screen.place_forget()
            self.current_screen.on_hide()
            # Save to history (only save non-splash and non-success to history)
            if self.current_screen not in [self.screens['splash']]:
                self._nav_history.append(self.current_screen)

        # Show new screen
        new_screen = self.screens[screen_name]
        new_screen.place(x=0, y=0, relwidth=1, relheight=1)
        self.current_screen = new_screen

        # Notify screen it's now visible
        new_screen.on_show()

    def go_back(self):
        """
        Navigate to previous screen using history stack.
        Falls back to dashboard if history is empty.
        
        Demonstrates: while loop concept (stack pop),
                      decision structure
        """
        # Decision: check history
        if self._nav_history:
            prev_screen = self._nav_history.pop()

            # Hide current
            if self.current_screen:
                self.current_screen.place_forget()
                self.current_screen.on_hide()

            # Show previous
            prev_screen.place(x=0, y=0, relwidth=1, relheight=1)
            self.current_screen = prev_screen
            prev_screen.on_show()
        else:
            # No history — go to dashboard
            self.navigate_to('dashboard')

    def _on_close(self):
        """
        Handle application close with confirmation.
        Demonstrates: decision structure (if/else)
        """
        dialog = ctk.CTkToplevel(self.root)
        dialog.title('Exit ATMORA')
        dialog.geometry('300x160')
        dialog.grab_set()
        dialog.configure(fg_color=C['bg_card'])
        dialog.resizable(False, False)

        # Center dialog
        x = self.root.winfo_x() + (S['window_width'] - 300) // 2
        y = self.root.winfo_y() + (S['window_height'] - 160) // 2
        dialog.geometry(f'+{x}+{y}')

        make_label(dialog, 'Exit ATMORA?', size='subtitle', bold=True).pack(pady=(20, 6))
        make_label(dialog, 'Are you sure you want to close the ATM system?',
                   size='small', color=C['text_secondary'],
                   wraplength=260).pack()

        btns = ctk.CTkFrame(dialog, fg_color='transparent')
        btns.pack(pady=16)

        def cancel():
            dialog.destroy()

        def exit_app():
            dialog.destroy()
            self.root.quit()
            self.root.destroy()

        make_button(btns, 'Cancel', cancel, style='secondary', width=110).pack(
            side='left', padx=6
        )
        make_button(btns, 'Exit', exit_app, style='danger', width=110).pack(
            side='left', padx=6
        )

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
