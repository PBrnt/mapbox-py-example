#!/usr/bin/env python3
## distance.py
##
## Made by Paul Bournat
## Login   <bourna_p@epitech.eu>
##
## Started on  Sat Jul  2 14:10:38 2016 Paul Bournat
## Last update Mon Jul  4 10:19:37 2016 Paul Bournat
##

from json       import loads
from mapbox     import Directions
from requests   import codes, get
from sys        import argv, exit, stderr

CITY         = "Toulouse"
EXIT_FAILURE = 1
JCDECAUX_KEY = ""
MAPBOX_TOKEN = ""
PROFILE      = "mapbox.cycling"
URL_DATA     = "https://api.jcdecaux.com/vls/v1/stations?contract=%s&apiKey=%s"\
               %(CITY, JCDECAUX_KEY)

def man(scriptName):
    man  = "SYNOPSIS\n"
    man += '\t' + scriptName + " station#1 station#2" + '\n'
    man += '\t' + scriptName + " -h" + "\n\n"
    man += "DESCRIPTION" + '\n'
    man += '\t' + "Arguments:" + '\n'
    man += "\t\t" + "station#n\tVelôToulouse station number" + '\n'
    man += "\t\t" + "-h, --help" + '\t' + "display this help and exit" + "\n\n"
    man += '\t' + "Exit status:" + '\n'
    man += "\t\t" + '0' + "\t\t" + "if OK," + '\n'
    man += "\t\t" + '1' + "\t\t" + "if an error occured." + "\n\n"
    man += "AUTHOR" + '\n'
    man += '\t' + "Written by Paul Bournat."
    return man

def getUInt(s):
    try:
        n = int(s)
        if n < 1:
            print("Arguments must be strictly positive integers", file=stderr)
            exit(EXIT_FAILURE)
        return n
    except ValueError:
        print("Arguments must be strictly positive integers", file=stderr)
        exit(EXIT_FAILURE)

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

def computeDistance(stationN1, stationN2):
    def getDirectionObjects(stationN1, stationN2):
        data = getStationsData()
        dest = {"type":     "Feature",
                "geometry": {"type":        "Point",
                             "coordinates": [None, None]}}
        orig = {"type":     "Feature",
                "geometry": {"type":        "Point",
                             "coordinates": [None, None]}}
        for station in data:
            if station["number"] == stationN1:
                orig["geometry"]["coordinates"][1] = station["position"]["lng"]
                orig["geometry"]["coordinates"][0] = station["position"]["lat"]
            elif station["number"] == stationN2:
                dest["geometry"]["coordinates"][1] = station["position"]["lng"]
                dest["geometry"]["coordinates"][0] = station["position"]["lat"]
            if orig["geometry"]["coordinates"][0] != None and \
               dest["geometry"]["coordinates"][0] != None:
                break
        return [orig, dest]

    service = Directions(MAPBOX_TOKEN)
    response = service.directions(getDirectionObjects(stationN1, stationN2),
                                  PROFILE)
    try:
        response.raise_for_status()
    except:
        print("Error %d occured while retreiving answer from server"
              %response.status_code, file=stderr)
        exit(EXIT_FAILURE)
    try:
        response = loads(response.text)
    except TypeError or ValueError:
        print("Incorrect data formating collected from:\n  %s" %URL_DATA,
              file=stderr)
        exit(EXIT_FAILURE)
    return response["routes"][0]["distance"]

def main():
    ac = len(argv)
    if ac == 3:
        result = computeDistance(getUInt(argv[1]), getUInt(argv[2]))
        print(str(result) + 'm')
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
