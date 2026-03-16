"""
Performance benchmarks for the Tamil number parser.
"""
import time
from tamil_voice_system.number_parser import TamilNumberParser

def benchmark_parser_initialization():
    """Measure parser initialization time."""
    start = time.time()
    parser = TamilNumberParser()
    elapsed = time.time() - start
    print(f"Parser initialization: {elapsed*1000:.2f}ms")
    return parser

def benchmark_tamil_parsing(parser, iterations=1000):
    """Measure parsing of Tamil numbers."""
    test_input = "ஐந்தாயிரத்து முன்னூற்றி எழுபத்தி நான்கு"
    
    start = time.time()
    for _ in range(iterations):
        parser.parse(test_input)
    elapsed = time.time() - start
    
    avg_ms = (elapsed / iterations) * 1000
    print(f"Tamil parsing ({iterations}x): {elapsed:.2f}s avg {avg_ms:.2f}ms/parse")

def benchmark_romanized_parsing(parser, iterations=1000):
    """Measure parsing of Romanized Tamil numbers."""
    test_input = "ravi irubathu twenty rupees"
    
    start = time.time()
    for _ in range(iterations):
        parser.parse(test_input)
    elapsed = time.time() - start
    
    avg_ms = (elapsed / iterations) * 1000
    print(f"Romanized parsing ({iterations}x): {elapsed:.2f}s avg {avg_ms:.2f}ms/parse")

def benchmark_fuzzy_matching(parser, iterations=100):
    """Measure fuzzy matching performance."""
    test_input = "ஐம்பதி"  # Similar to ஐம்பது (50)
    
    start = time.time()
    for _ in range(iterations):
        parser._fuzzy_match(test_input, threshold=75)
    elapsed = time.time() - start
    
    avg_ms = (elapsed / iterations) * 1000
    print(f"Fuzzy matching ({iterations}x): {elapsed:.2f}s avg {avg_ms:.2f}ms/match")

if __name__ == "__main__":
    print("Tamil Number Parser Benchmarks")
    print("=" * 50)
    
    parser = benchmark_parser_initialization()
    print()
    
    benchmark_tamil_parsing(parser)
    benchmark_romanized_parsing(parser)
    benchmark_fuzzy_matching(parser)
    
    print()
    print("Benchmarks complete!")
