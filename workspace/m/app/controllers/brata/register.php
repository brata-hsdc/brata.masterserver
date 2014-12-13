<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
function _register() 
{
	trace("register");
	
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("team_id,message", $json);
    $teamPIN = $json['team_id'];
	if ($teamPIN === null) {
		error_log("missing PIN\n",3,"/var/tmp/m.log");
		rest_sendBadRequestResponse(400,"missing team PIN");  // doesn't return
	}
	$teamId = Team::getFromPin($teamPIN);

	$event = Event::makeEvent(Event::TYPE_START,$teamId, 0); // todo use real id
	$event->create();
	// todo send message to station
	$json = array('message' => "test");  //@todo what to send to rPI
	json_sendObject($json);
}