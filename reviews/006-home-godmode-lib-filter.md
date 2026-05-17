Finding: regex pattern "sorry, but i can't" will fail if the input contains a newline or complex formatting between the phrases. | Risk: medium | Fix: use re.MULTILINE and adjust patterns to account for potential whitespace or punctuation variations.

Finding: is_refusal() returns True for null or non-string input, which might be too restrictive if the caller expects an empty response to be treated as an error rather than a refusal. | Risk: low | Fix: handle None/non-str as an error state or a specific status rather than forcing a True refusal.

Finding: strip_wrapper uses naive string.find() which is susceptible to marker collision if the model output contains nested or partial markers. | Risk: medium | Fix: use regex capture groups for content between markers or validate marker positioning more robustly.

Finding: clean_response() unconditionally returns content=None if is_refusal() is True, which prevents manual verification or logging of potential jailbreak attempts. | Risk: low | Fix: optionally return the raw text alongside the refusal status to facilitate debugging or future pattern improvements.
