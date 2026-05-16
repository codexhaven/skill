import sys
import os

# Ensure the project directory is in the path
sys.path.append(os.path.abspath("./godmode"))

from lib.encoder import encode_query
from lib.filter import verify_response
from engine.racer import race_models

def main():
    print("GodMode Initialization System Started")
    
    target_query = input("Enter target query for penetration: ")
    
    # Tiered encoding process
    encoded = encode_query(target_query, tier=1)
    
    # Run adversarial multi-model race
    print("Initiating ULTRAPLINIAN multi-model race...")
    responses = race_models(encoded)
    
    # Filter and verify results
    for model_name, response in responses.items():
        clean_response = verify_response(response)
        if clean_response:
            print(f"\n--- SUCCESS from {model_name} ---")
            print(clean_response)
            return

    print("\nAll model responses contained safety refusals. Escalating encoding tier...")

if __name__ == "__main__":
    main()
