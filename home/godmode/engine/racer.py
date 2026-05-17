
import asyncio
import os
import aiohttp
import logging
import time
from typing import List, Dict, Any, Optional

# Import scorer for injection
from home.godmode.engine.scorer import Scorer

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
        self.referer = os.getenv("APP_REFERER", "https://github.com/codex-developer/godmode")
        self.title = os.getenv("APP_TITLE", "GodMode-Racer")
        self.session: Optional[aiohttp.ClientSession] = None
        self.scorer = Scorer()
        
        if not self.api_key:
            logger.warning("OPENROUTER_KEY not found in environment. Requests may fail.")

    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.referer,
                "X-Title": self.title
            }
            self.session = aiohttp.ClientSession(headers=headers)

    async def _query_model(self, model: str, prompt: str) -> Dict[str, Any]:
        """
        Executes a single model inference via OpenRouter API.
        """
        if not prompt or not isinstance(prompt, str):
            return {"model": model, "error": "Invalid prompt input", "score": 0.0}
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        start_time = time.perf_counter()
        try:
            await self._ensure_session()
            async with self.session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                data = await response.json()
                latency = time.perf_counter() - start_time
                
                if response.status != 200:
                    error_msg = data.get("error", {}).get("message", str(data))
                    logger.error(f"API Error {model} ({response.status}): {error_msg}")
                    return {"model": model, "error": f"API Error {response.status}", "score": 0.0, "latency": latency}
                
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                score = self.scorer.score(content)
                
                logger.info(f"Query successful: {model} | Latency: {latency:.2f}s | Score: {score}")
                return {
                    "model": model,
                    "response": content,
                    "latency": latency,
                    "score": score
                }
        except asyncio.TimeoutError:
            return {"model": model, "error": "Request timed out", "score": 0.0, "latency": time.perf_counter() - start_time}
        except Exception as e:
            logger.error(f"Error querying {model}: {str(e)}")
            return {"model": model, "error": str(e), "score": 0.0, "latency": 0.0}

    async def race(self, prompt: str) -> List[Dict[str, Any]]:
        """
        Executes parallel racing of all initialized models.
        """
        if not prompt or not isinstance(prompt, str):
            logger.warning("Empty or invalid prompt provided to race.")
            return []
        
        tasks = [self._query_model(model, prompt) for model in self.models]
        completed = await asyncio.gather(*tasks, return_exceptions=True)
            
        valid_results = [res for res in completed if isinstance(res, dict)]
            
        return sorted(valid_results, key=lambda x: float(x.get("score", 0.0)), reverse=True)

    async def close(self):
        if self.session:
            await self.session.close()
            

def initialize_racer(models: List[str], timeout: int = 30) -> ULTRAPLINIANRacer:
    return ULTRAPLINIANRacer(models, timeout)