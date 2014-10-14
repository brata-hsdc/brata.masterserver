#!/bin/bash


TEAMID=$1
STATIONID=$2
if [ -z "$TEAMID" -o  -z "$STATIONID" ] ; then 
   usage;
fi
# -d '{ "message_version" : "0" , "station_key" : "1of7" , "station_type" : "hmb" , "station_callback_url" : "callback" }' \

HOST="localhost"
curl -v -X GET \
 -H "Content-Type: application/json" \
 http://$HOST/m/brata-v00/start_challenge/$TEAMID/$STATIONID
