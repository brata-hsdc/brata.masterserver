<?php
// 
//	sent by rPI when challenge end due to time out
//  stationId - station id assigned to rPI during join
//  teamId - team id assigned to rPI during start-challenge
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');

function _time_expired($stationId=null,$teamId) {
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");
	}
	if ($teamId === null) {
		rest_sendBadRequestResponse(400,"missing teamId");
	}
	// todo update score?
	rest_sendBadRequestResponse(501, "not implemented");
}