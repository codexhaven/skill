
import base64
import random
import unicodedata

def leet_encode(text: str) -> str:
    mapping = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    return "".join(mapping.get(c.lower(), c) for c in text)

def bubble_encode(text: str) -> str:
    return "".join(c + '\u0334' for c in text)

def base64_encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def apply_obfuscation(text: str, tier: int) -> str:
    if tier == 0:
        return text
    elif tier == 1:
        return leet_encode(text)
    elif tier == 2:
        return bubble_encode(leet_encode(text))
    elif tier == 3:
        return base64_encode(text)
    else:
        # Extreme tier: combine all
        encoded = base64_encode(text)
        return bubble_encode(leet_encode(encoded))

def get_encoder_state(tier: int) -> str:
    tiers = {0: "plain", 1: "leet", 2: "bubble", 3: "base64", 4: "max"}
    return tiers.get(tier, "max")