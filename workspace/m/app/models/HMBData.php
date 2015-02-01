<?php
class HMBData extends ModelEx {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_hmb_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['_1st'] = 0;
    $this->rs['_2nd'] = 0;
    $this->rs['_3rd'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

//
//  convert Pulsator tripple to array of on/off pairs
//
function generateParameters() {
//	$tmp = array($this->rs['_1st'], $this->rs['_2nd'], $this->rs['_3rd']);
//	shuffle($tmp);
//	foreach ($tmp as $i) {
//		$on = (int)($i/2);
//		$parms[] = $on;
//		$parms[] = $i-$on;
//	}
//	return $parms;

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
