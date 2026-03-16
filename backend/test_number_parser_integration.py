"""
Integration tests for Tamil number parser with fuzzy matching and Romanized support.
"""
import pytest
from tamil_voice_system.number_parser import TamilNumberParser, parse_tamil_number

class TestTamilNumberParserIntegration:
    """Integration tests for the number parser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = TamilNumberParser()
    
    # Exact Tamil Script Tests
    def test_tamil_unit_numbers(self):
        """Test Tamil script unit numbers."""
        assert self.parser.parse("ஒன்று") == 1
        assert self.parser.parse("இரண்டு") == 2
        assert self.parser.parse("ஐந்து") == 5
        assert self.parser.parse("ஒன்பது") == 9
    
    def test_tamil_tens(self):
        """Test Tamil script tens."""
        assert self.parser.parse("பத்து") == 10
        assert self.parser.parse("இருபது") == 20
        assert self.parser.parse("ஐம்பது") == 50
        assert self.parser.parse("தொண்ணூறு") == 90
    
    def test_tamil_hundreds(self):
        """Test Tamil script hundreds."""
        assert self.parser.parse("நூறு") == 100
        assert self.parser.parse("இருநூறு") == 200
        assert self.parser.parse("ஐந்நூறு") == 500
    
    def test_tamil_composite_numbers(self):
        """Test composite Tamil numbers."""
        assert self.parser.parse("ஆயிரத்து ஐந்நூறு") == 1500
        assert self.parser.parse("ஐந்தாயிரத்து முன்னூற்றி எழுபத்தி நான்கு") == 5374
    
    # Romanized Tamil Tests
    def test_romanized_units(self):
        """Test Romanized Tamil unit numbers."""
        assert self.parser.parse("onnu") == 1
        assert self.parser.parse("irandu") == 2
        assert self.parser.parse("moonu") == 3
        assert self.parser.parse("naalu") == 4
        assert self.parser.parse("ayn") == 5
    
    def test_romanized_tens(self):
        """Test Romanized Tamil tens."""
        assert self.parser.parse("pathu") == 10
        assert self.parser.parse("irubathu") == 20
        assert self.parser.parse("aimpatu") == 50
        assert self.parser.parse("enpathu") == 80
    
    def test_romanized_hundreds(self):
        """Test Romanized Tamil hundreds."""
        assert self.parser.parse("nooru") == 100
        assert self.parser.parse("irunnooru") == 200
        assert self.parser.parse("munnooru") == 300
    
    # Fuzzy Matching Tests
    def test_fuzzy_matching_similar_words(self):
        """Test fuzzy matching for similar sounding numbers."""
        assert self.parser.parse("ஐம்பதி") == 50  # Slight variation of ஐம்பது
        assert self.parser.parse("அம்பதி") == 50  # Slight variation of அம்பது
        assert self.parser.parse("நூற்றை") == 100  # variation of நூறு
    
    def test_fuzzy_matching_typos(self):
        """Test fuzzy matching for typos."""
        # These should match with > 80% similarity
        result = self.parser._fuzzy_match("பத்தु", threshold=75)
        assert result == 10
    
    # Mixed Language Tests
    def test_mixed_english_tamil(self):
        """Test mixed English-Tamil input."""
        # Extract number from mixed input
        assert self.parser.parse("ravi irubathu") == 20
        assert self.parser.parse("kumar aimpatu") == 50
        assert self.parser.parse("test nooru") == 100
    
    # Edge Cases
    def test_empty_input(self):
        """Test edge case: empty input."""
        assert self.parser.parse("") == 0
        assert self.parser.parse(None) == 0
    
    def test_no_number_found(self):
        """Test edge case: input with no number."""
        assert self.parser.parse("ravi") == 0
        assert self.parser.parse("hello tamil") == 0
    
    def test_multiple_numbers(self):
        """Test multiple numbers in input (should sum)."""
        # "இருபது ஐம்பது" = 20 + 50 = 70
        assert self.parser.parse("இருபது ஐம்பது") == 70
        # "பத்து பத்து பத்து" = 10 + 10 + 10 = 30
        assert self.parser.parse("பத்து பத்து பத்து") == 30
    
    # Magnitude Tests
    def test_large_numbers(self):
        """Test large composite numbers."""
        assert self.parser.parse("ஐந்தாயிரம்") == 5000
        assert self.parser.parse("ஐந்தாயிரத்து முன்னூற்றி எழுபத்தி நான்கு") == 5374
    
    # Case Insensitivity Test
    def test_case_insensitive_romanized(self):
        """Test that Romanized parsing is case-insensitive."""
        assert self.parser.parse("IRUBATHU") == 20
        assert self.parser.parse("IruBathu") == 20
        assert self.parser.parse("irubathu") == 20


class TestParseTransactionVoiceInput:
    """End-to-end tests with realistic voice inputs."""
    
    def test_voice_input_ravi_twenty(self):
        """Test parsing 'ravi irubathu roobai' -> Ravi, ₹20."""
        amount = parse_tamil_number("irubathu")
        assert amount == 20
    
    def test_voice_input_with_rupees_keyword(self):
        """Test parsing with rupees keyword."""
        # The amount should be extracted from the Romanized form
        amount = parse_tamil_number("aimpatu roobai")
        assert amount == 50
    
    def test_voice_input_tamil_script(self):
        """Test parsing pure Tamil script voice input."""
        amount = parse_tamil_number("இருபது ரூபாய়")
        assert amount == 20


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
