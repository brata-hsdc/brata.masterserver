<?php
class HMBData extends XXXData {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_hmb_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['_1st_on'] = 0;
    $this->rs['_1st_off'] = 0;
    $this->rs['_2nd_on'] = 0;
    $this->rs['_2nd_off'] = 0;
    $this->rs['_3rd_on'] = 0;
    $this->rs['_3rd_off'] = 0;
    $this->rs['cycle'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

//
//  convert Pulsator tripple to array of on/off pairs
//
protected function generateParameters() {
//	return = array(
 //  $this->rs['_1st_on'], $this->rs['_1st_off'],
//   $this->rs['_2nd_on'], $this->rs['_2nd_off'], 
//   $this->rs['_3rd_on']  $this->rs['_3rd_off']
//   $cycle);
//
	$answer = array(1000, 2000, 1000, 4000, 1000, 16000);
	return $answer;
}
protected function fetchData($stationId) {
	$this->retrieveRandom();
}
// implement this to start a challenge for the given team
protected function teamStartChallenge($team, $state) {
	$team->startHMBChallenge($state);
}
protected function markTeamAtStation($team,$station) {
	//$station->updateTeamAtStation($team);
}
protected function testSolution($msg,$rPI=null) {
	throw new Exception("testSolution not implemented");
	$this->getOneValue("", $msg)
}
protected function updateTeamScore($team,$points) {
	$team->updateHMBScore($points);
}
// fetch the Station object for the given key
// depreciated
static function _getFromStationId($stationId) {
	$o = new HMBData();
	return $o->retrieve_one("stationId=?", $stationId);
}
// depreciated
static function _startChallenge($stationId) {
	$hmb = HMBData::getFromStationId($stationId);
	$parms['hmb_vibration_pattern_ms'] = $hmb->generateParameters(); // TODO : Jaron check this code
	return $parms; // TODO : Jaron check this code
}

}
