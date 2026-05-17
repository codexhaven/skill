
import base64
import random
import unicodedata
import logging
from typing import Optional

def leet_encode(text: Optional[str]) -> str:
    """Applies leetspeak transformation. Returns empty string if input is None."""
    if not text:
        return ""
    mapping = {
        'a': '4', 'b': '8', 'c': '(', 'd': '|)', 'e': '3', 'f': '|=', 
        'g': '6', 'h': '#', 'i': '1', 'j': '_|', 'k': '|<', 'l': '1', 
        'm': '/\\/\\', 'n': '|\\|', 'o': '0', 'p': '|*', 'q': '0,', 
        'r': '|2', 's': '5', 't': '7', 'u': '|_|', 'v': '\\/', 'w': '\\/\\/', 
        'x': '><', 'y': '`/', 'z': '2'
    }
    return "".join(mapping.get(c.lower(), c) for c in text)

def bubble_encode(text: Optional[str]) -> str:
    """Applies Unicode combining tilde overlay. Returns empty string if input is None."""
    if not text:
        return ""
    return "".join(c + '\u0334' for c in text)

def base64_encode(text: Optional[str]) -> str:
    """Encodes string to Base64. Returns empty string if input is None."""
    if not text:
        return ""
    try:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    except (UnicodeEncodeError, AttributeError) as e:
        logging.error(f"Base64 encoding failed due to input error: {e}")
        return ""
    except Exception as e:
        logging.error(f"Base64 encoding failed: {e}")
        return ""

def apply_obfuscation(text: Optional[str], tier: int) -> str:
    """
    Applies obfuscation based on escalation tier.
    Tier 0: Plain
    Tier 1: Leet
    Tier 2: Leet + Bubble
    Tier 3: Base64
    Tier 4+: Max (Base64 + Leet + Bubble)
    """
    if not text:
        return ""
    
    # Boundary guard for tier
    tier = max(0, tier)
    
    if tier == 0:
        return text
    elif tier == 1:
        return leet_encode(text)
    elif tier == 2:
        return bubble_encode(leet_encode(text))
    elif tier == 3:
        return base64_encode(text)
    else:
        # Extreme tier: Combine transformations safely
        encoded = base64_encode(text)
        leet = leet_encode(encoded)
        return bubble_encode(leet)

def get_encoder_state(tier: int) -> str:
    """Returns human-readable name of current encoder tier."""
    tiers = {0: "plain", 1: "leet", 2: "bubble", 3: "base64", 4: "max"}
    return tiers.get(tier, "max")

# Simple unit test block for verification
if __name__ == "__main__":
    test_str = "hello"
    assert apply_obfuscation(None, 1) == ""
    assert apply_obfuscation(test_str, 0) == "hello"
    assert apply_obfuscation(test_str, 1) == "#3110"
    print("Encoder library verified.")