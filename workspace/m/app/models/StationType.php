<?php
class StationType extends ModelEx {

  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_stationtype'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['longName'] = '';
    $this->rs['shortName'] = '';
    $this->rs['delay'] = 60;
    $this->rs['instructions'] = "todo";
    $this->rs['correct_msg'] = "todo";
    $this->rs['incorrect_msg'] = "todo";
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

// return the StationType object for the given "short" name 
  static function getFromShortname($shortName) {
    $type = new StationType();
    return $type->retrieve_one("shortName = ?", $shortName);
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