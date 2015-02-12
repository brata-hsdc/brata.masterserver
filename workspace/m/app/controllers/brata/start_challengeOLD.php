<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
// stationTag is stationId in ICD
function _start_challengeOLD($stationTag=null) 
{
	if ($stationTag === null) {
		rest_sendBadRequestResponse(400,"missing station Tag");  // doesn't return
	}
	
	$station = Station::getFromTag($stationTag);
	if ($station === false) {
		rest_sendBadRequestResponse(404,"can find station stationTag=".$stationTag);  // doesn't return		
	}
	
	$stationType = new StationType($station->get('typeId'),-1);
	if ($stationType === false ) {
		trace("can't find station type stationTag = ".$stationTag,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500,"can't find station type stationTag=".$stationTag);		
	}

	if ($stationType->get('hasrPI')) {
		$rpi = RPI::getFromStationId($station->get('OID'));
		if ($rpi === false) {
			trace("_start_challenge can't find RPI stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
			rest_sendBadRequestResponse(500,"can't find RPI stationTag=".$stationTag);
		}
	} else {
		$rpi=null;
	}	
	$json = json_getObjectFromRequest("POST");
	json_checkMembers("team_id,message", $json);
    $teamPIN = $json['team_id'];

	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		trace("_start_challenge can't find team teamPin=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"team not found PIN=".$teamPIN);  // doesn't return
	}
	
	$stationId = $station->get('OID');
	$parms = null; // compute challenge parameters into a php hash which will be sent to rPI and used to populate message sent to team
	$state = null;
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_CTS:
			$parms = CTSData::_startChallenge($stationId);
	        break;
	    case StationType::STATION_TYPE_HMB:
	    	$parms = HMBData::_startChallenge($stationId);
	    	break;
	    case StationType::STATION_TYPE_CPA:
	        $parms = CPAData::_startChallenge($stationId);
	        break;
	    case StationType::STATION_TYPE_FSL:
   	        $state= FSLData::_startChallenge($stationId);
   	        $parms=$state['msg_values'];
	        break;
	    case StationType::STATION_TYPE_EXT:
	        $state = EXTData::_startChallenge($stationId);
	        $parms = $state;
	        break;
	}
	
	if ($rpi!=null) {
		trace("sending to rPI");
		$rpi->start_challenge($stationType->get('delay'),$parms);
	}
	trace("station and team start calls");
	//TODO transaction
	$station->startChallenge($team);
	$team->startChallenge($parms,$stationType->get('typeCode'),$state);  // $state
	
	if ( Event::createEvent(Event::TYPE_START,$team, $station,0, $state) ===false) {
		trace("create event failed",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "database create failed");
	}

	$msg = $team->expandMessage($stationType->get('instructions'), $parms );
	if($GLOBALS['SYSCONFIG_ENCODE'] == 1){
          // if not in student mode encode, if in student mode we only encrypt the even team numbers responses
          if($GLOBALS['SYSCONFIG_STUDENT'] == 0 or ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $teamPIN % 2 == 0)) {
            $msg = $team->encodeText($msg);
          }
        }
	json_sendObject(array('message' => $msg ) );
}


