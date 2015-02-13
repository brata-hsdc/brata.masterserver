<?php
// base class for all challenged data classes
class XXXData extends ModelEx {
	
	// use this to extract a named value from a brata message
	//  assume regex has one and only one capture clause a.k.a. "()"
	protected function getOneValue($regex,$msg) {
		$matches = array();
		if (preg_match($regex,$msg,$matches)==0) return false;
		return $matches[1];
	}
	
	// fetch the challenge data for this station
	protected function fetchData($stationId) {
		// implement as follows if all stations share all data 
		//$this->retrieveRandom();
		// implement as follows if the challenge data is station specific
		//$this->retrieve_one("stationId=?", $stationId);
	}
	
	// Called to generate challenge parameters from this object
	//  i.e. randomize the data compute hashes etc.
	protected function generateParameters() {
	  throw new Exception("generateParameters not implemented");
	}
	
	// implement this to start a challenge for the given team
	protected function teamStartChallenge($team, $state) {
		throw new Exception("teamStartChallenge not implemented");
		//use $team->startXXXChallenge($state);
		// where XXX is one of the challenges
	}
	// Called to start a challenge at the given station for the given teamt
	//
	// get challenge data
	// generate parameters.
	// attach challenge data to team
	// return encoded instructions
	function startChallenge($team,$station,$stationType) 
	{	
	   $this->fetchData($station->get('OID')); // polymorphic callback to derived class      
	   // putcomputed challenge parameters into a php hash which will be sent to rPI and used to populate message sent to team
       $parms = $this->generateParameters();   // polymorphic callback to derivce class 

       $rpi = null;
       if ($stationType->get('hasrPI')) {
       	 $rpi = RPI::getFromStationId($station->get('OID'));
       	 if ($rpi === false) {
       	   trace("_start_challenge can't find RPI stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
       	   throw new InternalError("can't find RPI stationTag=".$stationTag);
       	}
       	$rpi->start_challenge($stationType->get('delay'),$parms);
       }     
       
       //TODO transaction
       $station->updateTeamAtStation($team);     // with this we know which team is at this station
       //TODO fix the above FSL & EXT don't need the above
       $this->teamStartChallenge($team,$parms);  // polymorphic callback to derived class
       
       if ( Event::createEvent(Event::TYPE_START,$team, $station,0, $parms) ===false) {
       	trace("create event failed",__FILE__,__LINE__,__METHOD__);
       	rest_sendBadRequestResponse(500, "database create failed");
       }
       
       $msg = $team->expandMessage($stationType->get('instructions'), $parms );
       $msg = $team->encodeText($msg);
       return $msg;
	}
	
	
	function brataSubmit($msg,$team) {
		throw Exception("startChallenge not implemented");
		// parse message
		// test candidate answer
		// team->update(needs Station Type)  a better solution is to split updateScore by station type
		// return message expanding and encoding if needed
	}
	
	// called pro process the
	// msg is the message containing the answer from the brata framework 
	// return message or false if DB error
	function rpiSubmit($msg,$team) {
		throw Exception("startChallenge not implemented");
		// parse message
		// test candidate answer
		// team->update(needs Station Type)  a better solution is to split updateScore by station type
		// return message expanding and encoding if needed
	}
	static function factory($stationTypeCode,$OID=0)
	{
		$xxx = null;
		switch($stationTypeCode)
		{
			case StationType::STATION_TYPE_CTS:
				$xxx= new CTSData();
				break;
			case StationType::STATION_TYPE_FSL:
				$xxx = new FSLData();
				break;
			case StationType::STATION_TYPE_HMB:
				$xxx = new HMBData();
				break;
			case StationType::STATION_TYPE_CPA:
				$xxx = new CPAData();
				break;
			case StationType::STATION_TYPE_EXT:
				$xxx = new EXTData();
				break;
		}
		if ($OID >0) $xxx->retreive($OID,-1);
		return $xxx;
	}
}