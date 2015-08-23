#!/usr/bin/python3

__author__='mleeds95'

import csv
from GeocodeLocations import geocode_Google

FILENAME = 'UA_BARA_2014-08-18.csv'
UA_BOUNDS = '33.180437,-87.611358|33.246932,-87.498319'
API_KEY = 'AIzaSyCTB-zTo3c8hRTm9jn4GvZPvT1QynZmwrA'

def main():
    """Read locations from the specified CSV file and geocode them."""
    cache = {} # store results so we don't ask for the same info multiple times
    numSuccess, numFailure = 0, 0
    updatedRows = []
    with open(FILENAME) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Building'] not in cache:
                result = geocode_Google(row['Building'], UA_BOUNDS, API_KEY)
                if type(result) is str: # failure
                    print('ERROR: ' + row['Building'] + ' resulted in ' + result)
                    cache[row['Building']] = ('', '')
                    row['Geocoding'] = ''
                    row['FormattedAddress'] = ''
                    numFailure += 1
                else: # success
                    string_coords = str(round(result[0]['lat'], 6)) + ', ' + \
                                    str(round(result[0]['lng'], 6))
                    cache[row['Building']] = (string_coords, result[1])
                    row['Geocoding'] = string_coords
                    row['FormattedAddress'] = result[1]
                    numSuccess += 1
            else: # copy from the cache
                row['Geocoding'] = cache[row['Building']][0]
                row['FormattedAddress'] = cache[row['Building']][1]
            updatedRows.append(row.copy())
        f.seek(0)
        header = f.readline().strip()
    print('Finished geocoding. ' + str(numSuccess) + ' successes, ' + 
                                   str(numFailure) + ' failures.')
    header += ',FormattedAddress'
    with open(FILENAME, 'w') as f:
        writer = csv.DictWriter(f, header.split(','))
        writer.writeheader()
        for row in updatedRows:
            writer.writerow(row)

if __name__=='__main__':
    main()
