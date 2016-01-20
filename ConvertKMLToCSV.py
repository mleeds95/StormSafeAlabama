#!/usr/bin/python3

#
# Purpose: Take KML data exported from this Google Map:
# https://www.google.com/maps/d/viewer?mid=zK84o4-5r9bQ.ka4_5ZNJpbzc&hl=en_US
# which catalogs North Alabama storm shelters, and export it in CSV format
# so it can be used for the Storm Safe Alabama app
#

__author__='mwleeds'

from csv import writer
from pykml import parser

INFILE = 'North_Alabama_Tornado_Shelters.kml'
OUTFILE = 'North_Alabama_Tornado_Shelters.csv'

def main():
    kml = parser.parse(INFILE).getroot()
    folder = kml.Document.Folder
    shelters = []
    for placemark in folder.Placemark:
        # grab the human readable name
        name = placemark.name
        # include the address if it's available
        try:
            address = placemark.description
        except AttributeError:
            address = ''
        # cut off the last element (altitude) and transpose them
        coords = str(placemark.Point.coordinates).split(',')[:-1]
        coords = ','.join([coords[1], coords[0]])
        # add this shelter to the list in a CSV ready format
        shelters.append([name, '', '', '', coords, address])
    with open(OUTFILE, 'w') as f:
        csvwriter = writer(f)
        csvwriter.writerow(['Building', 'BARA?', 'Floor', 'Description', 'Geocoding', 'Address'])
        for shelter in shelters:
            csvwriter.writerow(shelter)
    print('Transferred ' + str(len(shelters)) + ' records from ' + INFILE + ' to ' + OUTFILE)

if __name__=='__main__':
    main()
