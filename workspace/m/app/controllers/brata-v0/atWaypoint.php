<?php
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _atWaypoint($lat=null,$lng=null)
{
	if ($lat === null) {
		rest_sendBadRequestResponse(400,"missing lat");  // doesn't return
	}
	if ($lng === null) {
		rest_sendBadRequestResponse(400,"missing lng");  // doesn't return
	}
	
    $waypoint = Waypoint::getFromLatLng($lat, $lng);
    if ($waypoint === false) rest_sendBadRequestResponse(404,"waypoint not found");
    $json = array("message" => $waypoint->get('description'));
	json_sendObject($json);
}
