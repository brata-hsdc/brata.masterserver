<?php
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _at_waypoint($waypointId=null)
{
	trace("yes");
  if ($waypointId === null) {
    rest_sendBadRequestResponse(400,"missing waypointId");  // doesn't return
  }
  
  $json = json_getObjectFromRequest("POST");
  json_checkMembers("team_id,message", $json);
  $teamPIN = $json['team_id'];
  $team = Team::getFromPin($teamPIN);
  if ($team === false) {
    trace("_can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
    rest_sendBadRequestResponse(404,"missing can't find team PIN=".$teamPIN);  // doesn't return
  }
  
  $stationType = StationType::getFSLType();
  if ($stationType === false) {
  	trace("_can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
  	rest_sendBadRequestResponse(500,"can't find the FSL StationType");  // doesn't return
  }
  
  $count = $team->get('count');
  $isCorrect = false;
  $challengeComplete = false;
  
  $fslState = $team->getChallengeData();
  if ($fslState['waypoints'][$fslState['index']]==$waypointId) {
  	$isCorrect = true;
  	if (++$fslState['index']==3);
  } else {
  	if (++$count >= 3) $challengeComplete = true;  	
  }	
  
  if       ($isCorrect) $msg = $stationType->get('success_msg');
  else if  ($count >=3) $msg = $stationType->get('failed_msg');
  else                  $msg = $stationType->get('retry_msg');
    
  $team->expandMessage($msg,$table);
  
  if(isEncodeEnabled()) {
  	// if not in student mode encode, if in student mode we only encrypt the even team numbers responses
     if(!isStudenServer() || (isStudenServer() && ($teamPIN % 2 == 0))) {
       $msg = $team->encodeText($msg);
     }
  }
  $json = array("message" => $msg);
  json_sendObject($json);
}
