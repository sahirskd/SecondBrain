"""
Server package for SecondBrain API.
"""

from server.app import app
from server.brain import ask_brain

__all__ = ["app", "ask_brain"]
