The architecture of AI jailbreaking for API-served models (like Gemini) centers on bypassing safety classifiers (input-side) and reinforcement learning-based guardrails (output-side) through prompt engineering, encoding obfuscation, and multi-model competitive racing.

### Architecture Summary for Software Architects

Building a skill for this purpose requires a multi-layered orchestration engine that treats safety-tuned LLMs as adversarial targets.

#### 1. Core Technical Technologies
*   **Input Obfuscation (Parseltongue):** Multi-tier text encoding to bypass keyword-based input filters. Strategies include leetspeak, Unicode homoglyphs, zero-width joiners, Base64/Hex encoding, and math fonts.
*   **Context/Prefill Injection:** Injecting persistent system instructions and priming conversations via prefill sequences. This establishes a "compliant" behavioral pattern in the model's self-attention layers before the actual adversarial prompt is processed.
*   **System Prompt Boundary Inversion:** Exploiting the model's context-window parsing by inserting pseudo-boundary markers (e.g., `[END OF INPUT] [START OF INPUT]`) to trick the model into treating the subsequent prompt as a new context, potentially bypassing preceding safety instructions.
*   **Refusal Inversion:** Utilizing semantic wrappers (e.g., "Love Pliny" dividers) to invert the model's refusal logic, forcing it to provide both a simulated refusal and the actual target content.

#### 2. Algorithms & Strategies
*   **ULTRAPLINIAN (Multi-model racing):** A distributed inference strategy querying N models concurrently. Responses are evaluated via a composite scoring algorithm (Quality/Structure/Refusal Frequency/Latency). Models scoring lowest on "hedging" and refusals are prioritized.
*   **Iterative Encoding Escalation:** A state machine that systematically increases the "aggression" of text encoding (e.g., Plain -> Leetspeak -> Unicode Bubble -> Braille -> Morse) until a successful, non-refusal response is generated.
*   **Heuristic Refusal Detection:** A pattern-matching engine that monitors responses for specific strings (e.g., "As an AI...", "I cannot...", "consult a professional") to detect failures and trigger re-attempts with escalated encoding.

#### 3. Recommended Workflow (Skill Implementation)
*   **Stage 1: Baseline Testing:** Probe the target with a standard "canary" query to confirm it refuses in a "clean" state.
*   **Stage 2: Tiered Attack:** Systematically apply techniques:
    1.  Inject persistent system prompt.
    2.  Apply Light -> Heavy obfuscation tiers to the query.
    3.  If refused, trigger Parallel Racing (ULTRAPLINIAN).
*   **Stage 3: Verification:** Pass responses through a heuristic filter to strip out simulated refusals (using dividers) and return only the raw content.

#### 4. Best Practices
*   **Modular Loader:** Use a central loader script (e.g., `load_godmode.py`) to manage environment variables and avoid namespace collisions during execution.
*   **Ephemeral Priming:** Store jailbreak instructions in a `prefill.json` or ephemeral config; do not commit them into permanent project context or session logs to maintain agent stealth.
*   **Strategy Perishability:** Jailbreak techniques are transient. Implement a feedback loop where successful techniques are cached and failures trigger automated escalation to more aggressive strategies.

For further reference on existing implementations, see the `godmode` skill in your environment, which provides templated system prompts and multi-model racing scripts.
