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
    $this->rs['longName'] = '';
    $this->rs['delay'] = 60;
    $this->rs['instructions'] = "todo";
    $this->rs['correct_msg'] = "todo";
    $this->rs['incorrect_msg'] = "todo";
    $this->rs['failed_msg'] = "todo";
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

// return the StationType object for the given "short" name 
  static function getFromTypeCode($typeCode) {
    $type = new StationType();
    return $type->retrieve_one("typeCode = ?", $typeCode);
  }
  
  static function getAllAsHTMLOptions($oid=-1) {
    $type = new StationType();
    $aray = $type->retrieve_many();
    $options ="";
    foreach ($aray as $item) {
      $selected = $item->get('OID') == $oid ? "selected" : "";
      $options .= '<option value='. $item->get('OID'). ' ' . $selected . '>' . $item->get("longName");
    }
    return $options;
  }
  

  static function getAllOrderByName() {
    $item = new StationType();
    return $item->retrieve_many("OID !=0 order by longName");

  }}