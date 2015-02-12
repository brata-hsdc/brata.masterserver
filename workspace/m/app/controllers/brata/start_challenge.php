<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
// stationTag is stationId in ICD
function _start_challenge($stationTag=null) 
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
		trace("_start_challenge can't find team teamPin=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"team not found PIN=".$teamPIN);  // doesn't return
	}
	try 
	{
	  $xxxData = XXXData::factory($stationType->get('typeCode'));
	  $msg = $xxxData->startChallenge($team,$station,$stationType);
	  json_sendObject(array('message' => $msg ) );
	}
	catch (InternalError $ie)
	{
		rest_sendBadRequestResponse($ie->getCode(), $ie->getMessage());
	}
}

