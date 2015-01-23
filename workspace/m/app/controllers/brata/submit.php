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
	
//	$ans = $json['message']

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
	if (Event::createEvent(Event::TYPE_SUBMIT, $team, $station,$points) === false) {
		trace("can't create event object",__FILE__,__LINE__,__METHOD__);
		json_sendBadRequestResponse(500,"Can't create event object");
	}
	if       ($isCorrect) $msg = $stationType->get('success_msg');
	else if  ($count >=3) $msg = $stationType->get('failed_msg');
	else                  $msg = $stationType->get('retry_msg');
    $msg = $team->expandMessage($msg, $parms );
    $msg = $team->encodeText($msg);
	json_sendObject($json);
}