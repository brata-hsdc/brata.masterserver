<?php
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _atWaypoint($waypointId=null,$teamId=null)
{
	if ($waypointId === null) {
		rest_sendBadRequestResponse(400,"missing waypointId");  // doesn't return
	}
	if ($teamId === null) {
		rest_sendBadRequestResponse(400,"missing teamId");  // doesn't return
	}
//	if ($lng === null) {
//		rest_sendBadRequestResponse(400,"missing lng");  // doesn't return
//	}
//	if ($lat === null) {
//		rest_sendBadRequestResponse(400,"missing lat");  // doesn't return
//	}

	$waypoint = new Waypoint($waypointId,-1);
	$message = Message::getFromWaypointId($waypointId);
	if ($message === false) {
		rest_sendBadRequestResponse(500,"no message at this waypoint waypointId=$waypointId");  // doesn't return
	}
	$text = $message->get('text');
	if ($waypoint->get('encode')) {
		$text = "!$text";
	}
    //$waypoint = Waypoint::getFromLatLng($lat, $lng);
    //if ($waypoint === false) rest_sendBadRequestResponse(404,"waypoint not found");
	transactionBegin();
	Event::makeEvent(Event::TYPE_ARRIVE, $teamId, $stationId); // BUG!!! have way point need station?
    $json = array("message" => $text);
	if (json_sendObject($json)) transactionCommit();
	else                        transactionRollback();
}
