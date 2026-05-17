import geoip2.database

reader = geoip2.database.Reader("data/GeoLite2-City.mmdb")

def lookup_ip(ip):
    try:
        response = reader.city(ip)
        return {
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }
    except:
        return {
            "country": "Unknown"
        }