<?php
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _atWaypoint($waypointId=null)
{
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
  trace("getting fslState");
  $fslState = $team->getChallengeData();
  trace("fslState is now ".print_f($fslData,true));
  
  if($GLOBALS['SYSCONFIG_ENCODE'] == 1){
  	// if not in student mode encode, if in student mode we only encrypt the even team numbers responses
     if($GLOBALS['SYSCONFIG_STUDENT'] == 0 or ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $teamPIN % 2 == 0)) {
       $msg = $team->encodeText($msg);
     }
  }
  $json = array("message" => $msg);
  json_sendObject($json);
}
