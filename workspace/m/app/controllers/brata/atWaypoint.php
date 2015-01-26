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
	$msg = Message::getFromWaypointId($waypointId);
	if ($msg === false) {
		rest_sendBadRequestResponse(500,"no message at this waypoint waypointId=$waypointId");  // doesn't return
	}


	transactionBegin();
	if($GLOBALS['SYSCONFIG_ENCODE'] == 1){
          // if not in student mode encode, if in student mode we only encrypt the even team numbers responses
          if($GLOBALS['SYSCONFIG_STUDENT'] == 0 or ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $teamPIN % 2 == 0)) {
            $msg = $team->encodeText($msg);
          }
        }
        $json = array("message" => $msg);
	if (json_sendObject($json)) transactionCommit();
	else                        transactionRollback();
}
