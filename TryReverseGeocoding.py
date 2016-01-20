#!/usr/bin/python3

__author__='mwleeds'

import csv
from GeocodeLocations import reverse_geocode_Google

INFILE = 'North_Alabama_Tornado_Shelters.csv'
OUTFILE = 'North_Alabama_Tornado_Shelters_geo.csv'
API_KEY = 'AIzaSyCTB-zTo3c8hRTm9jn4GvZPvT1QynZmwrA'

def main():
    """Read locations from the specified CSV file and geocode them."""
    numSuccess, numFailure = 0, 0
    updatedRows = []
    print('Reading data from ' + INFILE)
    with open(INFILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = reverse_geocode_Google(row['Geocoding'], API_KEY)
            if not result[0]: # failure
                print('ERROR: ' + row['Geocoding'] + ' resulted in ' + result[1])
                numFailure += 1
            else: # success
                row['GeocodedAddress'] = result[1]
                numSuccess += 1
            updatedRows.append(row.copy())
    print('Finished geocoding. ' + str(len(updatedRows)) + ' rows, ' +
                                   str(numSuccess) + ' successes, ' +
                                   str(numFailure) + ' failures.')
    with open(OUTFILE, 'w') as f:
        header = ['Building', 'BARA?', 'Floor', 'Description', 'Geocoding', 'Address', 'GeocodedAddress']
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        for row in updatedRows:
            writer.writerow(row)
    print('Data written to ' + OUTFILE)

if __name__=='__main__':
    main()
