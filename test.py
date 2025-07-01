import requests
import pandas as pd

# Endpoint URL
url = "http://localhost:8000/portfolios/trade-history"

# POST Payload
payload = {
    "user_id": 7,
    "flag": 5,
    "offset": 1,
    "limit": 1000000000000,
    "type": None
}

# Send POST request
response = requests.post(url, json=payload)

# Handle response
if response.status_code == 200:
    response_json = response.json()

    # Extract records list from data
    records = response_json.get("data", {}).get("records", [])
    total = response_json.get("data", {}).get("total", 0)

    # Convert to DataFrame
    df = pd.DataFrame(records)

    # Save to Excel
    df.to_csv("trade_history.csv", index=False)
    print(f"Saved {len(df)} of {total} records to 'trade_history.xlsx'")
else:
    print(f"Request failed: {response.status_code}")
    print(response.text)
