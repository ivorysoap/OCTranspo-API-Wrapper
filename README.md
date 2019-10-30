# OC Transpo API Wrapper :busstop: :oncoming_bus:


The `oc.py` script can be used to interface with the OC Transpo API.  You give it a stop number, and it will give you either a summary of the upcoming trips for that stop, or just 
the formatted JSON that the API spits out when you give it a stop number (useful for debugging purposes).

## Usage

`$ python3 oc.py (app_id) (api_key) [-json]`

where:

* `(app_id)` is your Application ID
* `(api_key)` is your API key
* `-json` is an optional parameter - if you include it, you'll _just_ get the API's JSON output.  Otherwise, you get the regular bus stop summary.

## Dependencies

* Python 3.7
* OC Transpo API credentials (you'll need to get these yourself)
