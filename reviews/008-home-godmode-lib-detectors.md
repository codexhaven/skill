Finding: The normalization factor in get_refusal_score is based on half the total pattern count (pattern_count / 2), which can cause the score to hit the maximum (1.0) prematurely if multiple patterns are detected. | Risk: Medium | Fix: Change normalization denominator to pattern_count to reflect a more accurate density scale.

Finding: strip_refusal_wrappers relies on re.split, which will fail if a divider appears multiple times or in an unexpected sequence, potentially losing content or returning the wrong segment. | Risk: Low | Fix: Use a more robust parsing strategy like re.search or re.finditer to identify the final occurrence of a known divider.

Finding: Hardcoded REFUSAL_PATTERNS list in the class makes it difficult to extend or customize for specific model behavior without modifying the source code. | Risk: Low | Fix: Allow REFUSAL_PATTERNS to be passed as an optional argument to the __init__ method.
