<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
// stationTag is stationId in ICD
function _start_challenge($stationTag=null) 
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
	//if ($json === NULL) return;
	json_checkMembers("team_id,message", $json);
    $teamPIN = $json['team_id'];

	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		trace("_start_challenge can't find team teamPin=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"team not found PIN=".$teamPIN);  // doesn't return
	}
	
	$stationId = $station->get('OID');
	$parms = null; // compute challenge parameters into a php hash which will be sent to rPI and used to populate message sent to team
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_CTS:
			$parms = CTSData::startChallenge($stationId);
	        break;
	    case StationType::STATION_TYPE_HMB:
	    	$parms = HMBData::startChallenge($stationId);
	    	break;
	    case StationType::STATION_TYPE_CPA:
	        $parms = CPAData::startChallenge($stationId);
	        break;
	    case StationType::STATION_TYPE_EXT:
	    	$parms = EXTData::startChallenge($stationId);
	        break;
	    case StationType::STATION_TYPE_FSL:
                // For testing need to send them to their schools params
                if($GLOBALS['SYSCONFIG_STUDENT'] == 1) {
                  switch($teamPIN){
                    case '00001':
                    case '00002':
                      $parms = FSLData::startChallenge('T-WP');
                      break;
                    case '00003':
                    case '00004':
                      $parms = FSLData::startChallenge('EW-WP');
                      break;
                    case '00005':
                    case '00006':
                      $parms = FSLData::startChallenge('HT-WP');
                      break;
                    case '00007':
                    case '00008':
                      $parms = FSLData::startChallenge('WS-WP');
                      break;
                    case '00009':
                    case '00010':
                      $parms = FSLData::startChallenge('M-WP');
                      break;
                    case '00011':
                    case '00012':
                      $parms = FSLData::startChallenge('PB-WP');
                      break;
                    case '00013':
                    case '00014':
                      $parms = FSLData::startChallenge('BS-WP');
                      break;
                  }
                }
                else{
                  // For the real competition we just pick a tag at random
                  // TODO
   	          $parms = FSLData::startChallenge($stationId);
                }
	        break;
	}
	if ($rpi!=null) $rpi->start_challenge($stationType->get('delay'),$parms);
	//TODO transaction
	$station->startChallenge($team);
	$team->startChallenge($station, $parms);
	
	if ( Event::createEvent(Event::TYPE_START,$team, $station,0) ===false) {
		trace("create event failed",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "database create failed");
	}

	$msg = $team->expandMessage($stationType->get('instructions'), $parms );
	trace("message before decode $msg",__FILE__,__LINE__,__METHOD__);
	if($GLOBALS['SYSCONFIG_ENCODE'] == 1){
          // if not in student mode encode, if in student mode we only encrypt the even team numbers responses
          if($GLOBALS['SYSCONFIG_STUDENT'] == 0 or ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $teamPIN % 2 == 0)) {
            $msg = $team->encodeText($msg);
          }
        }
	json_sendObject(array('message' => $msg ) );
}

