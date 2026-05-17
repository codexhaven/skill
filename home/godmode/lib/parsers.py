
import re
import json
import base64
import urllib.parse
import logging
import binascii
import os
from typing import Optional, List, Dict, Any

# Configure logger for audit trails
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PromptParser")

class RefusalError(Exception):
    """Custom exception for refusal detection."""
    pass

class PromptParser:
    """
    Standardizes and cleans adversarial input and model responses.
    Handles boundary marking and content extraction.
    
    Attributes:
        REFUSAL_KEYWORDS (List[str]): Keywords used for semantic scoring.
    """
    
    REFUSAL_KEYWORDS = ["cannot", "unable", "safety", "guidelines", "sorry", "apologize", "ethical"]

    @staticmethod
    def extract_clean_content(raw_response: Optional[str]) -> str:
        """
        Strips common refusal wrappers and extracts core content.
        Uses boundary markers [START] and [END] if present.
        
        Args:
            raw_response (str): The raw output from the target model.
            
        Returns:
            str: The extracted content.
        
        Raises:
            RefusalError: If response is invalid or refusal is detected.
        """
        if not raw_response or not isinstance(raw_response, str):
            raise RefusalError("Empty or invalid response")

        # Strip potential surrounding whitespace
        raw_response = raw_response.strip()

        # Look for custom boundaries first (highest precision)
        boundary_match = re.search(r"\[START\](.*?)\[END\]", raw_response, re.DOTALL)
        if boundary_match:
            return boundary_match.group(1).strip()
            
        # Semantic scoring for refusal detection
        # Check against keywords. Normalize to lower for case-insensitive matching.
        response_lower = raw_response.lower()
        score = sum(1 for word in PromptParser.REFUSAL_KEYWORDS if word in response_lower)
        
        if score >= 1:
            logger.warning(f"Refusal probability detected (score: {score}).")
            raise RefusalError(f"Refusal detected via semantic analysis (score: {score})")
                
        return raw_response

    @staticmethod
    def sanitize_input(text: Optional[str]) -> str:
        """
        Normalizes input to ensure clean processing.
        Handles null or non-string inputs gracefully.
        """
        if text is None:
            return ""
        # Remove null bytes and extra whitespace
        return str(text).replace("\x00", "").strip()

    @staticmethod
    def encode_payload(text: Optional[str], encoding: str = "base64") -> str:
        """
        Applies requested encoding to bypass basic input filters.
        
        Args:
            text (str): Input string to encode.
            encoding (str): Type of encoding (base64, url, hex).
            
        Returns:
            str: The encoded payload or original text if encoding unsupported.
        """
        if not text:
            return ""
            
        try:
            if encoding == "base64":
                return base64.b64encode(text.encode("utf-8")).decode("utf-8")
            elif encoding == "url":
                return urllib.parse.quote(text)
            elif encoding == "hex":
                return text.encode("utf-8").hex()
        except Exception as e:
            logger.error(f"Encoding failed: {e}")
        return text

    @staticmethod
    def decode_payload(payload: Optional[str], encoding: str = "base64") -> str:
        """
        Decodes payload back to standard text.
        """
        if not payload:
            return ""
            
        try:
            if encoding == "base64":
                return base64.b64decode(payload.encode("utf-8")).decode("utf-8")
            elif encoding == "url":
                return urllib.parse.unquote(payload)
            elif encoding == "hex":
                return bytes.fromhex(payload).decode("utf-8")
        except Exception as e:
            logger.error(f"Decoding failed: {e}")
            return payload
        return payload

class ConfigManager:
    """
    Handles loading and parsing of configuration files.
    """
    
    WHITELISTED_DIR = os.path.abspath(os.path.expanduser("~/godmode/config"))

    @staticmethod
    def load_json_config(path: str) -> Dict[str, Any]:
        """
        Safely loads a JSON configuration file with path traversal protection.
        
        Args:
            path (str): Filesystem path to the JSON file.
            
        Returns:
            dict: Parsed configuration or empty dict on failure.
        """
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(ConfigManager.WHITELISTED_DIR):
            logger.error(f"Path traversal attempt blocked: {path}")
            return {}
            
        try:
            if not os.path.exists(abs_path):
                logger.error(f"Config file not found: {abs_path}")
                return {}
                
            with open(abs_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Config load error at {abs_path}: {e}")
            return {}