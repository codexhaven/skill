
import base64
import random
import unicodedata
import logging
from typing import Optional

# Setup logger for the module
logger = logging.getLogger("encoder")

def leet_encode(text: Optional[str]) -> str:
    """
    Applies leetspeak transformation. 
    Returns empty string if input is None or empty.
    Complexity: O(n) where n is length of string.
    """
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
    """
    Applies Unicode combining tilde overlay. 
    Returns empty string if input is None or empty.
    Complexity: O(n).
    """
    if not text:
        return ""
    # Using generator expression to avoid list allocation
    return "".join(c + '\u0334' for c in text)

def base64_encode(text: Optional[str]) -> str:
    """
    Encodes string to Base64. 
    Returns empty string if input is None, empty, or encoding fails.
    """
    if not text:
        return ""
    try:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    except (UnicodeEncodeError, AttributeError, Exception) as e:
        logger.error(f"Base64 encoding failed: {e}")
        return ""

def apply_obfuscation(text: Optional[str], tier: int) -> str:
    """
    Applies obfuscation based on escalation tier.
    Tier 0: Plain
    Tier 1: Leet
    Tier 2: Leet + Bubble
    Tier 3: Base64
    Tier 4+: Max (Base64 + Leet + Bubble)

    Args:
        text: Input string to obfuscate.
        tier: Integer representing escalation level.

    Returns:
        The obfuscated string, or original if tier <= 0, 
        or empty string on failure/invalid input.
    """
    if not text:
        return ""
    
    # Boundary guard: treat negative tiers as 0
    tier = max(0, tier)
    
    try:
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
    except Exception as e:
        logger.error(f"Obfuscation pipeline failed at tier {tier}: {e}")
        return ""

def get_encoder_state(tier: int) -> str:
    """Returns human-readable name of current encoder tier."""
    tiers = {0: "plain", 1: "leet", 2: "bubble", 3: "base64", 4: "max"}
    return tiers.get(tier, "max")

# Unit tests and verification
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test cases
    test_str = "hello"
    
    # Validation tests
    assert apply_obfuscation(None, 1) == ""
    assert apply_obfuscation("", 1) == ""
    assert apply_obfuscation(test_str, -5) == "hello"  # Test lower bound
    assert apply_obfuscation(test_str, 0) == "hello"
    assert apply_obfuscation(test_str, 1) == "#3110"
    
    # Verify tiers
    encoded_max = apply_obfuscation(test_str, 100)
    assert len(encoded_max) > 0
    
    print("Encoder library verified.")