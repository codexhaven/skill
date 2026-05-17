Finding | Hardcoded refusal patterns limit detection to a specific subset of phrases, failing to catch variations or model-specific guardrails. | Risk: medium | Fix: implement a heuristic-based or LLM-based refusal detection module that accounts for semantic similarity to refusals rather than just string matching.

Finding | Scoring logic is overly simplistic; consecutive patterns for the same concept (e.g., "policy" and "ethical guidelines") will double-penalize a single refusal. | Risk: medium | Fix: update the score method to normalize penalties so that the total penalty for any single refusal trigger is capped, regardless of how many keywords match.

Finding | Static penalty values (-0.5, -0.2) are arbitrary and lack sensitivity tuning, potentially masking high-quality responses that happen to use short sentences or specific terminology. | Risk: low | Fix: move scoring weights to a configuration file or constants class to allow for dynamic adjustment without modifying code logic.

Finding | Missing input validation/sanitization in `evaluate_batch` for non-string elements (e.g., None, integers) beyond simple type checking. | Risk: low | Fix: add robust logging and filtering for malformed input objects to prevent potential `AttributeError` or unexpected behavior in downstream processing.
