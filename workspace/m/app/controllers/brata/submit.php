<?php
//
//	"teamId": 0,
//	"message": "",
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _submit($stationTag=null)
{
	if ($stationTag === null) {
		trace("brata missing stationId",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
	}
	
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		trace("brata can't find station stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"can't find station stationTag=".$stationTag);  // doesn't return		
	}
	
	$stationType = new StationType($station->get('typeId'),-1);
	if ($stationType === false ) {
		trace("can't find station type stationTag = ".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500,"can't find station type stationTag=".$stationTag);		
	}
	
	if ($stationType->get('hasrPI'))
	{
	  $rpi = RPI::getFromStationId($station->get('OID'));
	  if ($rpi === false) {
		  trace("_submit can't find RPI stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
		  rest_sendBadRequestResponse(500,"can't find RPI stationTag=".$stationTag);
	  }
	} else {
		$rpi = null;
	}
	
	$json = json_getObjectFromRequest("POST");  // won't return if an error happens
	
	json_checkMembers("message,team_id", $json);
	
	$team = Team::getFromPin($json['team_id']);
	if ($team === false) {
		trace("can't find team from team ".$json['team_id']);
		rest_sendBadRequestResponse(404, "can't find team pin=".$json['team_id']);
	}
	
	$count = $team->get('count');
	$isCorrect = false;
	$challengeComplete = false;
	
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_FSL:
		  break;
		case StationType::STATION_TYPE_HMB:
		  preg_match("/.*answer.*=.*(\d)/", $json['message'], $matches);
		  trace('calling handle_challenge');
          $json = $rpi->handle_submission($stationType->get('delay'),$isCorrect, $challengeComplete);
          //TODO if ($json === false) ERROR???
          //TODO json_checkMembers("message,team_id", $json);
          //$isCorrect=$json['is_correct'];
          break;
		case StationType::STATION_TYPE_EXT:
          preg_match("/.*tower-lat.*=.*(\d)+dd.dddddd] [tower-lon=+dd.dddddd] [tower-height=dddd]",$json['message'],$matches);
          $msg = $stationType->get('success_msg');
          var_dump($matches);
          goto hack;
          
	}
	
	$count = $team->get('count');
	$points = 3-$count;
	$team->updateScore($stationType, $points);
	if (!$json['is_correct']) {
		$count++;
		$team->set('count',$count);
		$challenge_complete=($count<3?false:true);
	}
	else {
		$challenge_complete=true;
	}
	
	if ($challenge_complete)
	{
		$station->endChallenge();
		$team->endChallenge();
	}
	
	if (Event::createEvent(Event::TYPE_SUBMIT, $team, $station,$points) === false) {
		trace("can't create event object",__FILE__,__LINE__,__METHOD__);
		json_sendBadRequestResponse(500,"Can't create event object");
	}
	
	if       ($isCorrect) $msg = $stationType->get('success_msg');
	else if  ($count >=3) $msg = $stationType->get('failed_msg');
	else                  $msg = $stationType->get('retry_msg');
    $msg = $team->expandMessage($msg, $parms );

	if($GLOBALS['SYSCONFIG_ENCODE'] == 1){
          // if not in student mode encode, if in student mode we only encrypt the even team numbers responses
          if($GLOBALS['SYSCONFIG_STUDENT'] == 0 or ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $teamPIN % 2 == 0)) {
            $msg = $team->encodeText($msg);
          }
        }
 hack:
	json_sendObject(array('message' => $msg ) );
}