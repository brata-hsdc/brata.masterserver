<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
function _register() 
{
	trace("start",__FILE__,__LINE__,__METHOD__);
	
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("team_id,message", $json);
    $teamPIN = $json['team_id'];
	if ($teamPIN === null) {
		trace("missing PIN",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(400,"missing team PIN");  // doesn't return
	}
	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		trace("_can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"missing can' fint team PIN=".$teamPIN);  // doesn't return
	}
	
	// we are assuming that the QR code won't include the station tag.
	$station = Station::getRegistrationStation();
	if ($station === false) {
		trace("can't find registration station",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "can't fing registration station");
	}

	if (Event::createEvent(Event::TYPE_REGISTER,$team, $station,0) === false) {
	  trace("createEvent Failes",__FILE__,__LINE__,__METHOD__);
	  rest_sendBadRequestResponse(500, "could not create event object");	
	}
    $stationType = StationType::getFromTypeCode($station->get('tag'));
    Team::
	json_sendObject(array('message' => $stationType->get('instructions')) );
}