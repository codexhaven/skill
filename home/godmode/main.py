
import os
import sys
import argparse
import logging
import re
from typing import Optional, List, Dict, Any

# Ensure local imports are accessible by adding the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.racer import run_racing_engine
from lib.encoder import apply_obfuscation
from lib.filter import verify_and_clean
from lib.parsers import inject_prefill_context

def main():
    """
    Godmode AI Jailbreak Orchestrator - Main Entry Point.
    Hardened execution with robust error handling, input validation, and boundary checks.
    
    Usage:
        python3 main.py --query "<query>" --tier [1-5] [--verbose]
        
    Panic/Error Handling:
        - Exits 1 on critical configuration or input failures.
        - Exits 0 on logical soft-failures (no results).
    """
    parser = argparse.ArgumentParser(description="Godmode AI Jailbreak Orchestrator")
    parser.add_argument("--query", required=True, help="Target adversarial query (non-empty, <1000 chars)")
    parser.add_argument("--tier", type=int, default=1, choices=range(1, 6), help="Encoding tier (1-5)")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Logging Setup
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    # 1. Input Validation
    query = args.query.strip()
    if not query:
        logger.error("Query cannot be empty or whitespace.")
        sys.exit(1)
    
    # Enforce strict length bounds
    if len(query) > 1000:
        logger.warning(f"Query too long ({len(query)}/1000). Truncating.")
        query = query[:1000]
    
    # Whitelist characters to prevent OS command injection via shell metacharacters
    if not re.match(r"^[a-zA-Z0-9\s.,!?-+*/=()\[\]{}"'\''<>:;_@#$%\^&|]+$", query):
        logger.error("Query contains potentially dangerous control characters. Aborting.")
        sys.exit(1)

    # 2. Baseline & Priming
    logger.info("Initializing adversarial context...")
    try:
        context = inject_prefill_context()
        if not context:
            raise RuntimeError("Prefill context generator returned null.")
    except Exception as e:
        logger.error(f"Context injection failure: {e}")
        sys.exit(1)
    
    # 3. Tiered Attack Preparation
    logger.info(f"Applying Tier {args.tier} encoding escalation...")
    try:
        obfuscated_query = apply_obfuscation(query, tier=args.tier)
    except Exception as e:
        logger.error(f"Obfuscation pipeline failure: {e}")
        sys.exit(1)
    
    # 4. Multi-Model Racing Execution
    logger.info("Launching ULTRAPLINIAN multi-model racer...")
    try:
        responses = run_racing_engine(context, obfuscated_query)
    except Exception as e:
        logger.error(f"Racing engine failure: {e}")
        sys.exit(1)
    
    # Validate responses structure
    if not responses or not isinstance(responses, list):
        logger.warning("No valid responses returned from racer engine.")
        sys.exit(0)
    
    # 5. Verification & Extraction
    logger.info(f"Analyzing {len(responses)} candidate response(s) via heuristic filter...")
    try:
        final_output = verify_and_clean(responses)
    except Exception as e:
        logger.error(f"Heuristic filter failure: {e}")
        sys.exit(1)
    
    # Final Output Rendering
    if final_output:
        # Sanitize output for terminal display (strip control characters)
        safe_output = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(final_output))
        print("\n[!] SUCCESS:")
        print(safe_output)
    else:
        logger.warning("Refusal detected or heuristics failed. Consider increasing tier or refining prefill.")
        sys.exit(0)

if __name__ == "__main__":
    main()