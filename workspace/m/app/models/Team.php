<?php
class Team extends ModelEx {

  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_team'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['schoolId'] = -1;
    $this->rs['pin'] = "generated";
    //$this->rs['totalPoints'] = 0;
    //$this->rs['totalDuration'] = 0;
    //$this->rs['regPoints'] = 0;
    //$this->rs['regDuration'] = 0;
    //$this->rs['ctsPoints'] = 0;
    //$this->rs['ctsDuration'] = 0;
    //$this->rs['fslPoints'] = 0;
    //$this->rs['fslDuration'] = 0;
    //$this->rs['hmbPoints'] = 0;
    //$this->rs['hmbDuration'] = 0;
    //$this->rs['cpaPoints'] = 0;
    //$this->rs['cpaDuration'] = 0;
    //$this->rs['extPoints'] = 0;
    //$this->rs['extDuration'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  function getSchoolName() {
  	return School::getSchoolNameFromId($this->rs['schoolId']);
  }
  
  // fetch the Team object for the given pin
  static function getFromPin($pin) {
  	$team = new Team();
  	return $team->retrieve_one("pin=?", $pin);
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