<?php
// 
//	sent by rPI when challenge end due to time out
//  stationId - station id assigned to rPI during join
//  teamId - team id assigned to rPI during start-challenge
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');

// if possible fold this into submit my adding challenge_over to message
function _time_expired($stationId=null) {
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");
	}
	error_log("time expired\n",3,"/var/tmp/m.log");
	// todo update score?
	rest_sendBadRequestResponse(501, "not implemented");
	
}