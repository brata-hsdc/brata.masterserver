<?php
class FSLData extends XXXData {

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
    $this->rs['l_tag'] = 0;
    $this->rs['l_lat'] = 0;
    $this->rs['l_lng'] = 0;
    $this->rs['a_rad'] = 0;
    $this->rs['b_rad'] = 0;
    $this->rs['c_rad'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

  // test if the given id matches the id of the current waypoint
  static function isMatch(&$json, $id) {
  	return $id == $json['waypoints'][$json['index']]['tag'];
  }
  // advance to the next waypoint if possible, also update the hash so expand message will replace with the current values
  // false means challenge complete
  static function nextWaypoint(&$json) {
  	if ($json['index'] == 3) return false;
  	$i = ++$json['index'];
 	if ($json['index'] == 3) {
 		$json['msg_values'] = array('a_rad' => $json['waypoints'][$i]['a_rad'],  // replace the old hash wih a whole new one
 		                            'b_rad' => $json['waypoints'][$i]['b_rad'],
 		                            'c_rad' => $json['waypoints'][$i]['c_rad']);
 		return false;
 	}
 	$json['msg_values']['ordinal'] = $i == 1 ? "second" : "third";   // update the hash
 	$json['msg_values']['lat'] = $json['waypoints'][$i]['lat'];
 	$json['msg_values']['lng'] = $json['waypoints'][$i]['lng']; 
 	return true;
 }
  
 // return true if looking for the lab
 static function atLab(&$json) {
 	return $json['index'] == 3 ? true : false;
 }
 // update score after each try
 // NOTE: you must also call the team update score after each try 
 static function updateScore(&$json,$points) {
 	$json['waypoints'][$json['index']]['score'] = $points;
 	$json ['totalScore'] = 0;
 	for($i=0;$i<count($json['waypoints']);$i++) {
 	  $json['totalScore'] += $json['waypoints'][$i]['score'] ;
 	}
 	return $json['totalScore'];
 }
  // fetch the Station object for the given skey
  static function getFromTag($tag) {
  	$o = new FSLData();
  	return $o->retrieve_one("tag=?", $tag);
  }
  
  // note stationId not used here
  protected function fetchData($stationId) {
  	$this->retrieveRandom();   // now replace that object with a real ramdon object.
  	$tmp= $fsl->generateParameters();
  	trace("parms ".print_r($tmp,true),__FILE__,__LINE__,__METHOD__);
  	return $tmp;
  }
  // generate the initial parameters atWaypoint will drive the game play from here on out
  protected function generateParameters() {
  	$tmp = array(
  			'totalScore' => 0,
  			'index' => 0,      // tracks which waypoint is current
  			'waypoints' => array(
  					array('score' => 0, 'tag' => $this->rs['a_tag'], 'lat' => $this->rs['a_lat'], 'lng' => $this->rs['a_lng']),
  					array('score' => 0, 'tag' => $this->rs['b_tag'], 'lat' => $this->rs['b_lat'], 'lng' => $this->rs['b_lng']),
  					array('score' => 0, 'tag' => $this->rs['c_tag'], 'lat' => $this->rs['c_lat'], 'lng' => $this->rs['c_lng']),
  					array('score' => 0, 'tag' => $this->rs['l_tag'],  'a_rad' => $this->rs['a_rad'], 'b_rad' => $this->rs['b_rad'], 'c_rad' => $this->rs['c_rad'])
  			),
  			'msg_values' => array(     // used to expand messages which will be sent to teams
  					'ordinal' => "first",
  					'lat' => $this->rs['a_lat'],
  					'lng' => $this->rs['a_lng']
  			)
  	);
  	return $tmp;
  }  
  function startChallenge($team,$station,$stationType)
  {
  	$this->retrieveRandom();   // now replace that object with a real ramdon object.
  	$state= $this->generateParameters();
  	trace("state ".print_r($state,true),__FILE__,__LINE__,__METHOD__);
  	$team->startChallenge($parms,$stationType->get('typeCode'),$state);  // $state
  	
  	if ( Event::createEvent(Event::TYPE_START,$team, $station,0, $state) ===false) {
  		trace("create event failed",__FILE__,__LINE__,__METHOD__);
  		rest_sendBadRequestResponse(500, "database create failed");
  	}
  	
  	$msg = $team->expandMessage($stationType->get('instructions'), $parms );
  	if($GLOBALS['SYSCONFIG_ENCODE'] == 1){
  		// if not in student mode encode, if in student mode we only encrypt the even team numbers responses
  		if($GLOBALS['SYSCONFIG_STUDENT'] == 0 or ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $teamPIN % 2 == 0)) {
  			$msg = $team->encodeText($msg);
  		}
  	}
  	 
  }
  
  // note stationId not used here
  // depreciated
  static function _startChallenge($stationId) {
  	$fsl = new FSLData();            // we need an object to call retrieveRandom 
  	$fsl = $fsl->retrieveRandom();   // now replace that object with a real ramdon object.
  	$tmp= $fsl->generateParameters();
  	trace("parms ".print_r($tmp,true),__FILE__,__LINE__,__METHOD__);
  	return $tmp;
  }
}
