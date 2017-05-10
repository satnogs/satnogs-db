from rest_framework.authtoken.models import Token

from django.core.cache import cache


UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWX'
LOWER = 'abcdefghijklmnopqrstuvwx'


def gridsquare(lat, lng):
    if not (-180 <= lng < 180):
        return False
    if not (-90 <= lat < 90):
        return False

    adj_lat = lat + 90.0
    adj_lon = lng + 180.0

    grid_lat_sq = UPPER[int(adj_lat / 10)]
    grid_lon_sq = UPPER[int(adj_lon / 20)]

    grid_lat_field = str(int(adj_lat % 10))
    grid_lon_field = str(int((adj_lon / 2) % 10))

    adj_lat_remainder = (adj_lat - int(adj_lat)) * 60
    adj_lon_remainder = ((adj_lon) - int(adj_lon / 2) * 2) * 60

    grid_lat_subsq = LOWER[int(adj_lat_remainder / 2.5)]
    grid_lon_subsq = LOWER[int(adj_lon_remainder / 5)]

    qth = '{}'.format(grid_lon_sq + grid_lat_sq + grid_lon_field +
                      grid_lat_field + grid_lon_subsq + grid_lat_subsq)

    return qth


def get_apikey(user):
    try:
        token = Token.objects.get(user=user)
    except:
        token = Token.objects.create(user=user)
    return token


def cache_get_key(*args, **kwargs):
    import hashlib
    serialise = []
    for arg in args:
        serialise.append(str(arg))
    for key, arg in kwargs.items():
        serialise.append(str(key))
    serialise.append(str(arg))
    key = hashlib.md5("".join(serialise)).hexdigest()
    return key


def cache_for(time):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            key = cache_get_key(fn.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result:
                result = fn(*args, **kwargs)
                cache.set(key, result, time)
            return result
        return wrapper
    return decorator
