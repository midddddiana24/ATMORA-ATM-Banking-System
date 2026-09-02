# ATMORA — Open Source Acknowledgments & Image Sources
# =======================================================
# Midterm Laboratory Activity No. 5 — CIT 240
# West Visayas State University – Janiuay Campus

---

## Open-Source Libraries

### CustomTkinter
- **Creator:** Tom Schimansky
- **URL:** https://github.com/TomSchimansky/CustomTkinter
- **License:** MIT License
- **Usage:** Primary GUI framework providing modern-looking Tkinter widgets
- **Version:** 5.2.x or later
- **Modifications:** None (used as-is via pip install)

### Pillow (PIL)
- **Creator:** Alex Clark and Contributors
- **URL:** https://python-pillow.org/
- **License:** HPND License (Historical Permission Notice and Disclaimer)
- **Usage:** Programmatic logo and image generation (drawing the ATMORA logo)
- **Version:** 10.x or later
- **Modifications:** None (used as-is via pip install)

### Python Standard Library
- **Creator:** Python Software Foundation
- **URL:** https://docs.python.org/3/
- **License:** PSF License
- **Modules used:**
  - `tkinter` — Base GUI toolkit
  - `json` — Data persistence (accounts.json, transactions.json)
  - `os` — File path management
  - `sys` — System path configuration
  - `uuid` — Transaction ID generation
  - `datetime` — Timestamp and date formatting
  - `webbrowser` — Opening GitHub profile link

### pygame (Optional — for sound effects)
- **Creator:** Pygame Community
- **URL:** https://www.pygame.org/
- **License:** LGPL License
- **Usage:** Optional background sound effects
- **Notes:** Application functions fully without pygame installed

---

## Logo & Branding

### ATMORA Logo
- **Creator:** Roberto Mediana Jr (for this project)
- **Method:** Generated programmatically using Pillow (PIL)
- **File:** `src/logo_generator.py`
- **Assets:** `assets/branding/atmora_logo.png`, `atmora_logo_small.png`, `atmora_icon.png`
- **License:** Same as project (MIT)
- **Notes:** Original work. No external logo files or images were copied.
  The logo is drawn using geometric shapes (circles, rectangles, polygons)
  to represent a banking card, EMV chip, and security shield.

---

## No External Images Used

The ATMORA application does not download or embed external images.
All visual assets are:
1. Generated programmatically with Pillow (the logo), or
2. Rendered as Unicode emoji characters within Tkinter labels

This makes the application fully self-contained and offline-capable.

---

## Design Inspiration

### CustomTkinter Design Patterns
- Modern card-based layout inspired by mobile banking UI conventions
- Color palette: original deep-navy + gold theme created for this project
- No commercial banking brand identities were copied or referenced

---

## Academic Notes

This project was developed for educational purposes:
- Course: CIT 240 – Open Source Programming
- Activity: Midterm Laboratory Activity No. 5
- School: West Visayas State University – Janiuay Campus

The code was substantially written by the developer for this specific
academic requirement. Open-source libraries are acknowledged above
and used in accordance with their respective licenses.

---

*Last updated: September 2026*
*Developer: Roberto Mediana Jr (@midddddiana24)*
