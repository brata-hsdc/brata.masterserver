<?php
// base class for all challenged data classes
class XXXData extends ModelEx {
	
	// use this to extract a named value from a brata message
	//  assume regex has one and only one capture clause a.k.a. "()"
	protected function getOneValueEx($regex,$msg) {
		$matches = array();
		if (preg_match($regex,$msg,$matches)==0) return false;
		return $matches[1];
	}
	// use this to extract a named value from a brata message
	//  assume regex has one and only one capture clause a.k.a. "()"
	protected function getOneValue($keyword,$msg) {
		return getOneFloatValue($keyword,$msg);
	}
	// use this to extract a named value from a brata message
	//  assume regex has one and only one capture clause a.k.a. "()"
	protected function getOneIntValue($keyword,$msg) {
		$matches = array();
		if (preg_match("/.*$keyword.*=.*(\d+)/",$msg,$matches)==0) return false;
		return $matches[1];
	}	
	// use this to extract a named value from a brata message
	//  assume regex has one and only one capture clause a.k.a. "()"
	protected function getOneFloatValue($keyword,$msg) {
		$matches = array();
		if (preg_match("/.*$keyword.*=.*(-?\d*\.?\d*)/",$msg,$matches)==0) return false;
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
	// implment this when there are multiple stations
	protected function markTeamAtStation($team,$station) {
		//$station->updateTeamAtStation($team);
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
       $this->markTeamAtStation($team, $station); // polymorphic callback so we know which team is at this station
       $this->teamStartChallenge($team,$parms);  // polymorphic callback to derived class
       
       if ( Event::createEvent(Event::TYPE_START,$team, $station,0, $parms) ===false) {
       	trace("create event failed",__FILE__,__LINE__,__METHOD__);
       	rest_sendBadRequestResponse(500, "database create failed");
       }
       
       $msg = $team->expandMessage($stationType->get('instructions'), $parms );
       $msg = $team->encodeText($msg);
       return $msg;
	}
	
    // implement this to test if the team's solution is correct
    // $msg is a text string holding the team's solution, 
    // return true or false
	protected function testBrataSolution($msg) {
		throw new Exception("testSolution not implemented");
	}
	// implement this to test if the team's solution is correct
	// $msg is a text string holding the team's solution,
	// $rPI is the rPI running the challenge or null if here is no rPI at this station
	// return true or false
	protected function testRpiSolution($msg) {
		throw new Exception("testSolution not implemented");	  //=====
	  // CPA and CTS are handled the same way.
	  	$stationjson = $team->getChallengeData();
	  	trace("stored station data = ".json_encode($stationjson));
	  	json_checkMembers("is_correct", $stationjson);
	  	trace("after check of stored station data ");
	  	$isCorrect = $stationjson['is_correct'];
	  	if ($isCorrect){
	  		// success
	  		$challengeComplete=true;
	  		$isCorrect = true;
	  	}
	  	else {
	  		$challengeComplete=($count<3?false:true);
	  		$isCorrect = false;
	  	}
	}
	// implment this to update the teams score (points and duration)
	protected function updateTeamScore($team,$points) {
		throw new Exception("updateTeamScore not implemented");
		//use $team->updateXXXScore($state);
		// where XXX is one of the challenges
	}
	// parse message
	// test candidate answer
	// team->update(needs Station Type)  a better solution is to split updateScore by station type
	// return message expanding and encoding if needed
	function brataSubmit($msg,$team,$station,$stationType) 
	{
	  $isCorrect = false;
	  $challengeComplete = false;

	  $rpi = null;
	  if ($stationType->get('hasrPI')) {
	    $rpi = RPI::getFromStationId($station->get('OID'));
	   	if ($rpi === false) {
	   	  trace("_start_challenge can't find RPI stationTag=".$stationTag,__FILE__,__LINE__,__METHOD__);
	   	  throw new InternalError("can't find RPI stationTag=".$stationTag);
	    }
	  }
      $count = $team->get('count');
      $team->set('count',$count+1);
      $points = 3-$count;
      $this->updateTeamScore($team, $points);  // save count
		
	  $isCorrect = $this->testRpiSolution($team->getChallengeData());
	  
	  if (!$isCorrect) {
		$challenge_complete=($count<3?false:true);
	  }
	  else {
	    $challenge_complete=true;
	  }
		
	  if ($challenge_complete) {
        $station->endChallenge();
		$team->endChallenge();
	  }
		
	  if (Event::createEvent(Event::TYPE_SUBMIT, $team, $station,$points) === false) {
	    trace("can't create event object",__FILE__,__LINE__,__METHOD__);
		throw new InternalError("Can't create event object");
	  }
		
	  if       ($isCorrect) $msg = $stationType->get('success_msg');
	  else if  ($count >=3) $msg = $stationType->get('failed_msg');
	  else                  $msg = $stationType->get('retry_msg');
	  $msg = $team->expandMessage($msg, $parms );		
	  $msg = $team->encodeText($msg);
	  return $msg;
	}
	
	// called pro process the
	// msg is the message containing the answer from the brata framework 
	// return message or false if DB error
	function rpiSubmit($msg,$team) {
		throw new Exception("startChallenge not implemented");
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