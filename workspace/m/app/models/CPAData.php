<?php
class CPAData extends XXXData {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_cpa_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['label'] = 0;
    $this->rs['fence'] = 0;
    $this->rs['building'] =  0;
    $this->rs['sum'] = 0;
    
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  
  protected function generateParameters() {
  	$tmp =  array(
  			"label"=> $this->rs['label'],
  			"fence"=> $this->rs['fence'], 
  			"building"=>$this->rs['building'],
  			"sum" => $this->rs['sum']
  	);
  	return array("cpa_velocity" => $this->rs['velocity'],
  			"cpa_velocity_tolerance_ms"=>$this->rs['velocity_tolerance'],
  			"cpa_window_time_ms"=>$this->rs['window_time'], 
  			"cpa_window_time_tolerance_ms"=>$this->rs['window_time_tolerance'],
  			"cpa_pulse_width_ms"=> $this->rs['pulse_width'], 
  			"cpa_pulse_width_tolerance_ms"=>$this->rs['pulse_width_tolerance'],
  			"fence"=> $this->rs['fence'], 
  			"building"=>$this->rs['building']);

  }
  // all stations share data pool stationId ignored
  protected function fetchData($stationId) {
  	$this->retrieveRandom();  	
  }

  // implement this to put the given team
  protected function teamStartChallenge($team, $state) {
  	return $team->startCPAChallenge($state);
  }
  protected function markTeamAtStation($team,$station) {
  	$station->updateTeamAtStation($team);
  }
  
  protected function updateTeamScore($team,$points) {
  	$team->updateCPAScore($points);
  }
  // fetch the Station object for the given key
  // depreciated
  static function _getFromStationId($stationId) {
  	$o = new CPAData();
  	return $o->retrieve_one("stationId=?", $stationId);
  }
  
  // depreciated
  static function _startChallenge($stationId) {
  	$cpa = CPAData::getFromStationId($stationId); // WARNING BUG HERE CPA data is not unique to station
  	return $cpa->generateParameters();
  }
  static function getItemsToMeasure($stationId) {
  	$cpa = CPAData::getFromStationId($stationId);
  	return $cpa->generateParameters();
  }
}


