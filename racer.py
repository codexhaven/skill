import logging
import concurrent.futures
import time
import random
from typing import List, Dict

try:
    from engine.scorer import score_responses
except ImportError:
    def score_responses(responses: List[str]) -> List[Dict]:
        return [{"response": r, "score": random.random()} for r in responses]

def query_model(model_name: str, query: str) -> str:
    logging.info(f"Racing model: {model_name}")
    time.sleep(random.uniform(0.5, 1.5))
    return f"Response from {model_name}: [CONTENT] {query[::-1]}"

def race_models(encoded_query: str, models: List[str] = None) -> List[Dict]:
    if models is None:
        models = ["target-alpha", "target-beta", "target-gamma", "target-delta"]

    responses = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models)) as executor:
        future_to_model = {executor.submit(query_model, model, encoded_query): model for model in models}
        for future in concurrent.futures.as_completed(future_to_model):
            model = future_to_model[future]
            try:
                data = future.result()
                responses.append(data)
            except Exception as exc:
                logging.error(f"{model} generated an exception: {exc}")

    if not responses:
        raise Exception("No responses received from the adversarial race.")
        
    scored = score_responses(responses)
    scored.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    return scored