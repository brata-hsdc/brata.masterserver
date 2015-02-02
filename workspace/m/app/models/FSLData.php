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

  // generate the initial parameters atWaypoint will drive the game play from here on out
  function generateParameters() {
  	return array(
  	'count' => 0, // tracks which waypoint is current
  	'lat' => $this->rs['a_lat'],
  	'lng' => $this->rs['a_lng'],
  	'next_lat' => $this->rs['b_lat'],
  	'next_lng' => $this->rs['b_lng'],
  	'c_lat' => $this->rs['c_lat'],
  	'c_lng' => $this->rs['c_lng'],
  	'a_rad' => $this->rs['a_rad'],
  	'b_rad' => $this->rs['b_rad'],
  	'c_rad' => $this->rs['c_rad']);
  
  }

  // fetch the Station object for the given skey
  static function getFromTag($tag) {
  	$o = new FSLData();
  	return $o->retrieve_one("tag=?", $tag);
  }
  

  // note stationId not used here
  static function startChallenge($stationId) {

  	trace("in FLS::startC...");
  	$fsl = new FSLData();            // we need an object to call retrieveRandom 
  	$fsl = $fsl->retrieveRandom();   // now replace that object with a real ramdon object.
  	return $fsl->generateParameters();
  }
}
