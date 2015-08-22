#!/usr/bin/python3

__author__='mleeds95'

from urllib.request import urlopen
from urllib.parse import urlencode
from time import sleep

GOOGLE_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?'
OSM_BASE_URL = 'http://open.mapquestapi.com/nominatim/v1/search.php?'

def geocode_Google(address, bounds, api_key):
    """Send a street address to Google to find its lat/lng coordinates.
    Parameters:
        address -- the street address to be geocoded
        bounds -- a rectangle that biases results in the format "lat,lng|lat,lng"
        api_key -- your API Key from the Google API Console
    Returns:
        on success -- a tuple of the coordinates and the nicely formatted address
        on failure -- a string describing the reason for the failure
    See https://developers.google.com/maps/documentation/geocoding/
    """
    params = {'address': address, 
              'bounds': bounds,
              'key': api_key}
    url = GOOGLE_BASE_URL + urlencode(params, safe='/,|')
    rawreply = urlopen(url).read()
    reply = json.loads(rawreply.decode('utf-8'))
    sleep(0.1) # stay under usage limit
    # assume the first result is correct
    if reply['status'] == 'OK':
        return (reply['results'][0]['geometry']['location'], reply['results'][0]['formatted_address'])
    else:
        return reply['status']

# uses the OpenStreetMap.org "Nominatim" geocoding service via MapQuest
# return values should match the format that the Google Maps function returns
def geocode_OSM(address, bounds, email_address):
    """Send a street address to OpenStreetMap.org ("Nominatim") to find it's lat/lng coordinates.
    Parameters:
        address -- the street address to be geocoded
        bounds -- a rectangle that biases results in the format "lat,lng|lat,lng"
        email_address -- your email address
    Returns:
        on success -- a tuple of the coordinates and the nicely formatted address
        on failure -- a string describing the reason for the failure
    See http://wiki.openstreetmap.org/wiki/Nominatim
    """
    params = {'q': address,
              'format': 'json',
              'email': email_address,
              'viewbox': bounds,
              'limit': '1',
              'addressdetails': '0'}
    url = OSM_BASE_URL + urlencode(params)
    rawreply = urlopen(url).read()
    reply = json.loads(rawreply.decode('utf-8'))
    sleep(1) # rate limit ourselves
    try:
        coords = {'lat': reply[0]['lat'], 'lng': reply[0]['lon']}
        niceAddress = reply[0]['display_name']
        result = (coords, niceAddress)
    except (IndexError, KeyError):
        result = 'NO_RESULTS_FOUND'
    return result

__all__ = ['geocode_Google', 'geocode_OSM']

