<?php
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _at_waypoint($waypointId=null)
{
  if ($waypointId === null) {
    rest_sendBadRequestResponse(400,"missing waypointId");  // doesn't return
  }
  
  $json = json_getObjectFromRequest("POST");
  json_checkMembers("team_id,message", $json);
  $teamPIN = $json['team_id'];
  $team = Team::getFromPin($teamPIN);
  if ($team === false) {
    trace("can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
    rest_sendBadRequestResponse(404,"missing can't find team PIN=".$teamPIN);  // doesn't return
  }
  
  $stationType = StationType::getFSLType();
  if ($stationType === false) {
  	trace("can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
  	rest_sendBadRequestResponse(500,"can't find the FSL StationType");  // doesn't return
  }
  
  $fslState = $team->getChallengeData();
  switch ($fslState['index'])
  {
  	case 0: // use "default" messages for waypoints 1 and 2
  	case 1:
  		break;   
  	case 2:     // for waypoint 2 change success and failed messages, keep retry message the same
  		$stationType->set('success_msg', 'Success! Use radius1=[a_rad] radius2=[b_rad] and radius3=[c_rad] to find the secret labatory marker');
  		$stationType->set('failed_msg' , 'Too bad, you failed. Use radius1=[a_rad] radius2=[b_rad] and radius3=[c_rad] to find the secret labatory marker');
  		break;
  	case 3:    // for the lab change 
  		$stationType->set('success_msg','Success! go quickly to the next queue');
  		$stationType->set('retry_msg'  ,'Wrong secret Laboratory marker, try again!');
  		$stationType->set('failed_msg' ,'Too bad, you failed. Go quickly to the next queue.');  		
  }
  
  $count = $team->get('count');

  $isCorrect = FSLData::isMatch($fslState, $waypointId);
  $challengeComplete = false;
  $points = 0;
  
  if ($isCorrect || $count == 3) {
  	$points = FSLData::updateScore($fslState,3-$count);
    $challengeComplete = !FSLData::nextSection($fslState);
    $team->set('count',0);
  } else {
  	$team->set('count',$count+1);
  }	

  $team->setChallengeData($fslState);                  // put the update state data back into the team object
  $team->updateFSLScore($points );
  
  if ($challengeComplete) {
  	$team->endChallenge();
  }
  
  if       ($isCorrect) $msg = $stationType->get('success_msg');
  else if  ($count >=3) $msg = $stationType->get('failed_msg');
  else                  $msg = $stationType->get('retry_msg');
  
  $msg = $team->expandMessage($msg,$fslState['msg_values']);
  $msg = $team->encodeText($msg);  
  $json = array("message" => $msg);
  json_sendObject($json);
}
