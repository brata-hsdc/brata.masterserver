<?php
class School extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_school'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['mascot'] = '';
    $this->rs['logo'] = NULL;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  static function getNameFromId($oid) {
    $item = new School($oid,-1);
    return $item->get('name');
  }
  static function getFromName($name) {
  	$item = new School();
  	return $item->retrieve_one("name=?", $name);
  }
  
  
  static function getAllAsHTMLOptions($itemId=-1) {
    $school = new School();
    $aray = $school->retrieve_many();
    $options ="";
    foreach ($aray as $item) {
      $itemOID = $item->get('OID');
      $selected = $item->rs['OID'] == $itemId ? "selected" : "";
      $options .= '<option value='. $itemOID. ' ' . $selected . '>' . $item->get("name");
    }
    return $options;
  }
  
  static function getAllOrderByName() {
    $item = new Station();
    return $item->retrieve_many("OID !=0 order by name");

  }
}