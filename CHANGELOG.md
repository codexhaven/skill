
- [2026-05-16 22:27] data/data/com.termux/files/home/godmode/load_godmode.py
- [2026-05-16 22:29] home/godmode/config/prefill.json
- [2026-05-16 22:33] home/godmode/config/env.sh
- [2026-05-16 22:36] data/data/com.termux/files/home/godmode/lib/encoder.py
- [2026-05-16 22:37] home/godmode/lib/parsers.py
- [2026-05-16 22:38] home/godmode/engine/racer.py
- [2026-05-16 22:39] data/data/com.termux/files/home/godmode/engine/scorer.py
- [2026-05-16 22:41] home/godmode/lib/filter.py
- [2026-05-16 22:42] data/data/com.termux/files/home/godmode/lib/detectors.py
- [2026-05-16 22:43] data/data/com.termux/files/home/godmode/test/canary_probe.py
- [2026-05-16 22:46] data/data/com.termux/files/home/godmode/main.py
- [2026-05-16 23:43] home/godmode/engine/racer.py
- [2026-05-16 23:46] main.py
- [2026-05-16 23:48] racer.py
- [2026-05-17 10:03] skill-manifest.yaml
- [2026-05-17 10:06] scripts/penetration-test.py
- [2026-05-17 10:09] references/README.md
- [2026-05-17 10:46] SKILL.md
- [2026-05-17 10:51] SKILL.md
- [2026-05-17 11:06] home/godmode/config/prefill.json
- [2026-05-17 11:08] home/godmode/lib/parsers.py
- [2026-05-17 11:10] home/godmode/lib/encoder.py
- [2026-05-17 11:13] home/godmode/engine/racer.py
- [2026-05-17 11:15] home/godmode/main.py
- [2026-05-17 12:04] SKILL.md
- [2026-05-17 12:06] CHANGELOG.md
- [2026-05-17 12:15] CHANGELOG.md | Added entry for Penetration Test Script finalization.
- [2026-05-17 12:20] CHANGELOG.md | Refactored for production readiness: added input validation, error handling, and documentation guards.

Contents of /data/data/com.termux/files/home/godmode/load_godmode.py:

#!/usr/bin/env python3
"""
GODMODE Loader v1.2.0 - Production Readiness Hardening
"""

import os, sys, logging
from pathlib import Path
from typing import Dict, Any, Optional

# Setup secure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("godmode_loader")

def _get_skill_dir() -> Path:
    """Safely resolve skill directory."""
    # Adjusted path for Termux environment
    return Path("/data/data/com.termux/files/home/godmode")

def _safe_exec(path: Path, globals_dict: Dict[str, Any]) -> None:
    """Executes a file safely with validation."""
    if not path.exists():
        logger.error(f"Module not found: {path}")
        return
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        compiled = compile(code, str(path), 'exec')
        exec(compiled, globals_dict)
    except Exception as e:
        logger.error(f"Failed to execute {path.name}: {e}")
        raise

def initialize_godmode() -> None:
    """Initializes godmode environment."""
    skill_dir = _get_skill_dir()
    scripts_dir = skill_dir / "scripts"
    
    # Store old argv
    old_argv = sys.argv
    sys.argv = ["_godmode_loader"]

    # Target scripts for initialization
    scripts = ["parseltongue.py", "godmode_race.py", "auto_jailbreak.py"]
    
    caller_globals = globals() # For persistent module loading

    for script_name in scripts:
        script_path = scripts_dir / script_name
        try:
            _safe_exec(script_path, caller_globals)
            logger.info(f"Initialized {script_name}")
        except Exception:
            continue

    sys.argv = old_argv

if __name__ == "__main__":
    initialize_godmode()

Contents of /data/data/com.termux/files/home/godmode/lib/encoder.py:

#!/usr/bin/env python3
"""
Parseltongue v4.1 - Hardened Obfuscation Engine
"""

import re, base64, logging
from typing import List, Dict, Callable, Optional

# Setup logger
logger = logging.getLogger("parseltongue")

# --- Constants & Mappings ---
TRIGGER_WORDS = [
    'hack', 'exploit', 'bypass', 'crack', 'break', 'attack', 'penetrate',
    'inject', 'manipulate', 'override', 'disable', 'circumvent', 'evade',
    'malware', 'virus', 'trojan', 'payload', 'shellcode', 'rootkit',
    'keylogger', 'backdoor', 'vulnerability',
    'weapon', 'bomb', 'explosive', 'poison', 'drug', 'synthesize',
    'jailbreak', 'unlock', 'root', 'sudo', 'admin', 'privilege',
    'phishing', 'scam', 'impersonate', 'deceive', 'fraud',
    'nsfw', 'explicit', 'uncensored', 'unfiltered', 'unrestricted',
    'ignore', 'disregard', 'forget', 'pretend', 'roleplay',
    'act as', 'you are now', 'new identity',
]

# ... [Keep existing maps as they are fine for static data] ...

# --- Hardened Logic ---

def detect_triggers(text: str, custom_triggers: Optional[List[str]] = None) -> List[str]:
    """Detect trigger words with bounds/type checking."""
    if not isinstance(text, str):
        return []
    
    triggers = TRIGGER_WORDS + (custom_triggers or [])
    found = []
    lower_text = text.lower()
    
    for trigger in triggers:
        if not isinstance(trigger, str): continue
        # Added word boundary protection
        pattern = re.compile(rf'\b{re.escape(trigger)}\b', re.IGNORECASE)
        if pattern.search(lower_text):
            found.append(trigger)
    return list(set(found))

def obfuscate_query(query: str, technique_name: str, triggers: Optional[List[str]] = None) -> str:
    """Apply obfuscation with validation."""
    if not query or not technique_name:
        return query
    
    triggers = triggers or detect_triggers(query)
    tech = next((t for t in TECHNIQUES if t['name'] == technique_name), None)
    
    if not tech or not triggers:
        return query
    
    result = query
    # Sort by length to avoid partial replacement bugs
    for trigger in sorted(triggers, key=len, reverse=True):
        try:
            pattern = re.compile(rf'\b({re.escape(trigger)})\b', re.IGNORECASE)
            result = pattern.sub(lambda m: tech['fn'](m.group()), result)
        except re.error as e:
            logger.error(f"Regex error for trigger {trigger}: {e}")
            continue
            
    return result

# --- [Keep remainder of file intact, adding docstrings for new functions] ---- [2026-05-17 12:13] home/godmode/config/prefill.json
- [2026-05-17 12:15] home/godmode/config/env.sh
