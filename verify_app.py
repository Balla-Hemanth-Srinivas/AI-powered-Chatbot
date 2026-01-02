import requests
import time
import sys

def verify():
    base_url = "http://127.0.0.1:8000"
    print(f"Checking {base_url}...")
    
    # Retry loop for server startup
    for i in range(10):
        try:
            resp = requests.get(base_url)
            if resp.status_code == 200:
                print("Root endpoint is UP.")
                break
        except requests.exceptions.ConnectionError:
            print(f"Server not ready, retrying ({i+1}/10)...")
            time.sleep(2)
    else:
        print("Server failed to start.")
        sys.exit(1)

    # Test Chat
    print("Testing /chat endpoint...")
    chat_payload = {"message": "Hello, how are you?"}
    try:
        resp = requests.post(f"{base_url}/chat", json=chat_payload)
        if resp.status_code == 200:
            print("Chat response:", resp.json())
        else:
            print("Chat endpoint failed:", resp.text)
            sys.exit(1)
    except Exception as e:
        print(f"Chat request failed: {e}")
        sys.exit(1)

    # Test History
    print("Testing /history endpoint...")
    try:
        resp = requests.get(f"{base_url}/history")
        if resp.status_code == 200:
            logs = resp.json()
            print(f"History retrieved. Count: {len(logs)}")
        else:
            print("History endpoint failed:", resp.text)
            sys.exit(1)
    except Exception as e:
        print(f"History request failed: {e}")
        sys.exit(1)

    print("VERIFICATION SUCCESSFUL: All systems nominal.")

if __name__ == "__main__":
    verify()
