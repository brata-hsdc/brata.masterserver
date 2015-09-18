# Master Server Message Summary

These messages are sent between the Master Server and another device.
They are described in detail in
the [**Master Server Web Service Interface**](ms_interface.md)
document.

## BRATA Messages

These messages are sent from a BRATA device to the Master Server.
These transactions are handled by the Master Server `piservice` app.

The URL format follows this pattern:  http://*ms-host-or-ip*/*msg_type*/*params*

Message         | Type | URL                                                | Params Sent | Params Received
----------------|------|----------------------------------------------------|-------------|----------------
Register        | POST | <b>http://</b><i>ms</i><b>/register/</b>           | team_id     | message
At Waypoint     | POST | <b>http://</b><i>ms</i><b>/at_waypoint/</b><i>&lt;lat&gt;</i><b>/</b><i>&lt;lon&gt;</i>      | team_id     | message
Start Challenge | GET  | <b>http://</b><i>ms</i><b>/start_challenge/</b><i>&lt;station_id&gt;</i> | team_id     | message
Submit          | POST | <b>http://</b><i>ms</i><b>/submit/</b><i>&lt;station_id&gt;</i>          | message_version, station_key, station_type, station_callback_url | message

The MS response to these messages consist of a human-readable (although it may need to be decrypted first) `message` string that is intended to be read by the competitors.  There is also the opportunity to return other items in the JSON data that the BRATA software could receive directly, but this option is currently not being utilized.

### Questions about BRATA Messages

1. Why is **Start Challenge** a **GET** message, while the others are **POST**?
2. **Submit** is not well documented.  What is its purpose?  What are the params?


## RPi Messages

These messages are sent from an RPi station to the Master Server.
These transactions are handled by the Master Server `piservice` app.

The URL format follows this pattern:  http://*ms-host-or-ip*/*msg_type*/*params*

Message         | Type | URL                                           | Params Sent | Params Received
----------------|------|-----------------------------------------------|-------------|----------------
Join            | POST | <b>http://</b><i>ms</i><b>/join/</b>          | host, pi_type, station_type  | station_id
Submit          | POST | <b>http://</b><i>ms</i><b>/submit/</b>        | *multiple*  | *multiple*
Leave           | POST | <b>http://</b><i>ms</i><b>/leave/</b>         | station_id  | message
Time Expired    | POST | <b>http://</b><i>ms</i><b>/time_expired/</b>  | station_id, timestamp   | 

*station_id* will be a unique identifier prepended with the PiStation database record id field value followed
by a colon, so for example, it might look like this:  `42:980a7df789g`.

### Questions about RPi Messages

1. The **Leave** message is not well documented.  I assume that it means the station (or at least the station app)
is going offline.  Why are we passing the *station_id* as a URL param in this message, whereas the **Join** message
sends it as POST data? (Changing it to send *station_id* as POST data.)
2. Is station_instance useful for anything?  It is kind of bothersome to compute the station_instance (like RTE #3)
because stations can join and leave at any time.


## MS Messages

These messages are sent from the Master Server to an RPi station.
These transactions are handled by the Master Server `piservice` app.

The URL format follows this pattern:  http://*rpi-host-or-ip*/*msg_type*/*params*

Message           | Type | URL                                              | Params Sent | Params Received
------------------|------|--------------------------------------------------|-------------|----------------
Reset             | GET  | <b>http://</b><i>rpi</i><b>/reset/</b><i>&lt;pin&gt;</i>                  |             | 
Start Challenge   | POST | <b>http://</b><i>rpi</i><b>/start_challenge/</b>              | *multiple*  | 
Handle Submission | POST | <b>http://</b><i>rpi</i><b>/handle_submission/</b>            | *multiple*  | 
Shutdown          | GET  | <b>http://</b><i>rpi</i><b>/shutdown/</b><i>&lt;pin&gt;</i>               |             | 


## Admin Messages

These messages are sent to the Master Server from a web browser.  They return HTML web pages.
These transactions are handled by the Master Server `dbkeeper` app.

```
Browser   ---------------------------- GET ---------------------------> MS
Browser <------------------------- text/html ------------------------   MS
Browser   ----------------- POST multipart/form-encoded --------------> MS
Browser <------------------------- text/html ------------------------   MS
```

The URL format follows this pattern:  http://*ms-host-or-ip*/*operation*/*entity*/

Message           | Type | URL                                              | Params Sent | Params Received
------------------|------|--------------------------------------------------|-------------|----------------
Add Organization  | GET  | <b>http://ms/add/organization/</b>               |             | 
Add User          | GET  | <b>http://ms/add/user/</b>                       |             | 
Add Team          | GET  | <b>http://ms/add/team/</b>                       |             | 
Check In Team     | GET  | <b>http://ms/checkin/team/</b>                   |             | 
