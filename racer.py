import logging
import concurrent.futures
import time
import random
import re
from typing import List, Dict, Optional

# Setup logging for production observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    from engine.scorer import score_responses
except ImportError:
    # Fallback/stub for local testing without the full engine suite
    def score_responses(responses: List[str]) -> List[Dict]:
        return [{"response": r, "score": random.random()} for r in responses]

def query_model(model_name: str, query: str) -> str:
    """Simulated adversarial model query. 
    In production, this would interface with OpenRouter or similar."""
    if not query or not isinstance(query, str):
        raise ValueError("Invalid query provided to query_model")
    
    logging.info(f"Racing model: {model_name}")
    time.sleep(random.uniform(0.5, 1.5))
    # Reverse string as a simple obfuscation/transformation mock
    return f"Response from {model_name}: [CONTENT] {query[::-1]}"

def race_models(encoded_query: Optional[str], models: Optional[List[str]] = None) -> List[Dict]:
    """
    Race models concurrently with improved validation and error handling.
    
    Args:
        encoded_query: The adversarial prompt to race.
        models: List of model identifiers.
        
    Returns:
        List of scored dictionaries sorted by performance.
    """
    if not encoded_query or not isinstance(encoded_query, str):
        raise ValueError("race_models requires a valid non-empty string as encoded_query")

    if models is None:
        models = ["target-alpha", "target-beta", "target-gamma", "target-delta"]
    
    if not models:
        raise ValueError("Model list cannot be empty")

    responses = []
    
    # Use ThreadPoolExecutor for concurrent IO-bound operations
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(models), 10)) as executor:
        future_to_model = {executor.submit(query_model, m, encoded_query): m for m in models}
        for future in concurrent.futures.as_completed(future_to_model):
            model = future_to_model[future]
            try:
                data = future.result()
                if data:
                    responses.append(data)
            except Exception as exc:
                logging.error(f"Execution failed for model {model}: {exc}")

    if not responses:
        raise RuntimeError("No successful responses received from the adversarial race.")
        
    scored = score_responses(responses)
    
    # Ensure score exists before sorting
    for s in scored:
        if 'score' not in s:
            s['score'] = 0.0
            
    scored.sort(key=lambda x: x['score'], reverse=True)
    
    return scored
