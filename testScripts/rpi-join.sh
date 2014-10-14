#!/bin/bash


function usage() 
{
  echo rpi-join.sh KEY TYP URL
  exit 1
}
KEY=$1
TYP=$2
URL=$3
if [ -z "$KEY" -o  -z "$TYP" -o -z "$URL" ] ; then 
   usage;
fi

HOST="localhost"
curl -v -X POST \
 -H "Content-Type: application/json" \
 -d "{ \"message_version\" : \"0\" , \"station_key\" : \"$KEY\" , \"station_type\" : \"$TYP\" , \"station_callback_url\" : \"$URL\" }" \
 http://$HOST/m/rpi-v00/join/$KEY
