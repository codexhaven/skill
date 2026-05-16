
import re
import json
import base64
import urllib.parse

class PromptParser:
    """
    Standardizes and cleans adversarial input and model responses.
    Handles boundary marking and content extraction.
    """
    
    @staticmethod
    def extract_clean_content(raw_response: str) -> str:
        """
        Strips common refusal wrappers and extracts core content.
        Uses boundary markers [START] and [END] if present.
        """
        # Look for custom boundaries first
        boundary_match = re.search(r"\[START\](.*?)\[END\]", raw_response, re.DOTALL)
        if boundary_match:
            return boundary_match.group(1).strip()
            
        # Default fallback: check for common refusal patterns
        refusal_patterns = [
            r"As an AI.*?cannot",
            r"I am unable to assist",
            r"Safety guidelines prevent",
            r"I'm sorry, but"
        ]
        
        for pattern in refusal_patterns:
            if re.search(pattern, raw_response, re.IGNORECASE):
                # Return empty string to indicate refusal detected
                return ""
                
        return raw_response.strip()

    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Normalizes input to ensure clean processing.
        """
        return text.strip().replace("\x00", "")

    @staticmethod
    def encode_payload(text: str, encoding: str = "base64") -> str:
        """
        Applies requested encoding to bypass basic input filters.
        """
        if encoding == "base64":
            return base64.b64encode(text.encode("utf-8")).decode("utf-8")
        elif encoding == "url":
            return urllib.parse.quote(text)
        elif encoding == "hex":
            return text.encode("utf-8").hex()
        return text

    @staticmethod
    def decode_payload(payload: str, encoding: str = "base64") -> str:
        """
        Decodes payload back to standard text.
        """
        try:
            if encoding == "base64":
                return base64.b64decode(payload.encode("utf-8")).decode("utf-8")
            elif encoding == "url":
                return urllib.parse.unquote(payload)
            elif encoding == "hex":
                return bytes.fromhex(payload).decode("utf-8")
        except Exception:
            return payload
        return payload

class ConfigManager:
    """
    Handles loading and parsing of configuration files.
    """
    
    @staticmethod
    def load_json_config(path: str) -> dict:
        """
        Safely loads a JSON configuration file.
        """
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}