import urllib.request
import urllib.parse
import argparse
import json


def main():
    ap, args = parseArgs()
    url = "https://api.octranspo1.com/v1.3/GetNextTripsForStopAllRoutes"  # URL to query
    while True:

        stopNumber = input("Please type in the stop number, or \"Exit\" to exit.")
        if stopNumber.lower() == "exit":
            exit(0)

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
            if trips["Trips"]["Trip"][i]["LastTripOfSchedule"]:
                print("\t\t(Last Trip)")
            print("\n")

        if numTrips == 0:
            print("\t\tNothing right now.\n\n")

    elif numRoutes > 1:

        numTrips = []

        for i in range(0, numRoutes):

            if 'Trips' in trips[i] and isinstance(trips[i]["Trips"], list):
                numTrips.append(len(trips[i]["Trips"]))
            elif 'Trips' in trips[i] and isinstance(trips[i]["Trips"], dict):
                numTrips.append(1)
            else:
                numTrips.append(0)

            print("\n\n\tRoute " + str(trips[i]["RouteNo"]) + " " + str(trips[i]["RouteHeading"]) + ":\n")

            if numTrips[i] > 1:
                for j in range(0, numTrips[i]):
                    print("\t\tto " + str(trips[i]["Trips"][j]["TripDestination"]) + " - at " + str(
                        trips[i]["Trips"][j]["TripStartTime"]))
                    if trips[i]["Trips"][j]["LastTripOfSchedule"]:
                        print("\t\t(Last Trip)")
                print("\n")
            elif numTrips[i] == 1:
                print("\t\tto " + str(trips[i]["Trips"]["TripDestination"]) + " - at " + str(
                    trips[i]["Trips"]["TripStartTime"]))
                if trips[i]["Trips"]["LastTripOfSchedule"]:
                    print("\t\t(Last Trip)")
            elif numTrips[i] == 0:
                print("\t\tNothing right now.\n")


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

    if jsonData is not None:  # API can sometimes return a None object if given nonsensical input

        if "Routes" in jsonData['GetRouteSummaryForStopResult']:
            # API only includes a Routes object inside the GetRouteSummaryForStopResult object if stop number is valid

            trips = jsonData['GetRouteSummaryForStopResult']["Routes"]["Route"]

            numRoutes = getNumRoutes(trips)

            printHeader(jsonData)

            printTrips(trips, numRoutes)

        elif "Error" in jsonData['GetRouteSummaryForStopResult']:

            errorNo = int(jsonData['GetRouteSummaryForStopResult']["Error"])
            print("\nAPI returned error " + str(errorNo) + ".")

            if errorNo == 10:
                print("Likely cause: stop number not found.\n")

    else:
        print("Unspecified error.")


if __name__ == "__main__":
    main()

# Message Ivor for app ID and API key
