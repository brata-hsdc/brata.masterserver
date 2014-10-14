<?php
//
//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//	"value": "true",
//	"station_type": "hmb",
require(APP_PATH.'inc/json_functions.php');
//
function _submit($teamId=null,$stationId=null,$points=0)
{
	if ($teamId === null) {
		rest_sendBadRequestResponse(400,"missing teamId");  // doesn't return
	}
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$json = json_getObjectFromRequest("POST");  // won't return if an error happens
	
	json_checkMembers("message_version,station_type,value", $json);

	//@todo calculate points
	Event::makeEvent(Event::TYPE_SUBMIT, $teamId, $stationId,$points);
	$rpi = RPI::getFromStationId($stationId);
	$rpi->start_challenge($teamId);
     $json = array();  //@todo 
	json_sendObject($json);
}