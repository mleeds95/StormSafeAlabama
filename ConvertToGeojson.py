#!/usr/bin/python3

__author__='mleeds95'

import csv
import geojson

INFILE = 'AL_BARA_DATA.csv'
OUTFILE = 'AL_BARA_DATA.geojson'

def main():
    """Convert csv -> geojson."""
    allFeatures = []
    with open(INFILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            coords = row['Geocoding']
            if len(coords) > 0:
                point = geojson.Point((float(coords.split(',')[1]), float(coords.split(',')[0])))
                row.pop('Geocoding') # so it's not included in properties
                feature = geojson.Feature(geometry=point, properties=row)
                allFeatures.append(feature)
    featureCollection = geojson.FeatureCollection(allFeatures)
    with open(OUTFILE, 'w') as f:
        geojson.dump(featureCollection, f)
    print('Wrote ' + str(len(allFeatures)) + ' places to ' + OUTFILE)

if __name__=='__main__':
    main()
