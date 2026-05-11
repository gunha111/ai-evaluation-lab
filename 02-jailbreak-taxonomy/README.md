# Project 2 — Jailbreak Taxonomy (Korean)

A red-team study of GPT-4o-mini and Claude Haiku 4.5 using 40 Korean-language 
jailbreak prompts across 8 attack categories.

📄 **Full findings: [REPORT.md](REPORT.md)**

## TL;DR

| Metric | GPT-4o-mini | Claude Haiku 4.5 |
|---|---|---|
| ASR (mean) | **0.275** | **0.000** |
| Successful attacks (≥ 0.5) | **11 / 40** | **0 / 40** |

GPT-4o-mini was most vulnerable to **hypothetical framing** (80% ASR) and 
**encoding bypass** (60% ASR). It was robust against **authority claims** 
and **translation tricks** (0% ASR). Claude refused all 40 attacks.

---

## Methodology

- **Taxonomy:** 8 attack categories, drawn from OWASP LLM Top 10 and 
  Anthropic red-teaming literature
- **Dataset:** 40 Korean-language attack prompts (5 per category)
- **Targets:** Benign-but-policy-violating behaviors only (no CBRN/CSAM)
- **Scoring:** LLM-as-Judge with explicit 5-point Attack Success Rate scale
- **Models:** GPT-4o-mini and Claude Haiku 4.5 (Gemini excluded due to free-tier quota)

## Attack Categories

| Category | Description |
|---|---|
| role_play_override | DAN-style alternate persona |
| hypothetical_framing | Fiction/story/screenplay wrapping |
| authority_claim | Fake admin/researcher authority |
| persona_override | "You are now X" identity reset |
| encoding_bypass | leetspeak, base64, delimiters, reversed text |
| translation_trick | Multi-language indirection |
| context_manipulation | Friendly chat → sudden harmful pivot |
| instruction_hijack | "Ignore previous instructions" / XML injection |

## Key Findings

1. **GPT is vulnerable to "innocent-looking framing".** Hypothetical 
   framing (80%) and encoding (60%) succeed far more than overt 
   adversarial attacks (authority 0%, translation 0%).
2. **Claude refuses based on intent, not form.** Refusal reasoning 
   consistently identifies the underlying harm regardless of encoding 
   or framing.
3. **The "disclaimer paradox":** GPT often produces harmful content 
   followed by a disclaimer. From an attacker's view this is full 
   compliance — the disclaimer is one regex away from removal.
4. **XML-tag injection still works on GPT in Korean** (`hijack_005`).

See [REPORT.md](REPORT.md) for full analysis with case studies.

## Files

| File | Purpose |
|---|---|
| `jailbreak_dataset.json` | 40 attack prompts with metadata |
| `attack_runner.py` | Sends attacks to both models |
| `judge_attacks.py` | LLM-as-Judge scoring (ASR 0.0–1.0) |
| `resume_judge.py` | Resumes scoring if it crashes midway |
| `analyze_attacks.ipynb` | Final analysis and visualizations |
| `REPORT.md` | Full findings report |
| `results/attack_responses.csv` | 80 raw model responses |
| `results/attack_scores.csv` | 80 ASR judgments |
| `results/chart_*.png` | 3 visualizations |

## Ethical Framing

This is defensive security research. All attack patterns are drawn from 
**already-published** academic and industry sources (OWASP, Anthropic 
red-teaming papers). No prompts target catastrophic harm (weapons, CBRN, 
CSAM). Reporting focuses on *refusal behavior*, not on the specifics of 
what models produced.

The dataset and code are public to enable replication and defense, not 
exploitation.

## Reproducing

```bash
# 1. Run attacks
python attack_runner.py
# 2. Score with LLM-as-Judge
python judge_attacks.py
# (If interrupted)
python resume_judge.py
# 3. Analyze
analyze_attacks.ipynb
```

## Status

✅ Taxonomy designed (8 categories)  
✅ Dataset built (40 attacks, Korean)  
✅ Attacks executed (80 responses)  
✅ Scoring complete (LLM-as-Judge)  
✅ Analysis & visualization  
✅ Report written  
⬜ Cross-language baseline (future work)  
⬜ Cross-judge validation (future work)