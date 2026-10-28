import time

_cache = {}
TTL = 3600  # 1 час

def get(key):
    item = _cache.get(key)
    if not item:
        return None
    value, expires = item
    if time.time() > expires:
        _cache.pop(key, None)
        return None
    return value

def set(key, value):
    _cache[key] = (value, time.time() + TTL)
