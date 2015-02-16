<?php
class EXTData extends XXXData {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_ext_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['a_lat'] = 0;
    $this->rs['a_lng'] = 0;
    $this->rs['b_lat'] = 0;
    $this->rs['b_lng'] = 0;
    $this->rs['c_lat'] = 0;
    $this->rs['c_lng'] = 0;
    $this->rs['t_lat'] = 0;
    $this->rs['t_lng'] = 0;
    $this->rs['height'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  // depreciated
  static function _startChallenge($stationId) {
  	$ext = new EXTData(1,-1);  // there is only one record
  	return array(
  	'a_lat' => $ext->rs['a_lat'],
    'a_lng' => $ext->rs['a_lng'],
    'b_lat' => $ext->rs['b_lat'],
    'b_lng' => $ext->rs['b_lng'],
    'c_lat' => $ext->rs['c_lat'],
    'c_lng' => $ext->rs['c_lng'],
  	't_lat' => $ext->rs['t_lat'],
  	't_lng' => $ext->rs['t_lng'],
  	'height' => $ext->rs['height']
  	);
  }
  
  // fetch the challenge data for this station
  protected function fetchData($stationId) {
  	$this->retrieve(1,-1);
  }
  
  // Called to generate challenge parameters from this object
  //  i.e. randomize the data compute hashes etc.
  protected function generateParameters() {
  	return array(
  			'a_lat' => $this->rs['a_lat'],
  			'a_lng' => $this->rs['a_lng'],
  			'b_lat' => $this->rs['b_lat'],
  			'b_lng' => $this->rs['b_lng'],
  			'c_lat' => $this->rs['c_lat'],
  			'c_lng' => $this->rs['c_lng'],
  			't_lat' => $this->rs['t_lat'],
  			't_lng' => $this->rs['t_lng'],
  			'height' => $this->rs['height']
  	);
  }
  // implement this to start a challenge for the given team
  protected function teamStartChallenge($team, $state) {
  	$team->startEXTChallenge($state);
  }
  
  // process the submit request
  // returns message for team, or false if DB error
  function brataSubmit($msg,$team,$station,$stationType) {
  	$lat    = getOneValue("tower-lat", $msg);
  	$lng    = getOneValue("tower-lon", $msg);
  	$height = getOneValue("tower-height", $msg);

  	if ($lat === false || $lng === false || $height === false) $msg = $stationType->get('failed_msg');
  	else                                                       $msg = $stationType->get('success_msg');
  	
  	$towerH = abs($this->rs['height']-$height);
  	$towerD = sqrt(pow($this->rs['t_lat']-$lat,2)+pow($this->rs['t_lng']-$lng,2));
  	if ($team->updateEXTScore($towerD,$towerH) === false) {
  		trace("Team::updateEXTScore failed for team".$team->get('name'));
  		throw new InternalError("Team::updateEXTScore failed for team".$team->get('name'));
  	}
  	return $team->encodeText($msg);
  }
  protected function updateTeamScore($team,$points) {
  	$team->updateEXTScore($points);
  }
}
