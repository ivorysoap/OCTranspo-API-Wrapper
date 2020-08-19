# OC Transpo API Wrapper :busstop: :oncoming_bus:

[![Build Status](https://travis-ci.com/ivorysoap/PiMonth2019-PiOT.svg?branch=master)](https://travis-ci.com/ivorysoap/PiMonth2019-PiOT)

Instead of messing around with oddly-formed GET requests, why not just call the API from your terminal and get real-time transit data at your fingertips - for any bus stop in Ottawa?

:warning: **Under construction** — Around the time the Confederation Line was opened, OC Transpo updated their API and I'm still working to adapt to the changes.

## Overview

This is a wrapper for the OC Transpo API with some built-in features.

Originally, the goal ofthis project was to make a wrapper that  provides the user more readability and ease of use than interfacing with the API directly.  However, since the API's been updated, I'm working on some new goals, like creating a Bash command to make the API accessible from a terminal.

The `oc.py` script can be used to interface with the OC Transpo API.  You give it a stop number, and it will give you either a summary of the upcoming trips for that stop, or just 
the formatted JSON that the API spits out when you give it a stop number (useful for debugging purposes).

The goal of this project was originally to make the API's output more readable, since at the time of creation, the API output was a complicated mess of XML that a non-technical person might not easily understand. Currently, I'm working on creating a bash command to interface with the API.

## Usage

`$ python3 oc.py (app_id) (api_key) [-json]`

where:

* `(app_id)` is your Application ID
* `(api_key)` is your API key
* `-json` is an optional parameter - if you include it, you'll _just_ get the API's JSON output.  Otherwise, you get the regular bus stop summary.

## Dependencies

* Python 3.7
* OC Transpo API credentials (you'll need to get these yourself)
