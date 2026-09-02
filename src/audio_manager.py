"""
ATMORA - Audio Manager
========================
Manages optional sound effects for the ATM interface.

Sound effects gracefully degrade when:
  - pygame is not installed
  - Sound files are missing
  - Audio hardware is unavailable

The application continues functioning even without audio.

Course: CIT 240 – Open Source Programming
"""

import os

# Attempt to import pygame — not required
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Sound file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUNDS_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

SOUND_FILES = {
    'click':       'click.wav',
    'success':     'success.wav',
    'error':       'error.wav',
    'transaction': 'transaction.wav',
    'logout':      'logout.wav',
}


# ============================================================
# AUDIO MANAGER CLASS
# ============================================================

class AudioManager:
    """
    Manages optional background sound effects.
    
    All methods fail silently if audio is unavailable.
    Demonstrates: error handling, conditional execution (if/else)
    """

    def __init__(self):
        self.enabled = True           # Sound on/off toggle
        self.initialized = False      # Whether pygame loaded successfully
        self.sounds = {}              # Loaded sound objects

        # Try to initialize audio system
        self._initialize()

    def _initialize(self):
        """
        Attempt to initialize pygame audio.
        Fails gracefully if unavailable.
        
        Demonstrates: try/except, nested if
        """
        # Decision: check if pygame is available
        if not PYGAME_AVAILABLE:
            return

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.initialized = True
            self._load_sounds()
        except Exception:
            # Audio hardware unavailable — continue without sound
            self.initialized = False

    def _load_sounds(self):
        """
        Load sound files into memory.
        Missing files are skipped gracefully.
        
        Demonstrates: for loop iteration, error handling
        """
        # FOR LOOP: Try to load each sound file
        for sound_name, filename in SOUND_FILES.items():
            filepath = os.path.join(SOUNDS_DIR, filename)

            # Decision: check if file exists before loading
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    self.sounds[sound_name].set_volume(0.3)
                except Exception:
                    # Could not load this sound — skip it
                    pass

    def play(self, sound_name: str):
        """
        Play a named sound effect.
        
        Fails silently if:
          - Sound is disabled
          - Audio not initialized
          - Sound file not loaded
        
        Demonstrates: nested if decision structure
        """
        # Decision: check multiple conditions before playing
        if not self.enabled:
            return  # Sound is turned off

        if not self.initialized:
            return  # Audio system not available

        if sound_name not in self.sounds:
            return  # Sound file not loaded

        try:
            self.sounds[sound_name].play()
        except Exception:
            pass  # Fail silently

    def toggle(self) -> bool:
        """
        Toggle sound on or off.
        Returns new state (True = enabled).
        
        Demonstrates: boolean toggle
        """
        self.enabled = not self.enabled
        return self.enabled

    def set_enabled(self, state: bool):
        """Set sound enabled state directly."""
        self.enabled = state

    def is_enabled(self) -> bool:
        """Check if sound is currently enabled."""
        return self.enabled and self.initialized

    # Convenience methods for common sounds
    def click(self):
        """Play button click sound."""
        self.play('click')

    def success(self):
        """Play success sound."""
        self.play('success')

    def error(self):
        """Play error sound."""
        self.play('error')

    def transaction(self):
        """Play transaction completion sound."""
        self.play('transaction')

    def logout(self):
        """Play logout sound."""
        self.play('logout')
