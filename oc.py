import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

url = "https://api.octranspo1.com/v1.2/GetNextTripsForStopAllRoutes" #URL to query

#appId = input("Please enter your app ID.")
appId = "8e242649"

#apiKey = input("Please enter your OC Transpo API key.")
apiKey = "d6cea23598c577d86e4eb922c500d481"

stopNumber = input("Please type in the stop number.")

vals = {'appID'  : appId,
        'apiKey' : apiKey,
        'stopNo' : stopNumber} #Parameters to pass to URL

data = urllib.parse.urlencode(vals) #Some parsing and encoding magic

data = data.encode('ascii')

req= urllib.request.Request(url, data)

with urllib.request.urlopen(req) as response:
   print(response.read())



def formatBusData(xmldata):

    #XML-parsing magic here
    return


# Message Ivor for app ID and API key