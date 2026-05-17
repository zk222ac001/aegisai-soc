from app.threat_intel.intel_engine import check_abuseipdb

def enrich_ip(ip_address):
    intel = check_abuseipdb(ip_address)
    return {
        "threat_intel": intel
    }