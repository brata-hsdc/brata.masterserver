<h1>How M Works</h1>
<h2>Introduction</h2>
<p>The site is divided into four major sections (including the 2 rest APIs) which are described below.</p>
<h3>The Management Site</h3>
The management site allows you to CRUD each object manageed by the system. 
 These include the following objects.
 <ul>
 <li><b>Schools</b> - have a name, mascot, and possible a logo if I have time.</li>
 <li><b>Teams</b> - teams are associated with a school and are assigned an randomly generated 5 digit PIN</li>

 <li><b>StationType</b> - have a type code (immutable), a name (immutable), has rPI (immutable)
  a delay (in ms seconds), and instructions for completing the challenge, success message, failure message and a retry message..
 These instructions will be encrypted and sent when the associated start challenge QR URL is scanned.
 </li>
 <li><b>Stations</b> - are associated with a station type, an id/tag that uniquely identifies them to the server.
 </li>
 <li><b>rPI</b> - can be managed here (reset,shutdown etc.) but are dynamiclly added via the join api
    they get associated with a station id via the station_id (a.k.a. tag)
</li>
<li><b>Users</b> - TODO remove?</li>
</ul>
<h3>The Public Site (under redesign)</h3>
The Public Site include the leader board as well as a detailed view that shows each teams score for each station.
The score is calculated vaa the event table which has the stationId, the teamId, the event type, an the points for that event.
Incorrect submits are scored as -1, each completed event is scored as 20, incomplete events are scored as 0.
<h3>The rPI rest API</h3>
<p>This API allows rPI's to interact with M the following methods are supported.</p>
<ul>
<li>join - integrated</li>
<li>submit - no tests</li>
<li>time_expired - no tests</li>
</ul>
<p>There is a cooresponding API that allows M to interace with the rPIs. TODO finalize this API.</p>
<ul>
<li>start_challenge - integated for CTS,CPA, HMB is todo</li>
<li>restart - integrated</li>
<li>shutdown - integrated</li>
<li>time_expired - no tests TODO depreciate this is possible</li>
</ul>
<h3>The Brata rest API</h3>
<p>This API allows the Brata framework to interact with M. TODO finailize this API</p>
<ul>
<li>register - integrated</li>
<li>submit - integrated</li>
</ul> 

<h3>The Debug Section</h3>
<p>This section can be enabled/disabled dynamiclly.
The "Debug" section allows you to "reset" the database which deletes all the data tables views and the recreates them.
You have the option to have reset generate test data.  
<p> By default the database is created with all known station types (see note below), all known station instances, as well 
as the the admin user.
When the test data is generated is inclues the two schools (Bayside and Valley) and two teams (Tigers for Bayside, and 
the Bulldogs for Valley. </p>