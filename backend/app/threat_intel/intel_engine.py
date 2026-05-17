import os
import requests

# ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
ABUSEIPDB_API_KEY = "8efd5e1fb557b9ee24c6c5e2289fe33cfdc8e7295c4355a651f51749ab84427366f2515a093192ed"
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

def check_abuseipdb(ip_address: str):    
    # Optimized AbuseIPDB lookup for IDS pipeline  
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": 90,
        "verbose": True
    }
    try:
        response = requests.get(
            ABUSEIPDB_URL,
            headers=headers,
            params=params,
            timeout=4
        )
        # -----------------------------
        # Validate HTTP status
        # -----------------------------
        if response.status_code != 200:
            print(f"[AbuseIPDB Warning] HTTP {response.status_code}")
            return _default_result()

        data = response.json()
        # -----------------------------
        # Validate API structure
        # -----------------------------
        abuse_data = data.get("data")
        if not abuse_data:
            print("[AbuseIPDB Warning] Invalid response format:", data)
            return _default_result()

        abuse_score = abuse_data.get("abuseConfidenceScore", 0)
        return {
            "malicious": abuse_score > 50,
            "abuse_score": abuse_score,
            "country": abuse_data.get("countryCode", "Unknown"),
            "isp": abuse_data.get("isp", "Unknown")
        }

    except requests.exceptions.Timeout:
        print("[AbuseIPDB Error] Timeout")
        return _default_result()

    except requests.exceptions.RequestException as e:
        print(f"[AbuseIPDB Error] Network issue: {e}")
        return _default_result()

    except Exception as e:
        print(f"[AbuseIPDB Error] Unexpected: {e}")
        return _default_result()

# -----------------------------
# Safe fallback (important)
# -----------------------------
def _default_result():
    return {
        "malicious": False,
        "abuse_score": 0,
        "country": "Unknown",
        "isp": "Unknown"
    }