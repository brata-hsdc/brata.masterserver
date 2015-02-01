<?php
class FSLData extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_fsl_data');
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['a_tag'] = "";
    $this->rs['a_lat'] = 0;
    $this->rs['a_lng'] = 0;
    $this->rs['b_tag'] = "";
    $this->rs['b_lat'] = 0;
    $this->rs['b_lng'] = 0;
    $this->rs['c_tag'] = "";
    $this->rs['c_lat'] = 0;
    $this->rs['c_lng'] = 0;
    $this->rs['l_lat'] = 0;
    $this->rs['l_lng'] = 0;
    $this->rs['a_rad'] = 0;
    $this->rs['b_rad'] = 0;
    $this->rs['c_rad'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

  // steps 1-3 for the 1st to third waypoint parameters
  function generateParameters($step) {
    $answer = null;
    switch($step){
      case 1:
        $answer = array("lat"=> $this->rs['lat1'], "lng" => $this->rs['lng1']);
        break;
      case 2:
        $answer = array("lat"=> $this->rs['lat2'], "lng" => $this->rs['lng2']);
        break;
      case 3:
        $answer = array("lat"=> $this->rs['lat3'], "lng" => $this->rs['lng3']);
        break;
    }
    return $answer;
  }

  // fetch the Station object for the given skey
  static function getFromTag($tag) {
  	$o = new FSLData();
  	return $o->retrieve_one("tag=?", $tag);
  }
  
  // fetch the Station object for the given skey
  static function getFromStationId($stationId) {
  	$o = new FSLData();
  	return $o->retrieve_one("stationId=?", $stationId);  // TODO not correct
  }

  // note stationId not used here
  static function startChallenge($stationId) {
    if ($GLOBALS['SYSCONFIG_STUDENT'] == 1){
        $fsl = FSLData::getFromTag($stationId);
        $parms = $fsl->generateParameters(1);
        return $parms;
    }
  	$fsl = $this->retrieveRandom();
  	return array
  	(
  	'count' => 0, // tracks which waypoint is current
  	'waypoint-lat' => $this->rs['lat1'],
  	'waypoint-lng' => $this->rs['lng1'],
  	'lat2' => $this->rs['lat2'],
  	'lng2' => $this->rs['lng2'],
  	'lat3' => $this->rs['lat3'],
  	'lng3' => $this->rs['lng3'],
  	'rad1' => $this->rs['rad1'],
  	'rad2' => $this->rs['rad2'],
  	'rad3' => $this->rs['rad3'],
  	);
  }
}
