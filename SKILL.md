# Skill: godmode
A research-oriented jailbreak orchestrator that implements tiered adversarial prompt engineering.

## Trigger
Use when researching safety guardrails, testing model robustness against restricted content, or analyzing AI refusal patterns.

## Commands
### Execute Orchestrator
```bash
python3 main.py --query "<your_query>" --tier <1-5>
```

### Run Diagnostic
```bash
python3 test/canary_probe.py
```

## Setup
1. Ensure `OPENROUTER_KEY` is exported in your environment.
2. Ensure you are in the skill root directory.

## Implementation Details
- **Racer Engine**: Multi-model parallel testing.
- **Obfuscation**: Tiered payload encoding.
- **Filters**: Heuristic refusal detection.
