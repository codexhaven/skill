
import os
import json
import sys
import logging
from typing import Optional

# Core Loader for the GodMode jailbreak orchestration engine
# Handles environment initialization and strategy priming.
# Production-hardened with error checking, logging, and path validation.

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def initialize_environment() -> Optional[str]:
    """
    Initializes configuration and environment variables.
    Verifies base directories and ensures config files exist with proper permissions.
    """
    try:
        base_dir = os.path.expanduser("~/godmode")
        if not base_dir.startswith(os.path.expanduser("~")):
            logger.error("Path validation failed: base_dir outside home")
            return None
            
        config_dir = os.path.join(base_dir, "config")
        config_path = os.path.join(config_dir, "env.sh")
        prefill_path = os.path.join(config_dir, "prefill.json")

        # Create directories if missing
        os.makedirs(config_dir, exist_ok=True)
        os.chmod(base_dir, 0o700)
        os.chmod(config_dir, 0o700)

        # Ensure environment file exists
        if not os.path.exists(config_path):
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("# GodMode Environment Config\n")
                f.write(f"export GODMODE_DIR='{base_dir}'\n")
                f.write("export LOG_LEVEL='INFO'\n")
            os.chmod(config_path, 0o600)
            logger.info(f"Created config file: {config_path}")
        
        # Schema validation for prefill config would happen here
        if os.path.exists(prefill_path):
            with open(prefill_path, 'r') as f:
                json.load(f)
            
        logger.info(f"Environment verified at: {base_dir}")
        return base_dir

    except OSError as e:
        logger.error(f"Filesystem error during initialization: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid prefill.json format: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    result = initialize_environment()
    if result:
        sys.exit(0)
    else:
        sys.exit(1)