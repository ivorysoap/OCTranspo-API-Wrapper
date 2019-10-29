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

def printResponseHeader(jsonData):
    print("\nUpcoming trips for stop #" + str(jsonData['GetRouteSummaryForStopResult']["StopNo"]) + " (" + str(
        jsonData['GetRouteSummaryForStopResult']["StopDescription"]) + "): \n\n")

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

    printResponseHeader(jsonData)

    numRoutes = getNumRoutes(trips)

    if (numRoutes == 1):

        numTrips = len(jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]["Trips"]["Trip"])

        print("\tRoute " + str(jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]["RouteNo"]) + " " + str(
            jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]["RouteHeading"]) + ":\n\n")

        for i in range(0, numTrips):
            print("\t\tto " + str(jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]["Trips"]["Trip"][i][
                                      "TripDestination"]) + " - at " + str(
                jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]["Trips"]["Trip"][i]["TripStartTime"]))
            print("\n")

        if (numTrips == 0):
            print("\t\tNothing right now.\n\n")

    elif (numRoutes > 1):

        # print("Multiple routes\n")

        for i in range(0, numRoutes):

            if 'Trips' in jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"][i]:
                numTrips = len(jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"][i]["Trips"])
            else:
                numTrips = 0

            print(
                "\tRoute " + str(jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"][i]["RouteNo"]) + " " + str(
                    jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"][i]["RouteHeading"]) + ":\n\n")

            for j in range(0, numTrips):
                print("\t\tto " + str(jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"][i]["Trips"][j][
                                          "TripDestination"]) + " - at " + str(
                    jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"][i]["Trips"][j]["TripStartTime"]))
                print("\n")

            if (numTrips == 0):
                print("\t\tNothing right now.\n\n")


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
