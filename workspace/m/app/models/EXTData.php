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
  
  
  static function startChallenge($stationId) {
  	$ext = EXTData(1,-1);  // there is only one record
  	return array(
  	'a_lat' =>   $this->rs['a_lat'],
    'a_lng' => $this->rs['a_lng'],
    'b_lat' => $this->rs['b_lat'],
    'b_lng' => $this->rs['b_lng'],
    'c_lat' => $this->rs['c_lat'],
    'c_lng' => $this->rs['c_lng']
  	);
  }
}
