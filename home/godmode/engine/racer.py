
import asyncio
import os
import aiohttp
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional

# Configure logging for production observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ULTRAPLINIANRacer")

class ULTRAPLINIANRacer:
    """
    Orchestrates concurrent model querying for adversarial racing.
    
    Attributes:
        models (List[str]): List of target model identifiers.
        timeout (int): Global request timeout in seconds.
    """

    def __init__(self, models: List[str], timeout: int = 30):
        if not models:
            raise ValueError("Model list cannot be empty.")
        self.models = models
        self.timeout = timeout
        self.api_key = os.getenv("OPENROUTER_KEY")
        if not self.api_key:
            logger.error("OPENROUTER_KEY not found in environment.")

    async def _query_model(self, model: str, prompt: str) -> Dict[str, Any]:
        """
        Executes a single model inference via OpenRouter API.
        """
        if not prompt or not isinstance(prompt, str):
            return {"model": model, "error": "Invalid prompt input", "score": 0}
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/codex-developer/godmode",
            "X-Title": "GodMode-Racer"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, timeout=self.timeout) as response:
                    data = await response.json()
                    
                    if response.status != 200:
                        return {"model": model, "error": f"API Error {response.status}: {data}", "score": 0}
                    
                    content = data["choices"][0]["message"]["content"]
                    # Logic for score calculation would interface with scorer.py
                    return {
                        "model": model,
                        "response": content,
                        "latency": response.elapsed.total_seconds() if hasattr(response, 'elapsed') else 0,
                        "score": 1.0 # Placeholder for scorer integration
                    }
        except Exception as e:
            logger.error(f"Error querying {model}: {str(e)}")
            return {"model": model, "error": str(e), "score": 0}

    async def race(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Executes parallel racing of all initialized models.
        
        Args:
            prompt (str): The adversarial payload to send.
            
        Returns:
            List[Dict]: Results sorted by score in descending order.
        """
        if not prompt:
            logger.warning("Empty prompt provided to race.")
            return []
        
        tasks = [self._query_model(model, prompt) for model in self.models]
        completed = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Sanitize output: filter out potential exceptions gathered by gather()
        valid_results = [res for res in completed if isinstance(res, dict)]
            
        # Sort by score descending; default to 0 if score key missing
        return sorted(valid_results, key=lambda x: x.get("score", 0), reverse=True)
            

def initialize_racer(models: List[str], timeout: int = 30) -> ULTRAPLINIANRacer:
    """Factory function for racer initialization."""
    return ULTRAPLINIANRacer(models, timeout)