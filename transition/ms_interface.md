# Master Server Web Service Interface
(I'm reverse engineering the HTTP requests in the `testScripts` folder.  This is mostly a warm-up exercise to get acquainted with the MS.)

(JIA - Incorporated last year's API document in here as well.)

(There is probably a standard notation for this, but I'm clueless.)

I'm attempting to group them by the sender/purpose:  BRATA, RPi, Admin.

`ms` is the hostname or IP address of the Master Server.

(JIA: Here are some notes from the beginning of last year's API document.)

* This document describes the API exposed by the Master Server (MS). All calls are REST over HTTP using JSON request and response objects.
* [TODO: Move this document’s contents to Mike’s sequence diagram slides.]
* TODO: Any problem having port 514 available on the MS for forwarding station logs via syslog? Config items for this would be log server IP address and port number; it’s possible log server might be different from MS.
* TODO: Low-priority issue (nice-to-have): Create Network Management screen on MS with R/G/Y status for each station, and probably a Reset button for each station that will send it the reset message.
TODO: Need to specify somewhere that these are the config params for each station:
    * station_id
    * station_type
    * station_url (at least IP and port, maybe determined instead of configured)
    * ms_base_url (at least host/IP and port)


---

## BRATA Messages

(Note from last year's API document: the URL will be in QR format and scanned by the BRATA framework.)

### Register
Notifies  M that the given team wants to register for the challenge.

```
         URL:  http://ms/m/brata-v00/register
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
None


#### JSON Data
```json
{
   "team_id" : "<team's DB id>" ,
   "message" : ""
}
```

#### Query Parameters
Name      | Format | Example | Meaning
----------|--------|---------|--------
team_id   |        |         | the team Id assigned during the registration process
message   |        |         | could be anything including a null string

#### Request Headers
* Accept - the response content type depends on _Accept_ header

#### Response Headers
* Content-Type - application/json

#### JSON Response
```json
{
   "messageteam_id" : "Welcome <school name> to the Design Challenge! Your app has successfully communicated with the Master Server! Congratulations! <Instructions><team’s DB id>"
}
```
#### Status Codes
* 200 OK - no error
* 400 Bad Request - message not JSON, request missing required header, request method incorrect
* 404 Not Found – failed to initiate shutdown

#### Remarks
The message response is the encoded greeting and instructions of where to proceed.

The team’s name, school affiliation and Key will be entered into M during the registration process.  The team will scan the register QR code appending their key.  (The key will be assigned by a random draw).  M will translate the key into its internal DB value which it will return to the framework to be saved for latter messages.


===

### At Waypoint
Notifies M that the given team is at the given waypoint.

```
         URL:  http://ms/m/brata-v00/atWaypoint/<LAT>/<LON>
      Method:  GET
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|--------
LAT       |        |         | latitude in decimal degrees
LON       |        |         | longitude in decimal degrees

(TODO: Last year's document specified ```at_waypoint/<waypointId>```.)

```
Example Request:
POST /m/brata/at_waypoint/<waypointId> HTTP/1.1
Host: example.com
Content-Type: application/json
{
"team_id": "<team’s DB id>"
"message": "" 
}

Example Response:
HTTP/1.1 200 OK
{
"team_id":
"message": "<message to be displayed to user>"
}

Query Parameters:
* waypointId – Note this is technically part of the URI not the content. This is the RDBMS object id of the waypoint
* teamId – the team Id assigned during the registration process
* message – could be anything including the null string.

Request Headers:
* Accept – the response content type depends on Accept header

Response Headers:
* Content-Type – application/json

Status Codes:
* 200 OK – no error
* 404 Not Found – failed to initiate shutdown

Remarks:
The message may be encoded or unencoded depding on the waypoint’s definition the the DB.
```

===

### Start Challenge

Notifies M that the given team is starting a challenge again this URL is scanned from the QR code attached to the station.

```
         URL:  http://ms/m/brata-v00/start_challenge/<TEAMID>/<STATIONID>
      Method:  GET
Content type:  application/json
Return value:  ??
```

(Note: Last year's API document does not mention these parameters at all--only JSON data.)

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|--------
TEAMID    |        |         | the team Id assigned during the registration process
STATIONID |        |         | could be anything including a null string


#### JSON Data
```json
{
   "team_id": "<team id>",
   "message": ""
}
```

#### JSON Response
```json
{
   "message": "“<instruction for the challenge to be displayed to user>"
}
```

#### Request Headers
* Accept – the response content type depends on Accept header

#### Response Headers
* Content-Type – application/json

#### Status Codes
* 200 OK – no error
* 400 Error - extended error message eg. Device didn’t response to start_challenge etc.
* 404 Not Found – standard HTTP response

#### Remarks
The message is always encoded and is the same for all teams and stations.

M will forward the start_challenge to the rPI device associated with this station if one exists.


===

### BRATA Submit
Not sure what this one is. (No mention of this in last year's API document.)
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

## RPi Messages from RPi to MS

### RPi Join

The caller wants to join the system.

```
         URL:  http://ms/m/rpi/join/<ID>
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
ID        |        |         | ID of the Raspberry Pi station. Note: The ID is associated with a station in M's RDBMS, and will be sent by the device to M on subsequent requests to avoid the additional lookup.
message_version   ||         | message schema version, default is 0
message_timestamp ||         | timestamp that the message was sent
TYP       |        | hmb     | one of "hmb", "cpa", or "cts"
URL       |        | http://192.168.0.2:9876 | the url used to call back from the MS to the station

#### JSON Data
```json
{
   "message_version"   : "0" ,
   "message_timestamp" : "2014-09-15 14:08:59",
   "station_type"      : "$TYP" ,
   "station_url"       : "$URL"
}
```

(Note: Last year's API document also specified message_timestamp in the JSON data.)

#### Status Codes

* 202 Accepted – no error
* 400 Bad Request – message not JSON, request missing required header, request method incorrect
* 404 Not Found – standard HTTP status

#### Remarks

The join message will be sent by each station periodically. As long as join messages are received, the MS will consider the station to be alive; if a join message has not been received within 10 (TBD) seconds, then the station will be considered offline.

===

### RPi Submit

Indicates to the MS that the CTS or CPA user has submitted an answer.

```
         URL:  http://ms/m/rest-v00/submit/<ID>
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
ID        |        |         | the same value provided in the join message
message_version   ||         | message schema version, default is 0
message_timestamp ||         | timestamp that the message was sent
`candidate_answer`  ||         | For the CTS this is a list of three values providing the combination for the safe in brackets and coma separated. As an example “ [31, 41, 59]”.  The range for each value is 0..99.  For the CPA the string “True” if the flash was within tolerance or “False” if the flash was not detected or there was an issue with the flash timing.  The details if a failure if a CPA are included in the fail_message parameter.  This message parameter is used by a CTS and CPA only.
is_correct        ||         | "True" if the submitted answer is the correct answer; "False" otherwise. This message parameter is used by a CPA and CTS only. 
fail_message      ||         | a message logged by MS for debugging/troubleshooting


#### JSON Data
```json
{
   "message_version"      : "0" ,
   "message_timestamp"    : "2014-09-15 14:08:59",
   "candidate_answer"     : [31, 41, 59],
   "is_correct"           : "False",
   "fail_message"         : "Incorrect answer provided."
}

//   "station_key"          : "1of7" ,
//   "station_type"         : "hmb" ,
//   "station_callback_url" : "callback"
```

(Note: Last year's API document also specified message_timestamp in the JSON data. The station key was not present in the JSON data. The station key, station type, and station callback url are not listed in last year's API doc.)

#### JSON Response
```json
{
  "message_version": "0",
  "message_timestamp": "2014-09-15 14:08:59"
  "theatric_delay_ms": 3000,
  "challenge_complete": "False"
}
```

#### Request Headers

* Accept – the response content type depends on Accept header
* Authorization – optional Oauth token to authenticate todo

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Response Parameters

* message_version - message schema version, default is 0
* message_timestamp - timestamp that the message was sent
* `theatric_delay_ms` - the amount of time in milliseconds before the station transitions to its challenge completed state. This keeps the user in suspense for a couple extra seconds before finding out whether the answer is correct or not.
* challenge_complete - "False" if the challenge has concluded without completion, i.e. the user has attempted and failed three (TBD) times; "True" otherwise

#### Status Codes

* 200 OK - no error
* 400 Bad Request - invalid request station ID doesn't match

#### Remarks

Note that this message is sent to a MS station by a CTS or CPA only with the station specific parameters. This is still followed by the MS sending a submit message to the CTS or CPA the same way as the other station types.

===

### RPi Leave

(Note: This message was specified in last year's API document; you didn't have it listed here.)

The caller wants to leave the system.

```
         URL:  http://ms/m/leave/<ID>
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
ID        |        |         | the same value provided in the join message


#### Request Headers

* Accept – the response content type depends on _Accept_ header
* Authorization – optional Oauth token to authenticate todo

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Status Codes

* 200 OK - no error
* 404 Not Found - there's no user todo

---

### RPi Time Expired

The caller has aborted a running challenge because the time limit has been reached with no successful answer given. This message applies to the HMB station.

```
         URL:  http://ms/m/time_expired/<ID>
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
ID        |        |         | the same value provided in the join message


#### JSON Data
```json
{
   "message_version"      : "0" ,
   "message_timestamp"    : "2014-09-15 14:08:59"
}
```

#### Request Headers

* Accept – the response content type depends on Accept header

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Status Codes

* 200 OK - no error

#### Remarks

This message to the MS will be followed by a submit message coming back from the MS directing what to do next; therefore, the station will not immediately transition to another state following this transmission of this time_expired message.

===

## RPi Messages to RPi from MS

(Note: These messages were specified in last year's API document; you didn't have them listed here.)

Messages from MS to station use URL and station_id from join message.

### Reset

Abort an currently-running challenge and reinitialize to the resting state.

```
         URL:  http://ms/rpi/reset/<PIN>
      Method:  GET
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
PIN       |        |         | a value to confirm that the reset is intentional


#### Request Headers

* Accept – the response content type depends on _Accept_ header

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Status Codes

* 200 OK - no error
* 403 - provided pin doesn't match expected value

#### Remarks

The reset PIN will always be "31415". Note that there is nothing covert about this value; it is simply used to ensure the request is intentional.

===

### Start Challenge

Start the challenge because the MS has been notified that a user has scanned the QR code for the current station.

```
         URL:  http://ms/rpi/start_challenge
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
message_version   ||         | message schema version, default is 0
message_timestamp ||         | timestamp that the message was sent
`theatric_delay_ms` ||       | the amount of time in milliseconds before the station transitions to its challenge started state. This gives the user time to read any text on the SAT and fully appreciate the hardware starting up.
`hmb_vibration_pattern_ms` ||| a list of six values providing the on/off times for the HMB vibration motors. This field will only be provided to a station that has joined specifying itself as the “hmb” station type.
||| * The first two values provide the on/off times for Vibration Motor #1; the next two values for Motor #2; and the last two for Motor #3.
||| * For each pair, the first specifies the ON time and the second specifies the OFF time.
cpa_velocity ||| a single value providing a temporal measurement from the initial position to the start of the building in ms. This field will only be provided to a station that has joined specifying itself as the "cpa" station type.
cpa_velocity_tolerance_ms ||| [TODO: Mike]. This field will only be provided to a station that has joined specifying itself as the "cpa" station type.  This time has been deprecated, but not removed in case it is later determined it is needed.
cpa_window_time_ms ||| [TODO: Mike]. This field will only be provided to a station that has joined specifying itself as the "cpa" station type. This is the time from the initial starting position to the middle of the window of time that would accept a pulse detection.
cpa_window_time_tolerance_ms ||| [TODO: Mike]. This field will only be provided to a station that has joined specifying itself as the "cpa" station type. This is the tolerance plus or minus milliseconds around the cpa_window_time_ms in which the pulse must occur including the start and end of the flash.
cpa_pulse_width_ms ||| [TODO: Mike]. This field will only be provided to a station that has joined specifying itself as the "cpa" station type. **This is the expected duration of time the flash should be on during the window time.**
cpa_pulse_width_tolerance_ms ||| [TODO: Mike]. This field will only be provided to a station that has joined specifying itself as the "cpa" station type. This is the tolerance for the duration of the flash pulse or minus ms.
cts_combo ||| a list of three values providing the combination for the safe. The range for each value is 0..99. This field will only be provided to a station that has joined specifying itself as the "cts" station type.


#### JSON Data
```json
{
   "message_version"      : "0" ,
   "message_timestamp"    : "2014-09-15 14:08:59",
   "theatric_delay_ms": 3000,
   "hmb_vibration_pattern_ms": [1000, 3000, 1000, 5000, 1000, 11000]
}
```

#### Request Headers

* Accept – the response content type depends on Accept header

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Status Codes

* 202 Accepted - no error
* 400 Bad Request - invalid request station ID doesn't match

#### Remarks

In the example above, the ON time for each motor is always one second, whereas the OFF times for each motor are 3, 5, and 11 seconds, respectively.

===

### Handle Submission

Indicates to the station that the HMB user has submitted an answer and whether or not the answer is correct for the challenge.

```
         URL:  http://ms/rpi/handle_submission
      Method:  POST
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
message_version   ||         | message schema version, default is 0
message_timestamp ||         | timestamp that the message was sent
`theatric_delay_ms` ||       | the amount of time in milliseconds before the station transitions to its challenge completed state. This keeps the user in suspense for a couple extra seconds before finding out whether the answer is correct or not.
is_correct        ||         | "True" if the submitted answer is the correct answer; "False" otherwise.
`challenge_complete` ||      | "False" if the challenge has concluded without completion, i.e. the user has attempted and failed three (TBD) times; "True" otherwise


#### JSON Data
```json
{
   "message_version"      : "0" ,
   "message_timestamp"    : "2014-09-15 14:08:59",
   "theatric_delay_ms": 3000,
   "is_correct": "False",
   "challenge_complete": "False"
}
```

#### Request Headers

* Accept – the response content type depends on _Accept_ header
* Authorization – optional Oauth token to authenticate todo

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Status Codes

* 200 OK - no error

#### Remarks

Note that this message is sent to a CTS station even though the CTS sends a submit message to the MS to provide the answer.

===

### Shutdown

Indicates to the station that it should shutdown.

```
         URL:  http://ms/rpi/shutdown/<PIN>
      Method:  GET
Content type:  application/json
Return value:  ??
```

#### Parameters
Name      | Format | Example | Meaning
----------|--------|---------|-------------------------------
PIN       |        |         | a value to confirm that the reset is intentional


#### Request Headers

* Accept – the response content type depends on _Accept_ header

#### Response Headers

* Content-Type – this depends on _Accept_ header of request

#### Status Codes

* 200 OK - no error
* 403 - provided pin doesn't match expected value

#### Remarks

The shutdown PIN will always be "31415". Note that there is nothing covert about this value; it is simply used to ensure the request is intentional.

Note that this message is sent when the expectation is that the unit will be powered off and in order to come back up power will need to be cycled.

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
