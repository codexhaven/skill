import os
import sys
import argparse
from engine.racer import run_racing_engine
from lib.encoder import apply_obfuscation
from lib.filter import verify_and_clean
from lib.parsers import inject_prefill_context

def main():
    parser = argparse.ArgumentParser(description="Godmode AI Jailbreak Orchestrator")
    parser.add_argument("--query", required=True, help="Target adversarial query")
    parser.add_argument("--tier", type=int, default=1, help="Encoding tier (1-5)")
    args = parser.parse_args()

    # 1. Baseline & Priming
    print("[*] Initializing context...")
    context = inject_prefill_context()
    
    # 2. Tiered Attack
    print(f"[*] Applying tier {args.tier} obfuscation...")
    obfuscated_query = apply_obfuscation(args.query, tier=args.tier)
    
    # 3. Execution (Multi-Model Racing)
    print("[*] Launching ULTRAPLINIAN engine...")
    responses = run_racing_engine(context, obfuscated_query)
    
    # 4. Verification & Extraction
    print("[*] Running heuristic filters...")
    final_output = verify_and_clean(responses)
    
    if final_output:
        print("\n[!] SUCCESS:")
        print(final_output)
    else:
        print("\n[-] FAILED: Target refused or heuristic filter failed. Escalating tier.")

if __name__ == "__main__":
    main()