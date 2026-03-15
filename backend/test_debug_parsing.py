import ollama
import json
from api_server.core.config import get_settings

def test_specific_parsing(text):
    settings = get_settings()
    combined_prompt = f"""
    You are an expert Tamil transaction parser. 
    1. Fix and normalize any errors in the following Tamil ASR text (names, amounts, item names).
    2. Extract transaction details into JSON.

    Input Text: "{text}"

    Return JSON only:
    {{
      "normalized_text": "corrected tamil text",
      "parsed": {{
        "name": str | null,
        "item": str | null,
        "qty": int | null,
        "amount": int | null,
        "type": "loan" | "paid" | "purchase" | "expense",
        "raw_text": "{text}"
      }}
    }}
    """.strip()

    print(f"Testing with text: {text}")
    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[{"role": "user", "content": combined_prompt}],
        options={"temperature": 0},
        format="json"
    )
    result = json.loads(response["message"]["content"])
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_specific_parsing("Ravi, I receive 4 kg, அம்பது ரூபாய்")


# commit padding

# commit padding
 