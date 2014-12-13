<?php
class Team extends ModelEx {

  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_team'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['schoolId'] = -1;
    $this->rs['pin'] = "00000";
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  function getSchoolName() {
  	return School::getSchoolNameFromId($this->rs['schoolId']);
  }
  
  // fetch the Team object for the given pin
  static function getFromPin($pin) {
  	$team = new Team();
  	return $team->retrieve_one("pin='?'", $pin);
  }
  
  static function getNameFromId($id) {
    $team = new Team($id,-1);
    return $team->get('name');
  }
  
  
  // generate a random pin of the given length, with the last digit a check digit
  static function generatePIN($length=5) {
    
  	$validchars = "0123456789";
  
  	$pin  = "";
  	$counter   = 0;
  	$sum = 0;
  
  	while ($counter < $length-1) {
  		$atChar = substr($validchars, mt_rand(0, strlen($validchars)-1), 1);
  	    $pin .= $atChar;
  		$sum = ($sum + (int)$atChar)%10;  // check digit mod 10
  		$counter++;
  	}
  	return $pin.$sum;
  }
  // for brata testing only
  static function getAllAsHTMLOptions($itemPIN=-1) {
  	$object = new Team();
  	$aray = $object->retrieve_many();
  	$options ="";
  	foreach ($aray as $item) {
  		$selected = $item->rs['pin'] == $itemPIN ? "selected" : "";
  		$options .= '<option value='. $item->rs['pin']. ' ' . $selected . '>' . $item->get('pin')." - ".$item->get("name");
  	}
  	return $options;
  }
}