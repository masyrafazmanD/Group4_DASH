import requests
import json

def scrap_data(base: str = "USD", target: str = "MYR") -> dict:
    url = "https://api.frankfurter.dev/v1/latest?from=USD&to=MYR,EUR,GBP"

    try:
        response = requests.get(url, timeout=10, verify=False)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")

        raw = response.json()

        rate = raw["rates"][target]

        body = {
            "base": base,
            "target": target,
            "rate": rate
        }

        return body

    except Exception as e:
        print("Error fetching API:", e)
        return None


if __name__ == "__main__":
    data = scrap_data()
    print(json.dumps(data, indent=2))