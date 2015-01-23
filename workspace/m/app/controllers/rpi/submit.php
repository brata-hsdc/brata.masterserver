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
function _submit($stationTag=null)
{
	if ($stationTag === null) {
		trace("missing station id");
		rest_sendBadRequestResponse(401,"missing stationId");  // doesn't return
	}
	
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		trace("can't find station from tag");
		rest_sendBadRequestResponse(404,"can find station stationTag=".$stationTag);  // doesn't return		
	}
	$team = new Team($station->get('teamAtStation'),-1);
	if ($team === false ) {
		trace("can't find team",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"can find team at station stationTag=".$stationTag." teamId=".$team->get('OID'));  // doesn't return
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
	
	json_checkMembers("candidate_answer,is_correct,fail_message", $json);

	// for CTS candidate_answer is array of three
	// for CPA candidate_answer is text hit in/out of window
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_CTS:
			break;
		case StationType::STATION_TYPE_CPA:
			break;
		
	}

	//TODO count >= 3
	$count = $team->get('count');
	$points = 3-$count;
	$team->updateScore($stationType, $points);
	if (!$json['is_correct']) {
		$team->set('count',$count+1);
		$challenge_complete=false;
	}
	else {
	   $station->endChallenge();
	   $team->endChallenge();
	   $challenge_complete=true;
	}

	if (Event::createEvent(Event::TYPE_SUBMIT, $team, $station,$points) === false) {
		trace("create event failed ".$team->get('OID')." ".$station->get('OID'),__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "database create failed");
	}
	
	$json = array("message_version" =>0 ,
			"message_timestamp"=> date("Y-m-d H:i:s"),
			"theatric_delay_ms"=>$stationType->get('delay') ,
			"challenge_complete"=>$challenge_complete
	);
	
	json_sendObject($json);
}