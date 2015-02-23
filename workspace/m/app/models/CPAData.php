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
  
  
  //protected function generateParameters() {
    // we have a problem as ideally this would be get from the team json object
  //}

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
  public function getItemsToMeasure() {
        $this->retrieveRandom();   // now replace that object with a real ramdon object.
	// We are to randomly select a time between 2-6 seconds for the time
	// the fence distance is traversed, and apply same to the building
	$fence_time = rand(2000, 6000);
        $building_time = (int)((float)$fence_time * (float)$this->rs['building'] / (float)$this->rs['fence']);
  	return array("cpa_velocity" => $fence_time,
  			"cpa_velocity_tolerance_ms"=>1000,
  			"cpa_window_time_ms"=>$fence_time+$building_time, 
  			"cpa_window_time_tolerance_ms"=> 400,
  			"cpa_pulse_width_ms"=> 100, 
  			"cpa_pulse_width_tolerance_ms"=> 75,
  			"fence"=>$this->rs['fence'], 
  			"building"=>$this->rs['building'],
                        "label"=>$this->rs['label']);
  }
}


