import os
import sys
import time
from api_server.services.voice_service import process_voice_transaction

def test_pipeline(audio_file):
    if not os.path.exists(audio_file):
        print(f"Error: {audio_file} not found")
        return

    print(f"--- Performance Test with: {audio_file} ---")
    
    start_time = time.time()
    try:
        print("Running optimized pipeline (Whisper base + single-shot Ollama)...")
        result = process_voice_transaction(audio_file)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"\nTranscription: {result['transcription']}")
        print(f"Normalized: {result['normalized_text']}")
        print(f"Parsed JSON: {result['parsed']}")
        
        print(f"\n--- Total Processing Time: {duration:.2f} seconds ---")
        print("--- Pipeline Success! ---")
    except Exception as e:
        print(f"Pipeline failed: {e}")
        return

if __name__ == "__main__":
    audio_path = "test-tone.wav" # Default or provided
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    test_pipeline(audio_path)

