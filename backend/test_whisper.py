import requests
import sys

# Step 1: Login
login_response = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/login",
    json={"username": "demo_shopkeeper", "password": "demoPassword123"}
)

if login_response.status_code != 200:
    # Try register if login fails
    login_response = requests.post(
        "http://127.0.0.1:8000/api/v1/auth/register",
        json={"username": "demo_shopkeeper", "password": "demoPassword123"}
    )
    if login_response.status_code != 200:
        print("Failed to login or register")
        sys.exit(1)

token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Step 2: Create a dummy customer
customer_response = requests.post(
    "http://127.0.0.1:8000/api/v1/customers",
    json={"name": "Test User", "phone": "1234567890"},
    headers=headers
)
customer_id = customer_response.json().get("id", 1) if customer_response.status_code == 200 else 1

# Step 3: Test voice transaction
with open("test-tone.wav", "rb") as f:
    files = {"audio": ("test-tone.wav", f, "audio/wav")}
    data = {"customer_id": customer_id}
    
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/voice-transaction",
        headers=headers,
        data=data,
        files=files
    )

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Response Text:", response.text)
