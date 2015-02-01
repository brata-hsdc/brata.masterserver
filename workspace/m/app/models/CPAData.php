<?php
class CPAData extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_cpa_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['label'] = 0;
    $this->rs['fence'] = 0;
    $this->rs['building'] =  0;
    $this->rs['sum'] = 0;
    
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  function generateParameters() {
  	return array(
  			"which"=> $this->rs['which'],
  			"fence"=> $this->rs['fence'], 
  			"building"=>$this->rs['building'],
  			"sum" => $this->rs['sum']
  	);
  }
  // fetch the Station object for the given key
  static function getFromStationId($stationId) {
  	$o = new CPAData();
  	return $o->retrieve_one("stationId=?", $stationId);
  }
  static function startChallenge($stationId) {
  	$cpa = CPAData::getFromStationId($stationId);
  	return $cpa->generateParameters();
  }
  static function getItemsToMeasure($stationId) {
  	$cpa = CPAData::getFromStationId($stationId);
  	return $cpa->generateParameters();
  }
}


