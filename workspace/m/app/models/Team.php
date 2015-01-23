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
    
    $this->rs['count'] = 0;
    $this->rs['started'] = 0;
    $this->rs['json'] = ""; // json string holding challenge data
    
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  function getSchoolName() {
  	return School::getSchoolNameFromId($this->rs['schoolId']);
  }
  
  // under development
  function startChallenge($station,$jsonObject) {
  	
  	$this->rs['count'] = 0;
  	$this->rs['started'] = time();                       // get system time 
  	$this->rs['json']    = json_encode($jsonObject);
  	return $this->update();
  }
  
  // under development
  function getChallengeData()  {
  	return json_decode($this->rs['json']);
  }
  
  // under development
  function endChallenge() {
  	$this->rs['count'] = 0;
  	$this->rs['started'] = 0;                       // get system time
  	$this->rs['json']    = '';
  	return $this->update();  	
  }
  // under development
  function updateScore($stationType,$points) {
  
  	$duration = time()-$this->get('started');
  	switch ($stationType->get('typeCode'))
  	{
  		case StationType::STATION_TYPE_REG:
  			$this->set('regScore',$points);
  			$this->set('regDuration',$duration);
  			break;
  		case StationType::STATION_TYPE_CTS:
  			$this->set('ctsScore',$points);
  			$this->set('regDuration',$duration);
  			break;
  		case StationType::STATION_TYPE_FSL:
  			$this->set('fslScore',$points);
  			$this->set('regDuration',$duration);
  			break;
  		case StationType::STATION_TYPE_HMB:
  			$this->set('hmbScore',$points);
  			$this->set('regDuration',$duration);
  			break;
  		case StationType::STATION_TYPE_CPA:
  			$this->set('cpaScore',$points);
  			$this->set('regDuration',$duration);
  			break;
  	}
  	$this->set('totalScore',$this->get('regScore')+$this->get('ctsScore')+$this->get('fslScore')+$this->get('cpaScore'));
  	$this->set('totalDuration',$this->get('regDuration')+$this->get('ctsDuration')+$this->get('fslDuration')+$this->get('cpaDuration'));
  	return $this->update();
  }
  // todo is this the best place?
  // table assoc array field the field name holding the message to expand
  function expandMessage($msg,$table) {
  	if ($table == null)  $table=array("team"=>$this->get('name'));
  	else                 $table['team'] = $this->get('name');   // add team name
  	foreach ($table as $key => $value) {
  		$msg = str_replace("[$key]", $value, $msg);
  	}
  	return $msg;
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