<?php
//  unfortunatly join is also used as a keep alive

//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//   candidate_answer: <string>
//   is_correct: <bool>
//   fail_message: <string>
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
	
	$count = $team->get('count');
	$team->setChallengeData($json);
        trace("count=".$count);
        $points = 3-$count;
	if (!$json['is_correct']) {
		$count++;
		$team->set('count',$count);
                trace("count=".$count);
		$challenge_complete=$count>2;
    	        $team->_updateScore($stationType, 0); //TODO add legacy update score
	}
	else {
	  $challenge_complete=true;
	}
	
	if ($challenge_complete)
	{
           switch($stationType->get('typeCode'))
           {
             case StationType::STATION_TYPE_HMB:
               // Leave scoring up to brata submit for CPA and CTS but HMB needs it 
	       $team->_updateScore($stationType, $points);
	       $station->endChallenge();
	       $team->endChallenge();
               break;
             default:
               // FSL does not have pi, CPA and CTS not done until scan last qr
               // so technically challenge not complete until the brata submit
               break;
           }
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
