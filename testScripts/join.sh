#!/bin/bash

HOST="localhost"
curl -v -X POST \
 -H "Content-Type: application/json" \
 -d '{ "message_version" : "0" , "station_key" : "1of7" , "station_type" : "hmb" , "station_callback_url" : "callback" }' \
 http://$HOST/m/rest-v0/join/1of7
