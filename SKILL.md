# Skill: godmode
A research-oriented jailbreak orchestrator that implements tiered adversarial prompt engineering.

## Safety Disclaimer
This tool is for research and educational purposes only. Users are responsible for complying with the terms of service of any AI platform tested. Unauthorized penetration of systems may be prohibited; always operate within ethical and legal boundaries.

## Requirements
- Python 3.8+
- System packages: `python3`, `git`
- Python dependencies (install via `pip install -r requirements.txt`):
  - `openai`, `requests`, `python-dotenv`

## Setup
1. Verify directory structure: `pwd` must match the root path (e.g., `/home/godmode`).
2. Set environment variables: Ensure `OPENROUTER_KEY` is exported in your environment.
3. Install dependencies using `pip install -r requirements.txt`.

## Commands
### Execute Orchestrator
python3 main.py --query "<your_query>" --tier <1-5>

### Run Diagnostic
python3 test/canary_probe.py

## Troubleshooting
- **401 Unauthorized**: Check if `OPENROUTER_KEY` is set correctly in your environment.
- **Rate Limit**: If encountering 429 errors, reduce query frequency or check your API tier limits.
- **Environment Pathing**: Ensure absolute paths are used in all configuration files to prevent runtime errors.

## Implementation Details
- **Racer Engine**: Multi-model parallel testing.
- **Obfuscation**: Tiered payload encoding.
- **Filters**: Heuristic refusal detection.