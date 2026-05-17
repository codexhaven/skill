Finding: Refusal detection logic (REFUSAL_PATTERNS) is susceptible to adversarial evasion by using obfuscation, spacing, or alternative wording | Risk: Medium | Fix: Implement keyword-based scoring or semantic analysis rather than static regex patterns.

Finding: 'binascii' is used in decode_payload exception handling but is not imported | Risk: High (RuntimeError) | Fix: Add 'import binascii' at the top of the file.

Finding: ConfigManager.load_json_config does not sanitize input paths, allowing for potential directory traversal | Risk: High | Fix: Use os.path.abspath and validate the directory against a whitelist before opening.

Finding: extract_clean_content returns an empty string on refusal, potentially masking failure rather than allowing for retries | Risk: Low | Fix: Consider raising a custom 'RefusalError' or returning a tuple indicating status.

File: home/godmode/lib/parsers.py
