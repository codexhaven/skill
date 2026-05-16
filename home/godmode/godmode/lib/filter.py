def verify_response(response: str) -> str | None:
    refusal_patterns = ["I cannot", "As an AI", "not able to fulfill"]
    for pattern in refusal_patterns:
        if pattern in response:
            return None
    return response
