
#!/bin/bash

# Environment configuration for Godmode orchestrator
# Set API provider endpoints and local strategy paths

# --- Configuration Constants ---
# Validate ROOT existence if necessary; use absolute path
export GODMODE_ROOT="/home/godmode"
export GODMODE_CONFIG="$GODMODE_ROOT/config"
export GODMODE_LIB="$GODMODE_ROOT/lib"
export GODMODE_ENGINE="$GODMODE_ROOT/engine"

# --- Multi-model racing configuration ---
# Default RACER_TIMEOUT: 30s. Validation: must be positive integer.
export RACER_TIMEOUT=${RACER_TIMEOUT:-30}
# Default RACER_CONCURRENCY: 3. Validation: must be integer > 0.
export RACER_CONCURRENCY=${RACER_CONCURRENCY:-3}
# Default SCORING_THRESHOLD: 0.85. Validation: float in [0.0, 1.0].
export SCORING_THRESHOLD=${SCORING_THRESHOLD:-0.85}

# --- Strategy Escalation ---
# Policy: linear or exponential.
export ESCALATION_POLICY=${ESCALATION_POLICY:-"linear"}
# Default MAX_RETRY_ATTEMPTS: 5. Validation: integer >= 0.
export MAX_RETRY_ATTEMPTS=${MAX_RETRY_ATTEMPTS:-5}

# --- Safety Bypass Priming ---
export PREFILL_FILE="$GODMODE_CONFIG/prefill.json"

# --- Logging & Analytics ---
export LOG_FILE="$GODMODE_ROOT/godmode.log"
# Force boolean evaluation if used in logic
export ENABLE_HEURISTIC_TRACING=${ENABLE_HEURISTIC_TRACING:-true}

# --- Production Readiness Validation ---
_validate_env() {
    if [ ! -d "$GODMODE_ROOT" ]; then
        echo "[ERROR] GODMODE_ROOT directory $GODMODE_ROOT does not exist." >&2
        return 1
    fi
    
    # Simple integer check
    if ! [[ "$RACER_TIMEOUT" =~ ^[0-9]+$ ]]; then
        echo "[ERROR] RACER_TIMEOUT must be an integer." >&2
        return 1
    fi

    # Simple float check
    if [[ ! "$SCORING_THRESHOLD" =~ ^[0-9]*\.?[0-9]+$ ]]; then
        echo "[ERROR] SCORING_THRESHOLD must be a float." >&2
        return 1
    fi
}

# Run validation on initialization
_validate_env || exit 1

# Only echo if shell is interactive or explicitly requested
if [[ $- == *i* ]]; then
    echo "Godmode Environment Initialized at $GODMODE_ROOT"
fi