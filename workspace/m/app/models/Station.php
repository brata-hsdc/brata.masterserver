<?php
class Station extends ModelEx {
  
  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_station'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['typeId'] = -1;
    $this->rs['name'] = "";
    $this->rs['skey'] = "";
    $this->rs['description'] = "";  
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  // map the given typeId into its text falue
  static function getTypeAsText($typeId) {
  	$stationType = new StationType($typeId,-1);
  	return $stationType->get('shortName');
  } 
  
  // fetch the Station object for the given skey
  static function getFromKey($skey) {
  	$station = new Station();
  	return $station->retrieve_one("skey=?", $skey);
  }
}