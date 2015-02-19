<?php
//
//	"teamId": 0,
//	"message": "",
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');

function _submit($stationTag=null)
{
	if ($stationTag === null) {
		trace("brata missing stationId",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		trace("brata can't find station stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"can't find station stationTag=".$stationTag);  // doesn't return		
	}
	
	$json = json_getObjectFromRequest("POST");  // won't return if an error happens
	
	json_checkMembers("message,team_id", $json);
	
	$team = Team::getFromPin($json['team_id']);
	if ($team === false) {
		trace("can't find team from team ".$json['team_id']);
		rest_sendBadRequestResponse(404, "can't find team pin=".$json['team_id']);
	}	
	$stationType = new StationType($station->get('typeId'),-1);
	if ($stationType === false ) {
		trace("can't find station type stationTag = ".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500,"can't find station type stationTag=".$stationTag);		
	}
	

	try
	{
		$xxxData = XXXData::factory($stationType->get('typeCode'));
		$msg = $xxxData->brataSubmit($json['message'], $team,$station,$stationType);
		json_sendObject(array('message' => $msg ) );
	}
	catch (InternalError $ie)
	{
		rest_sendBadRequestResponse($ie->getCode(), $ie->getMessage());
	}
	
}