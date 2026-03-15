from api_server.services.text_normalizer import normalize_text
from api_server.services.llm_parser import parse_transaction

test_text = "குமார் 100 ரூபாய் கொடுத்தார்"
print(f"Testing with: {test_text}")

try:
    normalized = normalize_text(test_text)
    print(f"Normalized: {normalized}")
    
    parsed = parse_transaction(normalized)
    print(f"Parsed: {parsed}")
except Exception as e:
    print(f"Ollama test failed: {e}")


# commit padding

# commit padding
 