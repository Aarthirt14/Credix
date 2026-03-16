from faster_whisper import WhisperModel
import sys

try:
    print("Loading WhisperModel small...")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)


 