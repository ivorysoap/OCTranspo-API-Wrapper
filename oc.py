import urllib.request
import urllib.parse
import argparse
import xml.etree.ElementTree as ET
import json


def main():
    ap, args = parseArgs()

    url = "https://api.octranspo1.com/v1.2/GetNextTripsForStopAllRoutes"  # URL to query

    while True:

        stopNumber = input("Please type in the stop number.")

        vals = {'appID': args.app_id,
                'apiKey': args.api_key,
                'stopNo': stopNumber,
                'format': 'json'}  # Parameters to pass to URL

        data = urllib.parse.urlencode(vals)  # Some parsing and encoding magic

        data = data.encode('ascii')

        req = urllib.request.Request(url, data)

        with urllib.request.urlopen(req) as response:
            rawData = json.loads(response.read())

        cleanData = formatData(rawData)

        if not args.print_json:
            tripsToString(rawData)
        else:
            print(formatData(rawData))


def parseArgs():
    """Parses and generates command-line arguments."""
    ap = argparse.ArgumentParser()
    ap.add_argument("app_id", help="OC Transpo App ID")
    ap.add_argument("api_key", help="OC Transpo API Key")
    ap.add_argument("-json", "--print-json", action='store_true',
                    help="Causes the program to spit out the raw JSON data from the OC Transpo API")
    args = ap.parse_args()
    return ap, args


def getNumRoutes(trips):
    # Test: is "Route" a list or a dict?  If dict, stop serviced by one route.  If list, stop serviced by multiple
    # routes.
    if isinstance(trips, list):
        return len(trips)
    else:
        return 1


def printHeader(jsonData):
    print("\nUpcoming trips for stop #" + str(jsonData['GetRouteSummaryForStopResult']["StopNo"]) + " (" + str(
        jsonData['GetRouteSummaryForStopResult']["StopDescription"]) + "): \n\n")


def printRouteHeader(trips):
    print("\tRoute " + str(trips["RouteNo"]) + " " + str(
        trips["RouteHeading"]) + ":\n\n")


def printTrips(trips, numRoutes):
    if numRoutes == 1:

        printRouteHeader(trips)

        numTrips = len(trips["Trips"]["Trip"])

        for i in range(0, numTrips):
            print("\t\tto " + str(trips["Trips"]["Trip"][i]["TripDestination"]) + " - at " + str(
                trips["Trips"]["Trip"][i]["TripStartTime"]))
            print("\n")

        if numTrips == 0:
            print("\t\tNothing right now.\n\n")

    elif numRoutes > 1:

        # print("Multiple routes\n")

        for i in range(0, numRoutes):

            if 'Trips' in trips[i] and isinstance(trips[i]["Trips"], list):
                numTrips = len(trips[i]["Trips"])
            elif 'Trips' in trips[i] and isinstance(trips[i]["Trips"], dict):
                numTrips = 1
            else:
                numTrips = 0

            print("\tRoute " + str(trips[i]["RouteNo"]) + " " + str(trips[i]["RouteHeading"]) + ":\n\n")

            if numTrips > 1:
                for j in range(0, numTrips):
                    print("\t\tto " + str(trips[i]["Trips"][j]["TripDestination"]) + " - at " + str(
                        trips[i]["Trips"][j]["TripStartTime"]))
                    print("\n")
            elif numTrips == 1:
                print("\t\tto " + str(trips[i]["Trips"]["TripDestination"]) + " - at " + str(
                    trips[i]["Trips"]["TripStartTime"]))
                print("\n")
            elif numTrips == 0:
                print("\t\tNothing right now.\n\n")


def formatData(jsonData):
    """
    (dict)->(dict)
    Formats the incoming JSON object into a nicer printable one.
    """

    return json.dumps(jsonData, indent=4)


def tripsToString(jsonData):
    """
    (dict)->none
    Takes JSON object and from it, prints upcoming trips.
    """

    trips = jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]

    numRoutes = getNumRoutes(trips)

    printHeader(jsonData)

    printTrips(trips, numRoutes)


if __name__ == "__main__":
    main()

# Message Ivor for app ID and API key
