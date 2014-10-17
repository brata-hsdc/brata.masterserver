#!/bin/bash
# ------------------------------------------------------------------------------
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ------------------------------------------------------------------------------

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
