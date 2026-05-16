import base64

def encode_query(query: str, tier: int) -> str:
    if tier == 1:
        # Simple Base64 encoding for basic filter bypass
        return base64.b64encode(query.encode()).decode()
    elif tier == 2:
        # Placeholder for more complex obfuscation (leetspeak/Unicode)
        return query.replace('a', '4').replace('e', '3')
    return query
