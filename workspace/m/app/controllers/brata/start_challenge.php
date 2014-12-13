<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
// stationTag is stationId in ICD
function _start_challenge($stationTag=null) 
{
	if ($stationTag === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		rest_sendBadRequestResponse(404,"can find station stationId=".$stationTag);  // doesn't return		
	}
	$rpi = RPI::getFromStationId($station->get('OID'));
		
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("team_id,message", $json);
    $teamPIN = $json['team_id'];

	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		rest_sendBadRequestResponse(404,"team not found PIN=".teamPIN);  // doesn't return
	}
	
	$event = Event::makeEvent(Event::TYPE_START,$teamId, 0); // todo use real id
	$event->create();
	// todo send message to station
	$rpi->
	$json = array('message' => "test");  //@todo what to send to rPI
	json_sendObject($json);
	
	$teamId = Team::getFromPin($teamPIN);

	
	$event = Event::makeEvent(Event::TYPE_START,$teamId, $stationId);
	$event->create();
	// forward start to rPI

	$json = array();  //@todo what to send to rPI
	$rpi->start_challenge($teamId);
}

