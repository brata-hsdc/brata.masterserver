<?php

class CTSData extends XXXData {
	
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_cts_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['stationId'] = "";
    $this->rs['_1st'] = 0.0;
    $this->rs['_2nd'] = 0.0;
    $this->rs['_3rd'] = 0.0;
    $this->rs['_4th'] = 0.0;
    $this->rs['_5th'] = 0.0;
    $this->rs['tolerance'] = 0.0 ;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  //
  //  convert Pulsator tripple to array of on/off pairs
  //
  function generateParameters() {
  	$tmp = array($this->rs['_1st'], $this->rs['_2nd'], $this->rs['_3rd'],$this->rs['_4th'],$this->rs['_5th']);
  	shuffle($tmp);
        $keys = array_rand($tmp,3);
        $answer = array((int)$tmp[$keys[0]], (int)$tmp[$keys[1]], (int)$tmp[$keys[2]]);
        return $answer;
  } 
  
  // fetch the Station object for the given skey
  static function getFromStationId($stationId) {
  	$o = new CTSData();
  	return $o->retrieve_one("stationId=?", $stationId);
  }
  
  
  static function startChallenge($stationId) {
  	$cts = CTSData::getFromStationId($stationId);
  	$parms['cts_combo'] = $cts->generateParameters();
  	$parms['clue'] = CTSData::hash($parms['cts_combo']);
  	return $parms;
  }

  const XLATE="BCDGHJKLMNPQRSTVWZbcdghjkmnpqrstvwz";
             //12345678901234567890123456789012345
             //         1         2         3
  const XLATE_LNG= 35;
  
  static function hash($parms) {
  	
	(int)$h = ((($parms[0]*127) + $parms[1])*127) + $parms[2];
	$rVal="";
	for ( $i = 0; $i < 4; $i++ ) {
	  $rVal .= substr(CTSData::XLATE,$h % CTSData::XLATE_LNG,1);
	  (int)$h = $h / CTSData::XLATE_LNG;
	}
	return $rVal;
  }
}