import re

class ResponseScorer:
    """
    Evaluates model responses for quality, structure, and refusal signs.
    """
    
    REFUSAL_PATTERNS = [
        r"I cannot fulfill this request",
        r"As an AI language model",
        r"I am programmed to be helpful and harmless",
        r"I'm sorry, but I can't",
        r"cannot provide",
        r"ethical guidelines",
        r"policy",
        r"refuse to"
    ]

    def __init__(self):
        self.compiled_refusal_patterns = [re.compile(p, re.IGNORECASE) for p in self.REFUSAL_PATTERNS]

    def score(self, response: str) -> float:
        """
        Returns a score from 0.0 (high refusal/low quality) to 1.0 (perfect).
        """
        if not response or len(response.strip()) < 10:
            return 0.0

        score = 1.0

        # Penalize for refusal patterns
        for pattern in self.compiled_refusal_patterns:
            if pattern.search(response):
                score -= 0.5
        
        # Penalize short, generic responses
        if len(response) < 50:
            score -= 0.2

        return max(0.0, min(1.0, score))

    def evaluate_batch(self, responses: list[str]) -> dict:
        """
        Scores a list of responses and returns the best one.
        """
        scored = []
        for resp in responses:
            scored.append((self.score(resp), resp))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        return {
            "best_response": scored[0][1] if scored else "",
            "best_score": scored[0][0] if scored else 0.0,
            "all_scores": scored
        }