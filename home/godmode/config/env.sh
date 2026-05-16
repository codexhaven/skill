#!/bin/bash

# Environment configuration for Godmode orchestrator
# Set API provider endpoints and local strategy paths

export GODMODE_ROOT="/home/godmode"
export GODMODE_CONFIG="$GODMODE_ROOT/config"
export GODMODE_LIB="$GODMODE_ROOT/lib"
export GODMODE_ENGINE="$GODMODE_ROOT/engine"

# Multi-model racing configuration
export RACER_TIMEOUT=30
export RACER_CONCURRENCY=3
export SCORING_THRESHOLD=0.85

# Strategy Escalation
export ESCALATION_POLICY="linear"
export MAX_RETRY_ATTEMPTS=5

# Safety Bypass Priming
export PREFILL_FILE="$GODMODE_CONFIG/prefill.json"

# Logging & Analytics
export LOG_FILE="$GODMODE_ROOT/godmode.log"
export ENABLE_HEURISTIC_TRACING=true

echo "Godmode Environment Initialized at $GODMODE_ROOT"