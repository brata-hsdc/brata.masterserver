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
	$stationType = StationType::getFromShortname("REG");
	if ($stationType === false) {
		trace("can't find REG station",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "can't fing REG station");
	}

	$event = Event::makeEvent(Event::TYPE_REGISTER,$team->get('OID'), $stationType->get('OID'));
	$tmp = $event->create();
	$json = array('message' => $stationType->get('instructions'));
	json_sendObject($json);
}