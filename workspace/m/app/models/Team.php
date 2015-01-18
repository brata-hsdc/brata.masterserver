<?php
class Team extends ModelEx {

  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_team'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['schoolId'] = -1;
    $this->rs['pin'] = "generated";
    $this->rs['totalScore'] = 0;
    $this->rs['totalDuration'] = 0;
    
    $this->rs['regScore'] = 0;
    $this->rs['ctsScore'] = 0;
    $this->rs['fslScore'] = 0;
    $this->rs['hmbScore'] = 0;
    $this->rs['cpaScore'] = 0;
    $this->rs['extScore'] = 0;
    
    $this->rs['regDuration'] = 0;
    $this->rs['ctsDuration'] = 0;
    $this->rs['fslDuration'] = 0;
    $this->rs['hmbDuration'] = 0;
    $this->rs['cpaDuration'] = 0;
    $this->rs['extDuration'] = 0;
    
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
  
  function updateScore($stationType,$points) {
  
  	switch ($stationType->get('typeCode'))
  	{
  		case StationType::STATION_TYPE_REG:
  			$this->set('regScore',$points);
  			break;
  		case StationType::STATION_TYPE_CTS:
  			$this->set('ctsScore',$points);
  			break;
  		case StationType::STATION_TYPE_FSL:
  			$this->set('fslScore',$points);
  			break;
  		case StationType::STATION_TYPE_HMB:
  			$this->set('hmbScore',$points);
  			break;
  		case StationType::STATION_TYPE_CPA:
  			$this->set('cpaScore',$points);
  			break;
  	}
  	$this->set('totalScore',$sc->get('totalScore')+$points);
  	return $this->update();
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