<?php
// brata reports team start challenge at station
//
function _start_challenge($teamId,$stationId) 
{
	
	if ($teamId === null) {
		rest_sendBadRequestResponse(400,"missing teamId");  // doesn't return
	}
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$event = Event::makeEvent(Event::TYPE_START,$teamId, $stationId);
	$event->create();
	// forward start to rPI
	$rpi = RPI::getFromStationId($stationId);
	$json = array();  //@todo what to send to rPI
	$rpi->start_challenge($teamId);
}