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
