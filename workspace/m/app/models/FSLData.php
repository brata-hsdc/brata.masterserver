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
  
  
  static function startChallenge($tag) {
  	$fsl = FSLData::getFromTag($tag);
  	$parms = $fsl->generateParameters(1);
  	return $parms;
  }
}
