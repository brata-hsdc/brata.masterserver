<?php
// base class for all challenged data classes
class XXXData extends ModelEx {
	
	//
	//  assume regex has one and only one capture clause a.k.a. "()"
	function getOneValue($regex,$msg) {
		$matches = array();
		if (preg_match($regex,$msg,$matches)==0) return false;
		return $matches[1];
	}
	
	// Called to generate challenge parameters from this object
	//  i.e. randomize the data compute hashes etc.
	function generateParameters() {
		throw Exception("generateParameters not implemented");

	}
	
	// Called at challenge to fetch challenge specific data from DB
	// OID of station on which the challenge is being performed
	//
	function startChallenge($stationId,$team) {
       throw Exception("startChallenge not implemented");
       // get challenge data
       // generate parameters.
       // attach challenge data to team
       // return encoded instructions
	}
	
	// called pro process the
	// msg is the message containing the answer from the brata framework 
	// return message or false if DB error
	function submit($msg,$team) {
		throw Exception("startChallenge not implemented");
		// parse message
		// test candidate answer
		// team->update(needs Station Type)  a better solution is to split updateScore by station type
		// return message expanding and encoding if needed
	}
}