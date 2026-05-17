ioc_cache = {}
def get_cached_ioc(ip):
    return ioc_cache.get(ip)

def set_cached_ioc(ip, data):
    ioc_cache[ip] = data