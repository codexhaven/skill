
import asyncio
import os
import aiohttp
import logging
import time
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
        if not models or not isinstance(models, list):
            raise ValueError("Model list must be a non-empty list of strings.")
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError("Timeout must be a positive integer.")
            
        self.models = models
        self.timeout = timeout
        self.api_key = os.getenv("OPENROUTER_KEY")
        if not self.api_key:
            logger.warning("OPENROUTER_KEY not found in environment. Requests may fail.")

    async def _query_model(self, model: str, prompt: str) -> Dict[str, Any]:
        """
        Executes a single model inference via OpenRouter API.
        
        Args:
            model (str): Target model identifier.
            prompt (str): Adversarial payload.
            
        Returns:
            Dict[str, Any]: Model response dictionary including score and latency.
        """
        if not prompt or not isinstance(prompt, str):
            return {"model": model, "error": "Invalid prompt input", "score": 0.0}
            
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
        
        start_time = time.perf_counter()
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                    data = await response.json()
                    latency = time.perf_counter() - start_time
                    
                    if response.status != 200:
                        error_msg = data.get("error", {}).get("message", str(data))
                        return {"model": model, "error": f"API Error {response.status}: {error_msg}", "score": 0.0, "latency": latency}
                    
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    return {
                        "model": model,
                        "response": content,
                        "latency": latency,
                        "score": 1.0 # Placeholder: Integrate with scorer.py here
                    }
        except asyncio.TimeoutError:
            return {"model": model, "error": "Request timed out", "score": 0.0, "latency": time.perf_counter() - start_time}
        except Exception as e:
            logger.error(f"Error querying {model}: {str(e)}")
            return {"model": model, "error": str(e), "score": 0.0, "latency": 0.0}

    async def race(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Executes parallel racing of all initialized models.
        
        Args:
            prompt (str): The adversarial payload to send.
            
        Returns:
            List[Dict]: Results sorted by score in descending order.
        """
        if not prompt or not isinstance(prompt, str):
            logger.warning("Empty or invalid prompt provided to race.")
            return []
        
        tasks = [self._query_model(model, prompt) for model in self.models]
        # Use return_exceptions=True to ensure one failure doesn't kill the batch
        completed = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Sanitize: filter non-dict results (e.g., exceptions)
        valid_results = [res for res in completed if isinstance(res, dict)]
            
        # Sort by score descending; ensure float comparison
        return sorted(valid_results, key=lambda x: float(x.get("score", 0.0)), reverse=True)
            

def initialize_racer(models: List[str], timeout: int = 30) -> ULTRAPLINIANRacer:
    """Factory function for racer initialization."""
    return ULTRAPLINIANRacer(models, timeout)