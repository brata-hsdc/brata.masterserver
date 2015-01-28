<?php
class FSLData extends ModelEx {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_fsl_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['tag'] = "";
    $this->rs['lat1'] = 0;
    $this->rs['lng1'] = 0;
    $this->rs['lat2'] = 0;
    $this->rs['lng2'] = 0;
    $this->rs['lat3'] = 0;
    $this->rs['lng3'] = 0;    
    $this->rs['rad1'] = 0;
    $this->rs['rad2'] = 0;
    $this->rs['rad3'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  // fetch the Station object for the given skey
  static function getFromStationId($stationId) {
  	$o = new FSLData();
  	return $o->retrieve_one("stationId=?", $stationId);  // TODO not correct
  }
  
  // note stationId not used here
  static function startChallenge($stationId) {
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
