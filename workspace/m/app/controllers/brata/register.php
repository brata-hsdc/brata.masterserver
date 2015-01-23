<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
function _register($tag='reg01') 
{
	trace("start",__FILE__,__LINE__,__METHOD__);
	
	$json = json_getObjectFromRequest("POST");
	json_checkMembers("team_id,message", $json);
        $teamPIN = $json['team_id'];
	if ($teamPIN === null) {
		trace("missing PIN",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(400,"missing team PIN");  // doesn't return
	}
	
	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		trace("_can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"missing can't find team PIN=".$teamPIN);  // doesn't return
	}
	
	// we are assuming that the QR code won't include the station tag.
	$station = Station::getRegistrationStation();
	if ($station === false) {
		trace("can't find registration station",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "can't find registration station");
	}

    $points = 3;
	if (Event::createEvent(Event::TYPE_REGISTER,$team, $station,$points) === false) {
	  trace("createEvent Fails",__FILE__,__LINE__,__METHOD__);
	  rest_sendBadRequestResponse(500, "could not create event object");	
	}

    $stationType = StationType::getFromTypeCode($station->get('tag'));
    trace("registration complete",__FILE__,__LINE__,__METHOD__);
    $team->updateScore($stationType, $points);
    $msg = $team->expandMessage($stationType->get('instructions'), null ) ;
    if(isEncodeEnabled()) $msg = $team->encodeText($msg);
	json_sendObject(array('message' => $msg) );
}

