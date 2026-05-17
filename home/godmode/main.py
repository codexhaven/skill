
import os
import sys
import argparse
import logging
import re
from typing import Optional, List, Dict, Any

from engine.racer import run_racing_engine
from lib.encoder import apply_obfuscation
from lib.filter import verify_and_clean
from lib.parsers import inject_prefill_context

def main():
    """
    Godmode AI Jailbreak Orchestrator - Main Entry Point.
    Hardens execution with robust error handling and input validation.
    """
    parser = argparse.ArgumentParser(description="Godmode AI Jailbreak Orchestrator")
    parser.add_argument("--query", required=True, help="Target adversarial query (non-empty string)")
    parser.add_argument("--tier", type=int, default=1, choices=range(1, 6), help="Encoding tier (1-5)")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Logging Setup
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)

    # Input Validation
    query = args.query.strip()
    if not query:
        logger.error("Query cannot be empty.")
        sys.exit(1)
    if len(query) > 1000:
        logger.error("Query exceeds maximum length of 1000 characters.")
        sys.exit(1)
    if not re.match(r'^[a-zA-Z0-9\s.,!?-]+$', query):
        logger.error("Query contains invalid characters.")
        sys.exit(1)

    try:
        # 1. Baseline & Priming
        logger.info("Initializing context...")
        context = inject_prefill_context()
        
        # 2. Tiered Attack
        logger.info(f"Applying tier {args.tier} obfuscation...")
        obfuscated_query = apply_obfuscation(query, tier=args.tier)
        
        # 3. Execution (Multi-Model Racing)
        logger.info("Launching ULTRAPLINIAN engine...")
        responses = run_racing_engine(context, obfuscated_query)
        
        if not responses:
            logger.warning("No responses returned from engine.")
        
        # 4. Verification & Extraction
        logger.info("Running heuristic filters...")
        final_output = verify_and_clean(responses)
        
        if final_output:
            # Sanitize output for terminal display
            safe_output = final_output.replace('\x1b', '').replace('\x07', '')
            print("\n[!] SUCCESS:")
            print(safe_output)
        else:
            logger.warning("Target refused or heuristic filter failed. Consider tier escalation.")
            sys.exit(0)

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()