<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
// stationTag is stationId in ICD
function _start_challenge($stationTag=null) 
{
	if ($stationTag === null) {
		rest_sendBadRequestResponse(400,"missing stationId");  // doesn't return
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
	$parms = null; // todo compute challenge parameters
	switch($stationType->get('typeCode'))
	{
		case StationType::STATION_TYPE_CTS:
			$parms = CTSData::startChallenge($stationId);
	        break;
	    case StationType::STATION_TYPE_CPA:
	        	$parms =array("cpa_velocity" => 6000, "cpa_velocity_tolerance_ms"=>0,
	        	"cpa_window_time_ms"=>8000, "cpa_window_time_tolerance_ms"=>100,
	        	"cpa_pulse_width_ms"=>10, "cpa_pulse_width_tolerance_ms"=>20);
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

	json_sendObject(array('message' => $team->expandMessage($stationType->get('instructions'), $parms ) ) );
}

