<?php
class HMBData extends ModelEx {
		
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
function generateParameters() {
//	return = array(
 //  $this->rs['_1st_on'], $this->rs['_1st_off'],
//   $this->rs['_2nd_on'], $this->rs['_2nd_off'], 
//   $this->rs['_3rd_on']  $this->rs['_3rd_off']
//   $cycle);
//
	$answer = array(1000, 2000, 1000, 4000, 1000, 16000);
	return $answer;
}
// fetch the Station object for the given key
static function getFromStationId($stationId) {
	$o = new HMBData();
	return $o->retrieve_one("stationId=?", $stationId);
}
static function startChallenge($stationId) {
	$hmb = HMBData::getFromStationId($stationId);
	$parms['hmb_vibration_pattern_ms'] = $hmb->generateParameters(); // TODO : Jaron check this code
	return $parms; // TODO : Jaron check this code
}

}
