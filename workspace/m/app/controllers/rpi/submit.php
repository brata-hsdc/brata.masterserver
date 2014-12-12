<?php
//  unfortunatly join is also used as a keep alive

//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//	"station_id": "97531",
//	"station_type": "hmb",
//	"station_url": "http://192.168.0.2:9876"
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _submit($stationId=null)
{
	if ($stationId === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("message_version,message_timestamp,candidate_answer,is_correct,fail_message", $json);

	//@todo calculate points
	Event::makeEvent(Event::TYPE_SUBMIT, $teamId, $stationId,$points);
	$rpi = RPI::getFromStationId($stationId);
	//$rpi->start_challenge($teamId);
	$json = array();  //@todo
	json_sendObject($json);
}
