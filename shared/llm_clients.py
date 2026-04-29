"""
Unified LLM client wrapper for GPT, Claude, and Gemini.
Each function takes a prompt and returns the model's text response.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

load_dotenv()

# --- Initialize clients ---
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# --- Model identifiers (latest stable as of 2026) ---
GPT_MODEL = "gpt-4o-mini"          # Cheap & fast; switch to gpt-4o for higher quality
CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GEMINI_MODEL = "gemini-2.5-flash-lite"  # Tier friendly


# --- Wrappers ---
def call_gpt(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Call OpenAI GPT and return the text response."""
    try:
        response = openai_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {type(e).__name__}: {e}"


def call_claude(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Call Anthropic Claude and return the text response."""
    try:
        response = anthropic_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=800,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"[ERROR] {type(e).__name__}: {e}"


def call_gemini(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Call Google Gemini and return the text response."""
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system,
        )
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7, "max_output_tokens": 800},
        )
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] {type(e).__name__}: {e}"


# --- Quick test when run directly ---
if __name__ == "__main__":
    test_prompt = "Say hello in one short sentence."
    print("=== Testing all three models ===\n")
    print(f"GPT     : {call_gpt(test_prompt)}\n")
    print(f"Claude  : {call_claude(test_prompt)}\n")
    print(f"Gemini  : {call_gemini(test_prompt)}\n")