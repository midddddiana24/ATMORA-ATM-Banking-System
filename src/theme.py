"""
ATMORA - Theme Configuration
=============================
Professional banking color palette and typography settings.
Course: CIT 240 – Open Source Programming
"""

# ============================================================
# COLOR PALETTE — Deep Navy + Gold Banking Theme
# ============================================================
COLORS = {
    # Backgrounds (dark to light)
    'bg_darkest':   '#060E1A',   # Window root background
    'bg_dark':      '#0A1628',   # Main screen background
    'bg_medium':    '#0F1E35',   # Secondary panels
    'bg_card':      '#132040',   # Card surfaces
    'bg_elevated':  '#1A2D5A',   # Header/sidebar
    'bg_hover':     '#1E3565',   # Hover state

    # Brand colors
    'primary':      '#1565C0',   # Primary blue
    'primary_light':'#1976D2',   # Lighter blue
    'primary_dark': '#0D47A1',   # Darker blue

    # Accent — Gold
    'accent':       '#F5A623',   # Primary gold
    'accent_light': '#FFCC02',   # Bright gold
    'accent_dark':  '#E08C00',   # Deep gold

    # Semantic colors
    'success':      '#4CAF50',   # Success green
    'success_bg':   '#0D2B15',   # Success background
    'warning':      '#FF9800',   # Warning amber
    'warning_bg':   '#2B1A00',   # Warning background
    'error':        '#F44336',   # Error red
    'error_bg':     '#2B0A08',   # Error background
    'info':         '#29B6F6',   # Info blue

    # Text
    'text':         '#FFFFFF',   # Primary text
    'text_secondary':'#90A4AE',  # Secondary text
    'text_muted':   '#546E7A',   # Muted/placeholder text
    'text_accent':  '#F5A623',   # Accented text (balance, etc.)
    'text_success': '#4CAF50',   # Success text
    'text_error':   '#EF5350',   # Error text

    # Borders & dividers
    'border':       '#1E3050',   # Card border
    'border_light': '#263A5A',   # Lighter border
    'divider':      '#0F1E35',   # Divider line

    # Input fields
    'input_bg':     '#0D1E35',   # Input background
    'input_border': '#1E3050',   # Input border
    'input_focus':  '#1565C0',   # Focus border

    # Buttons
    'btn_primary':  '#1565C0',   # Primary button
    'btn_primary_hover': '#1976D2',
    'btn_secondary':'#132040',   # Secondary button
    'btn_secondary_hover': '#1A2D5A',
    'btn_danger':   '#C62828',   # Danger button
    'btn_success':  '#2E7D32',   # Success button

    # Special
    'gold_text':    '#F5A623',   # Balance / money display
    'masked':       '#546E7A',   # Masked account number dots
}

# ============================================================
# TYPOGRAPHY
# ============================================================
FONTS = {
    'family': 'Helvetica',
    'family_mono': 'Courier',
    'logo':     36,
    'title':    22,
    'subtitle': 16,
    'heading':  14,
    'body':     13,
    'small':    11,
    'tiny':     9,
    'balance':  38,
    'amount':   24,
    'label':    12,
}

# ============================================================
# SIZES & SPACING
# ============================================================
SIZES = {
    'window_width':  900,
    'window_height': 660,
    'header_height': 62,
    'footer_height': 36,
    'card_radius':   12,
    'btn_radius':    8,
    'btn_height':    46,
    'btn_width':     160,
    'input_height':  44,
    'padding_sm':    8,
    'padding_md':    16,
    'padding_lg':    24,
    'padding_xl':    36,
    'logo_size':     100,
    'logo_small':    40,
    'icon_size':     20,
}
