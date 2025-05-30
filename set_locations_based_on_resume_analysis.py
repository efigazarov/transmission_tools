import re
import requests

# === CONFIGURATION ===
RPC_URL = "http://localhost:9091/transmission/rpc"
RPC_AUTH = ('transmission', 'transmission')  # Change to your RPC credentials if needed
INPUT_FILE = "results.txt"  # Your text file with parsed resume entries

def get_session_id():
    """Fetch Transmission RPC session ID (for CSRF protection)."""
    response = requests.post(RPC_URL)
    return response.headers["X-Transmission-Session-Id"]

def set_location(torrent_hash, location, session_id):
    """Send a torrent-set-location RPC command for a given hash."""
    payload = {
        "method": "torrent-set-location",
        "arguments": {
            "ids": [torrent_hash],
            "location": location,
            "move": False
        }
    }
    headers = {"X-Transmission-Session-Id": session_id}
    response = requests.post(RPC_URL, json=payload, headers=headers, auth=RPC_AUTH)

    # Retry if session ID expired
    if response.status_code == 409:
        new_session_id = response.headers["X-Transmission-Session-Id"]
        return set_location(torrent_hash, location, new_session_id)
    
    return response.json()

def main():
    session_id = get_session_id()
    current_hash = None
    current_destination = None

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            # Detect start of a resume block
            hash_match = re.match(r"=== ([a-f0-9]{40})\.resume ===", line.strip())
            if hash_match:
                current_hash = hash_match.group(1)
                current_destination = None  # Reset destination
                continue

            # Detect destination line
            if line.startswith("destination: ") and current_hash:
                current_destination = line.strip().split("destination: ", 1)[1]
                if current_destination:
                    result = set_location(current_hash, current_destination, session_id)
                    print(f"{current_hash[:8]}... → {current_destination[:60]} → {result.get('result')}")
                current_hash = None  # Reset for next block

if __name__ == "__main__":
    main()

