<?php
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _at_waypoint($waypointId=null)
{
	trace("waypointId = $waypointId");
  if ($waypointId === null) {
    rest_sendBadRequestResponse(400,"missing waypointId");  // doesn't return
  }
  
  $json = json_getObjectFromRequest("POST");
  json_checkMembers("team_id,message", $json);
  $teamPIN = $json['team_id'];
  $team = Team::getFromPin($teamPIN);
  trace("got team from pin".print_r($team,true));
  if ($team === false) {
    trace("can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
    rest_sendBadRequestResponse(404,"missing can't find team PIN=".$teamPIN);  // doesn't return
  }
  
  $stationType = StationType::getFSLType();
  if ($stationType === false) {
  	trace("can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
  	rest_sendBadRequestResponse(500,"can't find the FSL StationType");  // doesn't return
  }
  
  $count = $team->get('count');
  $fslState = $team->getChallengeData();
  $isCorrect = FSLData::isMatch($fslState, $waypointId);
  trace("isCorrect=$isCorrect");
  $challengeComplete = false;
  
  if ($isCorrect) {
  	if (!FSLData::nextWaypoint($fslState)) {
  		$challengeComplete = true;  		
  	} else {
  		$team->set('count',0);
  		$team->setChallengeData($fslState);
  	}
  }
  else {
  	$team->set('count',++$count);
  	$team->setChallengeData($fslState);
  }	
  
  if       ($challengeComplete) {
  	$msg = "[a_rad] [b_rad] [c_rad]";
  } 
  else if  ($isCorrect) {
  	$msg = $stationType->get('success_msg');
  }
  else if  ($count < 3) { 
  	$msg = $stationType->get('retry_msg'); 
  }
  else {
  	$msg = $stationType->get('failed_msg');
  }
  $team->updateScore($stationType, 3-$count);
  if ($challengeComplete) $team->endChallenge();
    
  $msg = $team->expandMessage($msg,$fslState);
  
  if(isEncodeEnabled()) {
  	// if not in student mode encode, if in student mode we only encrypt the even team numbers responses
     if(!isStudentServer() || (isStudentServer() && ($teamPIN % 2 == 0))) {
       $msg = $team->encodeText($msg);
     }
  }
  $json = array("message" => $msg);
  json_sendObject($json);
}
