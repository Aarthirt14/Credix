# API Integration Guide

## Voice Transaction Endpoint

### POST /api/v1/voice-transaction

Process a voice recording and extract transaction details.

**Request:**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.webm');
formData.append('customer_id', customerId); // optional

const response = await fetch('http://127.0.0.1:8000/api/v1/voice-transaction', {
  method: 'POST',
  body: formData,
});

const preview = await response.json();
```

**Response Example:**
```json
{
  "transcription": "ravi irubathu roobai",
  "normalized_text": "ராவி இருபது ரூபாய்",
  "parsed": {
    "name": "ராவி",
    "amount": 20,
    "item": null,
    "qty": 1,
    "type": "expense",
    "raw_text": "ராவி இருபது ரூபாய்"
  },
  "matched_customer_id": 1,
  "matched_customer_name": "Ravi",
  "is_valid": true,
  "items": [
    {
      "name": "Credit Entry",
      "qty": 1,
      "price": 20
    }
  ],
  "calculated_total": 20,
  "parsing_warnings": []
}
```

### POST /api/v1/transactions

Create a transaction from voice preview data.

**Request:**
```javascript
const response = await fetch('http://127.0.0.1:8000/api/v1/transactions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    customer_id: customerId,
    amount: 20,
    category: "expense",
    voice_data: {
      name: "Ravi",
      amount: 20,
      type: "expense",
      raw_text: "ravi irubathu roobai"
    }
  }),
});
```

## Error Handling

- **422 Unprocessable Entity**: Invalid voice data or audio
- **404 Not Found**: Customer not found
- **429 Too Many Requests**: Rate limit exceeded (10/minute)
- **500 Server Error**: Processing pipeline failure

## Example Frontend Integration

```typescript
async function recordAndProcess() {
  // Record audio
  const mediaRecorder = new MediaRecorder(stream);
  const chunks: Blob[] = [];
  
  mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
  mediaRecorder.start();
  
  // Stop after 10 seconds
  setTimeout(() => {
    mediaRecorder.stop();
    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: 'audio/webm' });
      
      // Send to backend
      const formData = new FormData();
      formData.append('audio', blob);
      
      const res = await fetch('/api/v1/voice-transaction', {
        method: 'POST',
        body: formData,
      });
      
      const preview = await res.json();
      
      // Show preview to user - amount should be ₹20
      console.log(preview.parsed.amount); // 20
      console.log(preview.matched_customer_name); // "Ravi"
      
      // User confirms and submits
      if (confirm('Create transaction?')) {
        await createTransaction(preview);
      }
    };
  }, 10000);
}
```

## Rate Limiting

- Voice transactions: 10 per minute per user
- Status code 429 returned when exceeded
- Headers included: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
