#!/usr/bin/env python3
## plot.py
##
## Made by Paul Bournat
## Login   <bourna_p@epitech.eu>
##
## Started on  Sat Jul  2 14:10:38 2016 Paul Bournat
## Last update Mon Jul  4 10:19:56 2016 Paul Bournat
##

from __future__ import division, print_function
from json       import loads
from mapbox     import Static
from os         import system
from requests   import codes, get
from sys        import argv, exit, stderr

CITY         = "Toulouse"
EXIT_FAILURE = 1
JCDECAUX_KEY = ""
MAPBOX_TOKEN = ""
MAP_FILE     = "/tmp/veloToulouseMap.png"
URL_DATA     = "https://api.jcdecaux.com/vls/v1/stations?contract=%s&apiKey=%s"\
               %(CITY, JCDECAUX_KEY)

def man(scriptName):
    man  = "SYNOPSIS" + '\n'
    man += '\t' + scriptName + " [-h|--help]" + "\n\n"
    man += "DESCRIPTION" + '\n'
    man += '\t' + "Retrieve a map of every VeloToulouse stations" + '\n'
    man += '\t' + "4 colors are used to indicate their filling rate:" + '\n'
    man += "\t\t" + "Black:" + "\t\t" + "station closed" + '\n'
    man += "\t\t" + "Green:" + "\t\t" + "[66% ; 100%[ empty bike stands" + '\n'
    man += "\t\t" + "Khaki:" + "\t\t" + "[33% ;  66%[ empty bike stands" + '\n'
    man += "\t\t" + "Red:"   + "\t\t" + "[ 0% ;  33%[ empty bike stands" + "\n\n"
    man += '\t' + "Arguments:" + '\n'
    man += "\t\t" + "-h, --help" + '\t' + "display this help and exit" + "\n\n"
    man += '\t' + "Exit status:" + '\n'
    man += "\t\t" + '0' + "\t\t" + "if OK," + '\n'
    man += "\t\t" + '1' + "\t\t" + "if an error occured." + "\n\n"
    man += "AUTHOR" + '\n'
    man += '\t' + "Written by Paul Bournat."    
    return man

def getStationsData():
    data = get(URL_DATA)
    if data.status_code == codes.ok:
        try:
            return loads(data.text)
        except TypeError or ValueError:
            print("Incorrect data formating collected from:\n  %s" %URL_DATA,
                  file=stderr)
            exit(EXIT_FAILURE)
    else:
        print("Error %d occured while collecting data" %data.status_code,
              file=stderr)
        exit(EXIT_FAILURE)

def getPoints(data):
    def getColor(station):
        if station["status"] == "OPEN":
            fillingRate  = 100 * station["available_bike_stands"]
            fillingRate /= station["bike_stands"]
            if fillingRate < 33:
                return "cc0000"
            elif fillingRate < 66:
                return "666600"
            else:
                return "00cc00"
        else:
            return "000"

    points = [] ### Find a way to reduce URL...
#    for station in data:
    for station in [data[0], data[1], data[2], data[128], data[56], data[47]]:
        coord = [station["position"]["lng"], station["position"]["lat"]]
        point = {"type":       "Feature",
                 "properties": {"marker-color": getColor(station)},
                 "geometry":   {"type":         "Point",
                                "coordinates":  coord}}
        points.append(point)
    return points

def getMapCode(points):
    def errorsShallNotPass(response):
        try:
            response.raise_for_status()
        except:
            print("Error %d occured while getting map" %response.status_code,
                  file=stderr)
            exit(EXIT_FAILURE)

    service  = Static(MAPBOX_TOKEN)
    response = service.image("mapbox.streets", features=points)
    errorsShallNotPass(response)
    return response.content

def exportMapToPNG(mapCode):
    with open(MAP_FILE, "wb") as output:
        output.write(mapCode)
        
def main():
    ac = len(argv)
    if ac == 1:
        exportMapToPNG(getMapCode(getPoints(getStationsData())))
        system("exo-open  " + MAP_FILE)
    else:
        if ac == 2 and (argv[1] == "-h" or argv[1] == "--help"):
            print(man(argv[0]))
        else:
            print(man(argv[0]), file=stderr)
            exit(EXIT_FAILURE)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(" KeyboardInterrupt")
