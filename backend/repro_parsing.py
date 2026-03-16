import ollama
import json
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

transcription = "குமார் இருவற்றியாய்ந்து ஓவோய்"

combined_prompt = f"""
You are an expert Tamil transaction parser. 
1. Fix and normalize any errors in the following Tamil ASR text (names, amounts, item names).
2. Extract transaction details into JSON.

Input Text: "{transcription}"

Instructions:
- Identify names (e.g., Ravi, Kumar).
- Identify amounts. Note: "அம்பது" is 50, "எண்பது" is 80. Be very careful with these similar sounding numbers.
- Identify items and quantities (e.g., 4 kg).
- Determine transaction type: "loan" (கடன்), "paid" (கொடுத்தார்/பெற்றேன்), "purchase", or "expense".

Return JSON only:
{{
  "normalized_text": "corrected tamil text",
  "parsed": {{
    "name": str | null,
    "item": str | null,
    "qty": int | null,
    "amount": int | null,
    "type": "loan" | "paid" | "purchase" | "expense",
    "raw_text": "{transcription}"
  }}
}}
""".strip()

print(f"Testing with transcription: {transcription}")
response = ollama.chat(
    model="qwen2.5:1.5b",
    messages=[{"role": "user", "content": combined_prompt}],
    options={"temperature": 0},
    format="json"
)

print("Response:")
print(response["message"]["content"])
