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
  	'index' => 0, // tracks which waypoint is current
  	'waypoints' => array(	
  	  array('tag' => $this->rs['a_tag'], 'lat' => $this->rs['a_lat'], 'lng' => $this->rs['a_lng']),
  	  array('tag' => $this->rs['b_tag'], 'lat' => $this->rs['b_lat'], 'lng' => $this->rs['b_lng']),
  	  array('tag' => $this->rs['c_tag'], 'lat' => $this->rs['c_lat'], 'lng' => $this->rs['c_lng']),
  	),		
  	'a_rad' => $this->rs['a_rad'],
  	'b_rad' => $this->rs['b_rad'],
  	'c_rad' => $this->rs['c_rad'],
  	'ordinal' => "first",
  	'lat' => $this->rs['a_lat'],
  	'lng' => $this->rs['a_lng'],
  	);
  }
  // test if the given id matches the id of the current waypoint
  static function isMatch(&$json, $id) {
  	//trace("json ".print_r($json,true),__FILE__,__LINE__,__METHOD__);
  	//trace("index is ".$json['index'],__FILE__,__LINE__,__METHOD__);
  	//trace("waypoints  ".print_r($json['waypoints'][$json['index']],true),__FILE__,__LINE__,__METHOD__);
  	trace("id=$id tag is ".$json['waypoints'][$json['index']]['tag'],__FILE__,__LINE__,__METHOD__);
  	return $id == $json['waypoints'][$json['index']]['tag'];
  }
  // advance to the next waypoint if possible, also update the hash so expand message will replace with the current values
  static function nextWaypoint(&$json) {
 	if ($json['index'] >= 2) return false;
 	$i = ++$json['index'];
 	$json['ordinal'] = $i == 1 ? "second" : "third";
 	$json['lat'] = $json['waypoints'][$i];
 	$json['lng'] = $json['waypoints'][$i]; 	
 	return true;
 }
  
  // fetch the Station object for the given skey
  static function getFromTag($tag) {
  	$o = new FSLData();
  	return $o->retrieve_one("tag=?", $tag);
  }
  

  // note stationId not used here
  static function startChallenge($stationId) {
  	$fsl = new FSLData();            // we need an object to call retrieveRandom 
  	$fsl = $fsl->retrieveRandom();   // now replace that object with a real ramdon object.
  	$tmp= $fsl->generateParameters();
  	trace("parms ".print_r($tmp,true),__FILE__,__LINE__,__METHOD__);
  	return $tmp;
  }
}
