#!/bin/bash

function usage() 
{
  echo brata-atWaypoint.sh LAT LNG
  exit 1
}
LAT=$1
LNG=$2
if [ -z "$LAT" -o  -z "$LNG" ] ; then 
   usage;
fi

HOST="localhost"
curl -v -X GET \
 -H "Accept: application/json" \
 http://$HOST/m/brata-v00/atWaypoint/$LAT/$LNG
