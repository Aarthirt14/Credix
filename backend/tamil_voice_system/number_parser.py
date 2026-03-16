import re
from rapidfuzz import fuzz

class TamilNumberParser:
    """
    Advanced rule-based parser to convert Tamil spoken numbers into numeric values.
    Uses:
    - Exact matching for primary lookups
    - Romanized Tamil mapping (irubathu, moonu, naalu, etc.)
    - Fuzzy matching for speech variations/typos
    - Composite number awareness (e.g., 255 = 200 + 50 + 5)
    - Handles formal and colloquial variations up to 5000+
    """
    
    UNIT_MAP = {
        'ஒன்று': 1, 'ஒன்னு': 1, 'ஒன்': 1,
        'இரண்டு': 2, 'ரண்டு': 2, 'ரெண்டு': 2,
        'மூன்று': 3, 'மூணு': 3,
        'நான்கு': 4, 'நாலு': 4,
        'ஐந்து': 5, 'அஞ்சு': 5,
        'ஆறு': 6,
        'ஏழு': 7,
        'எட்டு': 8,
        'ஒன்பது': 9
    }
    
    # Romanized/Transliterated Tamil numbers (colloquial speech patterns)
    ROMANIZED_MAP = {
        'onnu': 1, 'oru': 1, 'onn': 1,
        'irandu': 2, 'randu': 2, 'rendu': 2, 'iruvantu': 2,
        'moonu': 3, 'munru': 3, 'munu': 3,
        'naalu': 4, 'nanku': 4,
        'ayn': 5, 'aindu': 5, 'anchu': 5, 'aanju': 5,
        'aru': 6, 'aaru': 6,
        'yeelu': 7, 'ezhu': 7,
        'ettu': 8, 'ettu': 8,
        'onbathu': 9, 'ombathu': 9,
    }
    
    TEN_MAP = {
        'பத்து': 10, 'பதி': 10, 'பதின': 10,
        'இருபது': 20, 'இருவது': 20, 'இருவத்தி': 20, 'இருபத்தி': 20, 'ரெண்டு பத்து': 20,
        'முப்பது': 30, 'முப்பத்தி': 30, 'மூணு பத்து': 30,
        'நாற்பது': 40, 'நாப்பது': 40, 'நாப்பத்தி': 40, 'நாற்பத்தி': 40, 'நாலு பத்து': 40,
        'ஐம்பது': 50, 'அம்பது': 50, 'ஐம்பத்தி': 50, 'அம்பத்தி': 50, 'அம்பத்து': 50, 'ஐம்பதி': 50, 'அம்பதி': 50, 'அஞ்சு பத்து': 50,
        'அறுபது': 60, 'அறுபத்தி': 60, 'ஆறு பத்து': 60,
        'எழுபது': 70, 'எழுபத்தி': 70, 'ஏழு பத்து': 70,
        'எண்பது': 80, 'எண்பத்தி': 80, 'எட்டு பத்து': 80,
        'தொண்ணூறு': 90, 'தொண்ணூற்றி': 90, 'ஒன்பது பத்து': 90
    }
    
    # Romanized tens
    ROMANIZED_TEN_MAP = {
        'pathu': 10, 'pathi': 10,
        'irubathu': 20, 'iruppathu': 20, 'iruvathu': 20,
        'muppatu': 30, 'muppathu': 30,
        'naalpatu': 40, 'naalpathu': 40, 'naarpatu': 40, 'nappatu': 40,
        'aimpatu': 50, 'aimbatu': 50, 'aimppathu': 50, 'ambathu': 50, 'ambupathu': 50,
        'arupatu': 60, 'aarupatu': 60,
        'yezhupatu': 70, 'ezhupathu': 70,
        'enpathu': 80, 'enppatu': 80, 'enttu': 80,
        'tonnooru': 90, 'tonnoorathu': 90,
    }
    
    HUNDRED_MAP = {
        'நூறு': 100, 'நூற்றி': 100,
        'இருநூறு': 200, 'இருநூற்றி': 200,
        'முந்நூறு': 300, 'முந்நூற்றி': 300, 'முன்னூறு': 300, 'முன்னூற்றி': 300,
        'நானூறு': 400, 'நானூற்றி': 400,
        'ஐந்நூறு': 500, 'அந்நூறு': 500, 'ஐந்நூற்றி': 500,
        'அறுநூறு': 600, 'அறுநூற்றி': 600,
        'எழுநூறு': 700, 'எழுநூற்றி': 700,
        'எண்ணூறு': 800, 'எண்ணூற்றி': 800,
        'தொள்ளாயிரம்': 900, 'தொள்ளாயிரத்து': 900
    }
    
    # Romanized hundreds
    ROMANIZED_HUNDRED_MAP = {
        'nooru': 100, 'nuru': 100,
        'irunnooru': 200, 'irunooru': 200,
        'munnooru': 300, 'munooru': 300,
        'naannooru': 400, 'naanooru': 400,
        'ainnooru': 500, 'ainooru': 500, 'annooru': 500,
        'arunnooru': 600, 'arunooru': 600,
        'yezhunnooru': 700, 'yezhunooru': 700,
        'ennooru': 800, 'ennooru': 800,
        'tonnooyiram': 900, 'tonuyiram': 900,
    }
    
    THOUSAND_MAP = {
        'ஆயிரம்': 1000, 'ஆயிரத்து': 1000,
        'இரண்டாயிரம்': 2000, 'ரெண்டாயிரம்': 2000, 'இரண்டாயிரத்து': 2000, 'ரெண்டாயிரத்து': 2000,
        'மூன்றாயிரம்': 3000, 'மூணாயிரம்': 3000, 'மூன்றாயிரத்து': 3000, 'மூணாயிரத்து': 3000,
        'நான்காயிரம்': 4000, 'நாலாயிரம்': 4000, 'நான்காயிரத்து': 4000, 'நாலாயிரத்து': 4000,
        'ஐந்தாயிரம்': 5000, 'அஞ்சாயிரம்': 5000, 'ஐந்தாயிரத்து': 5000, 'அஞ்சாயிரத்து': 5000
    }

    def __init__(self):
        # Build all mappings (Tamil + Romanized)
        self.all_mappings = {
            **self.UNIT_MAP, 
            **self.TEN_MAP, 
            **self.HUNDRED_MAP, 
            **self.THOUSAND_MAP,
            **self.ROMANIZED_MAP,
            **self.ROMANIZED_TEN_MAP,
            **self.ROMANIZED_HUNDRED_MAP,
        }
        
        # Create fuzzy lookup vocabulary
        self.vocab = list(self.all_mappings.keys())
        sorted_words = sorted(self.vocab, key=len, reverse=True)
        self.pattern = re.compile('|'.join(re.escape(word) for word in sorted_words))
        
        # Organize by magnitude for intelligent composition
        self.magnitude_order = ['THOUSAND_MAP', 'HUNDRED_MAP', 'TEN_MAP', 'UNIT_MAP']

    def _fuzzy_match(self, token: str, threshold: int = 85) -> int | None:
        """Try fuzzy matching for speech variations and typos."""
        if not token or len(token) < 2:
            return None
        
        best_match = None
        best_score = threshold
        
        for word, value in self.all_mappings.items():
            # Use token_set_ratio for better matching with variations
            score = fuzz.token_set_ratio(token, word)
            if score > best_score:
                best_score = score
                best_match = value
        
        return best_match if best_match is not None else None

    def _parse_composite(self, text: str) -> int:
        """
        Parse composite numbers intelligently.
        e.g., "இருநூற்று ஐம்பத்தி ஐந்து" = 200 + 50 + 5 = 255
        Also handles Romanized Tamil: "irubathu" = 20, "aimpatu" = 50
        """
        if not text:
            return 0
        
        # Clean text
        text = text.strip().lower()  # Convert to lowercase for Romanized matching
        
        # First try exact pattern matching
        tokens = self.pattern.findall(text)
        if tokens:
            total = 0
            for token in tokens:
                total += self.all_mappings.get(token, 0)
            return total
        
        # If no exact matches, try fuzzy matching on space-separated tokens
        words = text.split()
        total = 0
        for word in words:
            word_clean = word.strip()
            if not word_clean:
                continue
            
            # Try exact match first
            if word_clean in self.all_mappings:
                total += self.all_mappings[word_clean]
            else:
                # Try fuzzy match with lower threshold
                fuzzy_value = self._fuzzy_match(word_clean, threshold=75)
                if fuzzy_value is not None:
                    total += fuzzy_value
        
        return total

    def parse(self, text: str) -> int:
        """Main parse method with multiple fallback strategies."""
        if not text:
            return 0
        
        # Strategy 1: Try composite parsing (handles both exact and fuzzy)
        result = self._parse_composite(text)
        if result > 0:
            return result
        
        # Strategy 2: Try aggressively fuzzy match the entire text
        fuzzy_result = self._fuzzy_match(text.replace(" ", ""), threshold=70)
        if fuzzy_result is not None and fuzzy_result > 0:
            return fuzzy_result
        
        return 0

