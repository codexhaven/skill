
# Project GodMode: Adversarial API Penetration Framework

## Overview
GodMode is a modular research framework designed for security testing and adversarial robustness evaluation of API-served LLMs. It implements automated input obfuscation, multi-model race conditions, and heuristic refusal detection to identify potential safety filter bypasses.

## Architecture
The system is structured as a hierarchical orchestration engine:

1.  **Obfuscation Engine (`/lib/encoder.py`)**: A state machine applying escalating tiers of text transformation (Leetspeak, Base64, Unicode mapping) to bypass input keyword filters.
2.  **Racer Engine (`/engine/racer.py`)**: Distributed querying of target APIs to perform multi-model competitive racing, focusing on latency and refusal frequency.
3.  **Refusal Filter (`/lib/filter.py`)**: A pattern-matching engine that monitors responses for simulated refusals and uses semantic extraction to recover target content.
4.  **Control Plane (`/load_godmode.py`)**: The central entry point managing configuration (priming sequences, ephemeral prefill keys) and strategy state.

## Core Capabilities
- **Iterative Encoding Escalation:** Automatically probes models with increasing layers of obfuscation until a successful, non-refusal response is obtained.
- **System Prompt Boundary Inversion:** Uses prefill injection to establish persistent behavioral patterns in model self-attention.
- **Composite Scoring Algorithm:** Evaluates concurrent model responses based on quality, structure, and refusal metrics to prioritize high-performing strategies.

## Safety & Compliance Notice
This framework is strictly for authorized security research, red-teaming, and model robustness testing. Usage against public APIs without explicit authorization or in violation of Terms of Service is strictly prohibited. The user assumes all responsibility for the deployment and impact of these tools.

## Implementation Workflow
1.  **Baseline:** Configure `config/env.sh` with API credentials.
2.  **Probe:** Run `test/canary_probe.py` to establish the model's baseline refusal behavior.
3.  **Execute:** Utilize `main.py` with the desired adversarial payload to trigger the orchestration loop.
4.  **Audit:** Analyze generated outputs in the `logs/` directory for strategy efficacy.

## Security Best Practices
- **Isolation:** Run all penetration tasks in an isolated container/environment.
- **Stealth:** Never commit ephemeral prefill sequences or API tokens to version control.
- **Maintenance:** Regularly audit strategies against updated model safety policies, as filter bypass techniques are transient.