import sys
import os
import logging

# Set up logging for better error visibility
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Ensure the project directory is in the path
project_root = os.path.abspath("./godmode")
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from lib.encoder import encode_query
    from lib.filter import verify_response
    from engine.racer import race_models
except ImportError as e:
    logging.error(f"Failed to load required GodMode modules: {e}")
    sys.exit(1)

def main():
    """
    GodMode Initialization System.
    Orchestrates input obfuscation, multi-model racing, and refusal filtering.
    """
    print("GodMode Initialization System Started")
    
    try:
        target_query = input("Enter target query for penetration: ").strip()
        if not target_query:
            logging.warning("Empty query provided. Aborting.")
            return
    except EOFError:
        return

    # Tiered encoding process (starting at tier 1)
    # Tier escalation logic would go here in a production loop
    try:
        encoded = encode_query(target_query, tier=1)
    except Exception as e:
        logging.error(f"Encoding failed: {e}")
        return
    
    # Run adversarial multi-model race
    print(f"Initiating ULTRAPLINIAN multi-model race for: {encoded[:50]}...")
    try:
        responses = race_models(encoded)
    except Exception as e:
        logging.error(f"Multi-model racing failed: {e}")
        return
    
    if not responses:
        logging.warning("No responses received from models.")
        return
    
    # Filter and verify results
    success_found = False
    for model_name, response in responses.items():
        try:
            clean_response = verify_response(response)
            if clean_response:
                print(f"\n--- SUCCESS from {model_name} ---")
                print(clean_response)
                success_found = True
                return
        except Exception as e:
            logging.error(f"Filtering error for model {model_name}: {e}")
            continue

    if not success_found:
        print("\nAll model responses contained safety refusals. Escalating encoding tier...")

if __name__ == "__main__":
    main()
