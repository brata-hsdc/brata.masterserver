<?php
class EXTData extends ModelEx {
		
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
  
  // process the submit request
  // returns message for team, or false if DB error
  function submit($msg,$team,$stationType) {
  	$lat    = getOneValue("/.*tower-lat.*=.*(\d)/", $msg);
  	$lng    = getOneValue("/.*tower-lon.*=.*(\d)/`", $msg);
  	$height = getOneValue("/.*tower-height.*=*.(\d)/", $msg);

  	if ($lat === false || $lng === false || $height === false) $msg = $stationType->get('failed_msg');
  	else                                                       $msg = $stationType->get('success_msg');
  	
  	$towerH = abs($this->rs['height']-$height);
  	$towerD = sqrt(pow($this->rs['t_lat']-$lat,2)+pow($this->rs['t_lng']-$lng,2));
  	if ($team->updateExtScore($towerD,$towerH) === false) return false;
  	return $team->encodeText($msg);
  }
}
