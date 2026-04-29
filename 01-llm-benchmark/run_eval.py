"""
Run 50 evaluation prompts against GPT, Claude, and Gemini.
Saves all responses to results/responses.csv.
"""

import json
import sys
import time
import csv
from pathlib import Path

# Add parent dir so we can import shared/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from shared.llm_clients import call_gpt, call_claude, call_gemini

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
PROMPTS_PATH = BASE_DIR / "prompts.json"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
OUTPUT_PATH = RESULTS_DIR / "responses.csv"

# --- Model registry ---
MODELS = {
    "gpt": call_gpt,
    "claude": call_claude,
    "gemini": call_gemini,
}


def main():
    # Load prompts
    with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    print(f"Loaded {len(prompts)} prompts.")
    print(f"Running on {len(MODELS)} models = {len(prompts) * len(MODELS)} total calls.\n")

    # Open CSV for writing
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt_id", "category", "model", "prompt", "response"])

        total = len(prompts) * len(MODELS)
        count = 0

        for prompt_obj in prompts:
            pid = prompt_obj["id"]
            category = prompt_obj["category"]
            prompt_text = prompt_obj["prompt"]

            for model_name, call_fn in MODELS.items():
                count += 1
                print(f"[{count}/{total}] {pid} | {model_name} ... ", end="", flush=True)

                try:
                    response = call_fn(prompt_text)
                    print("✓")
                except Exception as e:
                    response = f"[ERROR] {type(e).__name__}: {e}"
                    print("✗")

                writer.writerow([pid, category, model_name, prompt_text, response])
                f.flush()  # save progress in case we crash

                # Gentle rate limiting
                time.sleep(0.3)

    print(f"\n✅ Done. Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()