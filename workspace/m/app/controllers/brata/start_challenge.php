<?php
// brata reports team start challenge at station
//
function _start_challenge($stationId=null,$teamPIN=null) 
{
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	if ($teamPIN === null) {
		rest_sendBadRequestResponse(400,"missing team PIN");  // doesn't return
	}
	$teamId = Team::getFromPin($teamPIN);
	if ($teamId === false) {
		rest_sendBadRequestResponse(400,"unknown team PIN");  // doesn't return		
	}
	
	$event = Event::makeEvent(Event::TYPE_START,$teamId, $stationId);
	$event->create();
	// forward start to rPI
	$rpi = RPI::getFromStationId($stationId);
	$json = array();  //@todo what to send to rPI
	$rpi->start_challenge($teamId);
}