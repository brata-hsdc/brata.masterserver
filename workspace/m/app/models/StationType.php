<?php
class StationType extends ModelEx {

 const STATION_TYPE_BAD = -1;
 const STATION_TYPE_REG = 0;
 const STATION_TYPE_CTS = 1;
 const STATION_TYPE_FSL = 2;
 const STATION_TYPE_HMB = 3;
 const STATION_TYPE_CPA = 4;
 const STATION_TYPE_EXT = 5;
  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_stationtype'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['typeCode'] = StationType::STATION_TYPE_BAD;
    $this->rs['name'] = '';
    $this->rs['hasrPI'] = false;
    $this->rs['delay'] = 60;
    $this->rs['instructions'] = "todo - instructions";
    $this->rs['success_msg'] = "todo - success message";
    $this->rs['failed_msg'] = "todo - failed message";
    $this->rs['retry_msg'] = "todo - retry message";
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
 
  // helper for resetdb
  static function makeStationType($typeCode,$name,$hasrPI,$delay,$instructions,$success_msg,$failed_msg,$retry_msg)
  {
  	$o = new StationType();
  	$o->set('typeCode'    , $typeCode);
  	$o->set('name'        , $name);
  	$o->set('hasrPI'      , $hasrPI);
  	$o->set('delay'       , $delay);
  	$o->set('instructions', $instructions);
  	$o->set('success_msg' , $success_msg);
  	$o->set('failed_msg'  , $failed_msg);
  	$o->set('retry_msg'   , $retry_msg);
  	return $o->create();  	
  }
 
// return the StationType object for the given "short" name 
  static function getFromTypeCode($typeCode) {
    $type = new StationType();
    return $type->retrieve_one("typeCode=?", array($typeCode));
  }
  
  static function getAllAsHTMLOptions($oid=-1) {
    $type = new StationType();
    $aray = $type->retrieve_many();
    $options ="";
    foreach ($aray as $item) {
      $selected = $item->get('OID') == $oid ? "selected" : "";
      $options .= '<option value='. $item->get('OID'). ' ' . $selected . '>' . $item->get("name");
    }
    return $options;
  }
}
  