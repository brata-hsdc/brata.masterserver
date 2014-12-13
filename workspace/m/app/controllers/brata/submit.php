<?php
//
//	"teamId": 0,
//	"message": "",
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _submit($stationId=null)
{
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$json = json_getObjectFromRequest("POST");  // won't return if an error happens
	
	json_checkMembers("message,teamId", $json);

	//@todo calculate points
	Event::makeEvent(Event::TYPE_SUBMIT, $teamId, $stationId,$points);
	$rpi = RPI::getFromStationId($stationId);
	//$rpi->start_challenge($teamId);
     $json = array();  //@todo 
	json_sendObject($json);
}