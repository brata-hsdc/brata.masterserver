<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
// stationTag is stationId in ICD
function _cpaMeasure($stationTag=null) 
{
	if ($stationTag === null) {
		rest_sendBadRequestResponse(400,"missing station Tag");  // doesn't return
	}
	
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		rest_sendBadRequestResponse(404,"can find station stationTag=".$stationTag);  // doesn't return		
	}
	
	$stationType = new StationType($station->get('typeId'),-1);
	if ($stationType === false ) {
		trace("can't find station type stationTag = ".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500,"can't find station type stationTag=".$stationTag);		
	}
	
	$json = json_getObjectFromRequest("POST");
	json_checkMembers("team_id,message", $json);
        $teamPIN = $json['team_id'];

	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		trace("_cpaMeasure can't find team teamPin=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"team not found PIN=".$teamPIN);  // doesn't return
	}
	
	$stationId = $station->get('OID');
	$parms = null; // compute challenge parameters into a message
	switch($stationType->get('typeCode'))
	{
	    case StationType::STATION_TYPE_CPA:
                $random = new CPAData();
	        $parms = $random->getItemsToMeasure();
                trace("CPA measure generated for team ".$teamPIN." this data ".print_r($parms,true));
                // record the challenge data randomly generated
                $team->setChallengeData($parms);
	        break;
            default:
		trace("_cpaMeasure can't find station tyecode=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"station tyecode not found =".$stationType->get('typeCode'));  // doesn't return
	}
	
	if ( Event::createEvent(Event::TYPE_START,$team, $station,0) ===false) {
		trace("create event failed",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "database create failed");
	}

	$msg = $team->expandMessage("PA is trying to escape. Quickly measure [fence=[label]] [building=[label]] and scan Start QR Code.", $parms );
	trace("message before decode $msg",__FILE__,__LINE__,__METHOD__);
    $msg = $team->encodeText($msg);
	json_sendObject(array('message' => $msg ) );
}

