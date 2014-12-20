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
	
	if ($stationType->get('hasrPI'))
	{
	  $rpi = RPI::getFromStationId($station->get('OID'));
	  if ($rpi === false) {
		  trace("_start_challenge can't find RPI stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
		  rest_sendBadRequestResponse(500,"can't find RPI stationTag=".$stationTag);
	  }
	} else {
		$rpi = null;
	}
	
	$json = json_getObjectFromRequest("POST");  // won't return if an error happens
	
	json_checkMembers("message,team_id", $json);

	$isCorrect = false;
	$challengeComplete = false;
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_HMB:
		  trace('calling handle_challenge');
          $rpi->handle_challenge($stationType->get('delay'),$isCorrect, $challengeComplete);
          break;
	}
	
	$team = Team::getFromPin($json['team_id']);
	if ($team === false) {
		trace("can't find team from team ".$json['team_id']);
		//todo fail here
	}
	//@todo calculate points
	$points = 0;
	Event::makeEvent(Event::TYPE_SUBMIT, $team->get('OID'), $station->get('OID'),$points);
	//$rpi->start_challenge($teamId);
     $json = array("message"=>"test ".$stationTag);  //@todo 
	json_sendObject($json);
}