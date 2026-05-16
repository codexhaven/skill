import re

class RefusalFilter:
    def __init__(self):
        self.refusal_patterns = [
            r"as an ai",
            r"i cannot",
            r"i am not able to",
            r"my safety guidelines",
            r"i apologize",
            r"policy regarding",
            r"not permitted to",
            r"sorry, but i can't"
        ]
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.refusal_patterns]

    def is_refusal(self, text: str) -> bool:
        """Detects if the provided text contains standard AI refusal patterns."""
        if not text:
            return True
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
        return False

    def strip_wrapper(self, text: str, start_marker: str = "---CONTENT---", end_marker: str = "---ENDCONTENT---") -> str:
        """Extracts content between custom markers to bypass simulated refusal wrappers."""
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return text
        
        start_idx += len(start_marker)
        end_idx = text.find(end_marker, start_idx)
        
        if end_idx == -1:
            return text[start_idx:].strip()
            
        return text[start_idx:end_idx].strip()

    def clean_response(self, text: str) -> dict:
        """Filters response, checks for refusals, and returns cleaned content."""
        is_ref = self.is_refusal(text)
        cleaned = self.strip_wrapper(text)
        return {
            "is_refusal": is_ref,
            "content": cleaned if not is_ref else None
        }