import os
from faster_whisper import WhisperModel
from .number_parser import parse_tamil_number
import re

class TamilVoicePipeline:
    """
    End-to-end pipeline for Tamil voice transaction recognition.
    """
    
    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        # Initialize Whisper Model
        # In a real scenario, we would load the fine-tuned weights/adapters here.
        # For this demonstration, we use the base Tamil-capable model.
        print(f"Initializing Whisper model ({model_size})...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        
    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio to Tamil text."""
        segments, info = self.model.transcribe(audio_path, language="ta", beam_size=5)
        text = "".join([segment.text for segment in segments])
        return text.strip()

    def extract_details(self, text: str) -> dict:
        """Extracts customer name, amount, and category from Tamil text."""
        # Simple extraction logic based on keywords
        # Category detection
        category = "General"
        if any(w in text for w in ["கடன்", "loan", "குடுத்த"]):
            category = "Loan"
        elif any(w in text for w in ["பெற்றேன்", "paid", "வாங்கு"]):
            category = "Payment"
        elif any(w in text for w in ["செலவு", "expense"]):
            category = "Expense"

        # Amount extraction using the rule-based parser
        # We look for number patterns in the text
        amount = 0
        # Try to find numeric strings first
        numeric_matches = re.findall(r'\d+', text)
        if numeric_matches:
            amount = int(numeric_matches[0])
        else:
            # Try parsing Tamil words
            amount = parse_tamil_number(text)

        # Name extraction (Naive: assume the first part of the sentence before any amount/category)
        # In production, use a Named Entity Recognition (NER) model.
        name = "Unknown"
        # Dummy logic: if text starts with a name followed by space
        words = text.split()
        if len(words) > 0:
            name = words[0]

        return {
            "customer_name": name,
            "amount_in_rupees": amount,
            "category": category,
            "raw_transcription": text
        }

    def process_audio(self, audio_path: str) -> dict:
        """Processes audio and returns structured transaction data."""
        if not os.path.exists(audio_path):
            return {"error": f"File not found: {audio_path}"}
            
        transcription = self.transcribe(audio_path)
        details = self.extract_details(transcription)
        return details

# Factory function
def get_pipeline():
    return TamilVoicePipeline()

if __name__ == "__main__":
    # Test case demonstration
    pipeline = get_pipeline()
    
    # Mocking audio processing since we don't have a real file here
    print("Testing pipeline logic with text:")
    sample_texts = [
        "குமார் ஐம்பது ரூபாய் கொடுத்தார்",
        "ரவி ஆயிரத்து எழுநூற்று நாற்பது ரூபாய் ரூபா",
        "செல்வா முப்பத்து அஞ்சு ரூபா"
    ]
    
    for text in sample_texts:
        result = pipeline.extract_details(text)
        print(f"Input: {text}")
        print(f"Output: {result}\n")
