# OC Transpo API Wrapper :busstop: :oncoming_bus:

[![Build Status](https://travis-ci.com/ivorysoap/PiMonth2019-PiOT.svg?branch=master)](https://travis-ci.com/ivorysoap/PiMonth2019-PiOT)

Instead of messing around with oddly-formed GET requests, why not just call the API from your terminal and get real-time transit data at your fingertips - for any bus stop in Ottawa?

## Overview

This is a wrapper for the OC Transpo API that provides the user more readability and ease of use than interfacing with the API directly.  

The `oc.py` script can be used to interface with the OC Transpo API.  You give it a stop number, and it will give you either a summary of the upcoming trips for that stop, or just 
the formatted JSON that the API spits out when you give it a stop number (useful for debugging purposes).

*Under construction*

## Usage

`$ python3 oc.py (app_id) (api_key) [-json]`

where:

* `(app_id)` is your Application ID
* `(api_key)` is your API key
* `-json` is an optional parameter - if you include it, you'll _just_ get the API's JSON output.  Otherwise, you get the regular bus stop summary.

## Dependencies

* Python 3.7
* OC Transpo API credentials (you'll need to get these yourself)