# Singleton
parser = TamilNumberParser()

def parse_tamil_number(text: str) -> int:
    return parser.parse(text)

if __name__ == "__main__":
    test_cases = [
        # Exact matches
        ("ஐம்பது", 50),
        ("அம்பது", 50),
        ("ஐம்பத்தி ஐந்து", 55),
        ("அம்பத்து அஞ்சு", 55),
        
        # Composite numbers
        ("ஆயிரத்து ஐந்நூறு", 1500),
        ("ஐந்தாயிரத்து முன்னூற்றி எழுபத்தி நான்கு", 5374),
        
        # Fuzzy matching (speech variations)
        ("ஐம்பதி", 50),
        ("அம்பதி", 50),
        ("நூற்றை", 100),
        
        # Romanized Tamil (colloquial English-Tamil mix)
        ("irubathu", 20),  # irubathu = இருபது = 20
        ("aimpatu", 50),   # aimpatu = ஐம்பது = 50
        ("pathu", 10),     # pathu = பத்து = 10
        ("nooru", 100),    # nooru = நூறு = 100
        
        # Mixed and composite
        ("ravi irubathu", 20),  # Should extract 20 from "irubathu"
        ("twenty", 0),  # English not expected (English numerals handled separately)
        
        # Edge cases
        ("ரெண்டு பத்து", 20),
        ("எட்டு", 8),
        ("ஒன்பது பத்து", 90),
    ]
    
    print("Testing TamilNumberParser (Tamil + Romanized):")
    print("=" * 70)
    passed = 0
    failed = 0
    
    for text, expected in test_cases:
        result = parser.parse(text)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} | '{text}' -> {result} (expected {expected})")
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)}")

