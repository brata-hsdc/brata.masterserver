# Master Server Message Summary

These messages are sent between the Master Server and another device.
They are described in detail in
the [**Master Server Web Service Interface**](ms_interface.md)
document.

## BRATA Messages

These messages are sent from a BRATA device to the Master Server.
These transactions are handled by the Master Server `piservice` app.

The last component of the URL in these messages is the BRATA message protocol
version.  For the 2016 competition, the protocol version is *brata-v01*.  The
version is included for backward compatibility.  However, for the 2016 competition,
*brata-v01* is the only protocol version that is guaranteed to be recognized.

The URL format follows this pattern:  http://*ms-host-or-ip*/*msg_type*/*brata_ver*/*params*

Message         | Type | URL                                                | Params Sent | Params Received
----------------|------|----------------------------------------------------|-------------|----------------
Register        | POST | <b>http://</b><i>ms</i><b>/register/brata-v01</b>                     | team_id     | message
At Waypoint     | POST | <b>http://</b><i>ms</i><b>/at_waypoint/brata-v01/</b><i>&lt;lat&gt;</i><b>/</b><i>&lt;lon&gt;</i>      | team_id     | message
Start Challenge | GET  | <b>http://</b><i>ms</i><b>/start_challenge/brata-v01/</b><i>&lt;station_id&gt;</i> | team_id     | message
Submit          | POST | <b>http://</b><i>ms</i><b>/submit/brata-v01/</b><i>&lt;station_id&gt;</i>          | message_version, station_key, station_type, station_callback_url | message


### Questions about BRATA Messages

1. Why is **Start Challenge** a **GET** message, while the others are **POST**?
2. **Submit** is not well documented.  What is its purpose?  What are the params?


## RPi Messages

These messages are sent from an RPi station to the Master Server.
These transactions are handled by the Master Server `piservice` app.

The last component of the URL in these messages is the RPi message protocol
version.  For the 2016 competition, the protocol version is *rpi-v01*.  The
version is included for backward compatibility.  However, for the 2016 competition,
*rpi-v01* is the only protocol version that is guaranteed to be recognized.

The URL format follows this pattern:  http://*ms-host-or-ip*/*msg_type*/*rpi_ver*/*params*

Message         | Type | URL                                           | Params Sent | Params Received
----------------|------|-----------------------------------------------|-------------|----------------
Join            | POST | <b>http://</b><i>ms</i><b>/join/rpi-v01</b>                      | station_id  | message
Submit          | POST | <b>http://</b><i>ms</i><b>/submit/rpi-v01</b>                    | *multiple*  | *multiple*
Leave           | POST | <b>http://</b><i>ms</i><b>/leave/rpi-v01/</b><i>&lt;station_id&gt;</i>        |             | 
Time Expired    | POST | <b>http://</b><i>ms</i><b>/time_expired/rpi-v01/</b><i>&lt;station_id&gt;</i> | timestamp   | 

### Questions about RPi Messages

1. Why was the version for **Submit** in the [**ms_interface**](ms_interface.md) document *rest-v00* instead
of *rpi_v00* like **Join**?
2. The **Leave** message is not well documented.


## MS Messages

These messages are sent from the Master Server to an RPi station.
These transactions are handled by the Master Server `piservice` app.

The URL format follows this pattern:  http://*rpi-host-or-ip*/*msg_type*/*ms_ver*/*params*

Message           | Type | URL                                              | Params Sent | Params Received
------------------|------|--------------------------------------------------|-------------|----------------
Reset             | GET  | <b>http://</b><i>rpi</i><b>/reset/ms-v01/</b><i>&lt;pin&gt;</i>                  |             | 
Start Challenge   | POST | <b>http://</b><i>rpi</i><b>/start_challenge/ms-v01</b>              | *multiple*  | 
Handle Submission | POST | <b>http://</b><i>rpi</i><b>/handle_submission/ms-v01</b>            | *multiple*  | 
Shutdown          | GET  | <b>http://</b><i>rpi</i><b>/shutdown/ms-v01/</b><i>&lt;pin&gt;</i>               |             | 


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
