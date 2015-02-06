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
  $challengeComplete = false;
  $atLab = FSLData::atLab($fslState);   // are we looking for the lab?
  $labNext = false;                     // is the lab next?
  
  if ($isCorrect) {
    FSLData::nextWaypoint($fslState);
    $labNext = FSLData::atLab($fslState); // are we now looking for the lab?
    $team->set('count',0);
  } else {
  	$team->set('count',++$count);
  }	
  
  //TODO Too bad, you failed. Use ...
  //TODO Success! go quickly to the next queue
  //TODO Wrong secet Laboratory marker, try again!
  //TODO Too bad, you failed. Go quickly to the next queue.
  if  ($atLab) {
  	if  ($isCorrect) {
  		//$msg = $stationType->get('TODO');
  		$msg = 'Success! go quickly to the next queue';
  		$challengeComplete = true;
  	}
  	else if  ($count < 3) {
  		//$msg = $stationType->get('TODO');
  		$msg = 'Wrong secet Laboratory marker, try again!';
  	}
  	else {
  		//$msg = $stationType->get('TODO');
  		$msg = 'Too bad, you failed. Go quickly to the next queue.';
  		$challengeComplete = true;
  	}	
  } 
  else if ($labNext) 
  {
  	//TODO move messages to DB if possible
  	$prefix = ($isCorrect) ? "Success!" : "Too bad, you failed.";
  	$msg = "$prefix Use radius1=[a_rad] radius2=[b_rad] and radius3=[c_rad] to find the secret labatory marker";
  } 
  else 
  {
  	if  ($isCorrect) {
  	  $msg = $stationType->get('success_msg');
    }
    else if  ($count < 3) { 
  	  $msg = $stationType->get('retry_msg'); 
    }
    else {
  	  $msg = $stationType->get('failed_msg');
    }
  }

  trace("the poings  is ".(3-$count));
  $points = FSLData::updateScore($fslState,3-$count);
  trace("the point are $points");
  $team->setChallengeData($fslState);                  // put the update state data back into the team object
  $team->updateScore($stationType, $points );
  
  if ($challengeComplete) {
  	$team->endChallenge();
  }
    
  $msg = $team->expandMessage($msg,$fslState['msg_values']);
  
  if(isEncodeEnabled()) {
  	// if not in student mode encode, if in student mode we only encrypt the even team numbers responses
     if(!isStudentServer() || (isStudentServer() && ($teamPIN % 2 == 0))) {
       $msg = $team->encodeText($msg);
     }
  }
  $json = array("message" => $msg);
  json_sendObject($json);
}
