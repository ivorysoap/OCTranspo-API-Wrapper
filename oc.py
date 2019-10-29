import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import sys


def getNumRoutes(trips):
    # Test: is "Route" a list or a dict?  If dict, stop serviced by one route.  If list, stop serviced by multiple
    # routes.
    if isinstance(trips, list):
        return len(trips)
    else:
        return 1


def printUsage():
    print(
        "\nUsage: python oc.py (app_id) (api_key) [-json]\n\n where -json will cause the program to spit out the raw "
        "JSON data from the API.  Omitting it gives you the regular interface.")


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

            if 'Trips' in trips[i]:
                numTrips = len(trips[i]["Trips"])
            else:
                numTrips = 0

            print(
                "\tRoute " + str(trips[i]["RouteNo"]) + " " + str(
                    trips[i]["RouteHeading"]) + ":\n\n")

            for j in range(0, numTrips):
                print("\t\tto " + str(trips[i]["Trips"][j][
                                          "TripDestination"]) + " - at " + str(
                    trips[i]["Trips"][j]["TripStartTime"]))
                print("\n")

            if numTrips == 0:
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


if (len(sys.argv) != 3) and len(sys.argv) != 4:
    printUsage()
    sys.exit(-1)

url = "https://api.octranspo1.com/v1.2/GetNextTripsForStopAllRoutes"  # URL to query

# appId = input("Please enter your app ID.")
appId = sys.argv[1]

# apiKey = input("Please enter your OC Transpo API key.")
apiKey = sys.argv[2]

while True:

    stopNumber = input("Please type in the stop number.")

    vals = {'appID': appId,
            'apiKey': apiKey,
            'stopNo': stopNumber,
            'format': 'json'}  # Parameters to pass to URL

    data = urllib.parse.urlencode(vals)  # Some parsing and encoding magic

    data = data.encode('ascii')

    req = urllib.request.Request(url, data)

    with urllib.request.urlopen(req) as response:
        rawData = json.loads(response.read())

    cleanData = formatData(rawData)

    if (len(sys.argv) == 3):
        tripsToString(rawData)
    elif (len(sys.argv) == 4 and sys.argv[3] == '-json'):
        print(formatData(rawData))

# Message Ivor for app ID and API key
