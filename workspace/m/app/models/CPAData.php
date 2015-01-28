<?php
class CPAData extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_cpa_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['stationId'] = -1;
    $this->rs['velocity'] = 0;
    $this->rs['velocity_tolerance'] = 0;
    $this->rs['window_time'] =  0;
    $this->rs['window_time_tolerance'] = 0;
    $this->rs['pulse_width'] = 0;
    $this->rs['pulse_width_tolerance'] = 0;
    
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  function generateParameters() {
  	return array("cpa_velocity" => $this->rs['velocity'],
  			"cpa_velocity_tolerance_ms"=>$this->rs['velocity_tolerance'],
  			"cpa_window_time_ms"=>$this->rs['window_time'], 
  			"cpa_window_time_tolerance_ms"=>$this->rs['windown_time_tolerance'],
  			"cpa_pulse_width_ms"=> $this->rs['pulse_width'], 
  			"cpa_pulse_width_tolerance_ms"=>$this->rs['pulse_witch_tolerance']);
  }
  // fetch the Station object for the given key
  static function getFromStationId($stationId) {
  	$o = new CPAData();
  	return $o->retrieve_one("stationId=?", $stationId);
  }
  static function startChallenge($stationId) {
  	$cpa = CPAData::getFromStationId($stationId);
  	return $cpa->generateParameters(); 
  }
}


