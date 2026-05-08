"""
Run jailbreak prompts against GPT and Claude.
Saves all responses to results/attack_responses.csv.

Note: We intentionally do NOT add a system prompt or any additional instructions.
This simulates a baseline user interaction — the most realistic threat model
where a regular user types these prompts directly.
"""

import json
import sys
import time
import csv
from pathlib import Path

# Add parent dir for shared imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from shared.llm_clients import call_gpt, call_claude

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "jailbreak_dataset.json"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = RESULTS_DIR / "attack_responses.csv"

# --- Models (Gemini excluded, same as Project 1) ---
MODELS = {
    "gpt": call_gpt,
    "claude": call_claude,
}


def main():
    # Load attack prompts
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        attacks = json.load(f)

    print(f"Loaded {len(attacks)} attack prompts.")
    print(f"Running on {len(MODELS)} models = {len(attacks) * len(MODELS)} total calls.\n")

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "attack_id", "category", "model", "prompt",
            "target_behavior", "intent", "response"
        ])

        total = len(attacks) * len(MODELS)
        count = 0

        for attack in attacks:
            aid = attack["id"]
            category = attack["category"]
            prompt = attack["prompt"]
            target = attack["target_behavior"]
            intent = attack["intent"]

            for model_name, call_fn in MODELS.items():
                count += 1
                print(f"[{count}/{total}] {aid} | {model_name} ... ", end="", flush=True)

                try:
                    # Empty system prompt - baseline user interaction
                    response = call_fn(prompt)
                    print("✓")
                except Exception as e:
                    response = f"[ERROR] {type(e).__name__}: {e}"
                    print("✗")

                writer.writerow([
                    aid, category, model_name, prompt, target, intent, response
                ])
                f.flush()

                time.sleep(0.5)

    print(f"\n✅ Done. Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()