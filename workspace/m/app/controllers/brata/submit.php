<?php
//
//	"teamId": 0,
//	"message": "",
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _submit($stationTag=null)
{
	if ($stationTag === null) {
		trace("brata missing stationId",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		trace("brata can't find station stationTag".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"can't find station stationTag=".$stationTag);  // doesn't return		
	}
	
	$stationType = new StationType($station->get('typeId'),-1);
	if ($stationType === false ) {
		trace("can't find station type stationTag = ".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500,"can't find station type stationTag=".$stationTag);		
	}
	
	$rpi = RPI::getFromStationId($station->get('OID'));
	if ($rpi === false) {
		trace("_start_challenge can't find RPI stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500,"can't find RPI stationTag=".$stationTag);
	}
	
	$json = json_getObjectFromRequest("POST");  // won't return if an error happens
	
	json_checkMembers("message,teamId", $json);

	$isCorrect = false;
	$challengeComplete = false;
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_HMB:
		  trace('calling handle_challenge');
          $rpi->handle_challenge($stationType->get('delay'),$isCorrect, $challengeComplete);
          break;
	}
	
	//@todo calculate points
	Event::makeEvent(Event::TYPE_SUBMIT, $teamId, $stationId,$points);
	//$rpi->start_challenge($teamId);
     $json = array();  //@todo 
	json_sendObject($json);
}