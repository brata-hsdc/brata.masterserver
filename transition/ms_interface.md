# Master Server Web Service Interface
(I'm reverse engineering the HTTP requests in the `testScripts` folder.  This is mostly a warm-up exercise to get acquainted with the MS.)

(There is probably a standard notation for this, but I'm clueless.)

I'm attempting to group them by the sender/purpose:  BRATA, RPi, Admin.

`ms` is the hostname or IP address of the Master Server.

---

## BRATA Messages

### Start Challenge
```
         URL:  http://ms/m/brata-v00/start_challenge/TEAMID/STATIONID
      Method:  GET
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|--------
TEAMID    |        |         |
STATIONID |        |         |

===

### At Waypoint
```
         URL:  http://ms/m/brata-v00/atWaypoint/LAT/LON
      Method:  GET
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|--------
LAT       |        |         | latitude in decimal degrees
LON       |        |         | longitude in decimal degrees

===

### BRATA Submit
Not sure what this one is.
```
         URL:  http://ms/m/rest-v00/submit/1of7
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
*None?*

#### JSON Data
```json
{
   "message_version"      : "0" ,
   "station_key"          : "1of7" ,
   "station_type"         : "hmb" ,
   "station_callback_url" : "callback"
}
```

---

## RPi Messages

### RPi Join
```
         URL:  http://ms/m/rpi/join/ID
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
ID        |        |         | ID of the Raspberry Pi station
TYP       |        |         |
URL       |        |         |

#### JSON Data
```json
{
   "message_version" : "0" ,
   "station_type"    : "$TYP" ,
   "station_url"     : "$URL"
}
```

===

### RPi Submit
```
         URL:  http://ms/m/rest-v00/submit/1of7
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
*None?*

#### JSON Data
```json
{
   "message_version"      : "0" ,
   "station_key"          : "1of7" ,
   "station_type"         : "hmb" ,
   "station_callback_url" : "callback"
}
```

---

## Admin Messages


### Setup
(From `workspace/m/setup.php`)
```
         URL:  http://ms/setup.php
      Method:  GET
Content type:  ??
Return value:  ??
```

#### Parameters
*None?*

===

### Save Setup Configuration
(From `workspace/m/setup.php`)
```
         URL:  http://ms/setup.php?write=1
      Method:  POST
Content type:  multipart/form-encoded (??)
Return value:  ??
```

#### Parameters
*None?*

#### Form Data
These values come from form field widgets in a web `<form>`.

Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
webdomain |        |         | 
webfolder |        |         | 
dbhost    |        |         | 
dbname    |        |         | 
dbuser    |        |         | 
dbpass    |        |         | 
leaderBoardRefersh (sic) | | | 
loglevel  |        |         | 
logfile   |        |         | 
sendmail  |        |         | 
debug     |        |         | 
student   |        |         | 
