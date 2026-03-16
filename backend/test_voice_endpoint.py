import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
DEMO_USERNAME = "demo_shopkeeper"
DEMO_PASSWORD = "demoPassword123"

def test_voice_endpoint():
    print("Logging in...")
    try:
        login_resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": DEMO_USERNAME, "password": DEMO_PASSWORD}
        )
        login_resp.raise_for_status()
        token = login_resp.json()["access_token"]
        print("Login successful.")
    except Exception as e:
        print(f"Login failed: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    files = {"audio": ("test-tone.wav", open("test-tone.wav", "rb"), "audio/wav")}
    data = {"customer_id": "1"}

    print("Sending voice transaction request...")
    try:
        response = requests.post(
            f"{BASE_URL}/voice-transaction",
            headers=headers,
            files=files,
            data=data,
            timeout=120 # Long timeout for processing
        )
        print(f"Status Code: {response.status_code}")
        print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
    except requests.exceptions.Timeout:
        print("Request timed out after 120 seconds!")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_voice_endpoint()


 