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
  
  // Must be called to put the challenge data into the started state
  //  basiclly the try count is cleared the started time is set (used to calculate duration) and the
  // the station type code is needed to clear any stale challenge data when a team restarts a challenge like when their phone dies
  // option challenge data can be saved to the DB.
  function startChallenge($station,$stationTypeCode,$jsonObject=null) {
  	
  	$this->rs['count'] = 0;
  	$this->rs['started'] = time();                       // get system time 
  	$this->rs['json']    = $jsonObject?json_encode($jsonObject):"";

  	switch ($stationTypeCode)
  	{
  	  case StationType::STATION_TYPE_REG:
  		$this->set('regScore',0);
  		$this->set('regDuration',0);
  		break;
  	  case StationType::STATION_TYPE_CTS:
  		$this->set('ctsScore',0);
  		$this->set('regDuration',0);
  		break;
  	  case StationType::STATION_TYPE_FSL:
  		$this->set('fslScore',0);
  		$this->set('regDuration',0);
  		break;
  	  case StationType::STATION_TYPE_HMB:
  		$this->set('hmbScore',0);
  		$this->set('regDuration',0);
  		break;
  	  case StationType::STATION_TYPE_CPA:
  		$this->set('cpaScore',0);
  		$this->set('regDuration',0);
  		break;
  	}
  	return $this->update();
  }
  
  // under development
  function getChallengeData()  {
  	return json_decode($this->rs['json'],true);
  }
  function setChallengeData($json) {
  	$this->rs['json'] = json_encode($json);
  }
  
  // must be called at end of challenge to clear challenge state
  function endChallenge() {
  	$this->rs['count'] = 0;
  	$this->rs['started'] = 0;
  	$this->rs['json']    = '';
  	return $this->update();  	
  }
  // Must be called to update team's score, this method is designed to be called 
  // after every submit.  The last call will be the final score.  This allows the leader board
  // to dyamiclly converge to the final score (duration goes up, points go down) with each submit.
  function updateScore($stationType,$points) {
  
  	$duration = time()-$this->get('started');
  	switch ($stationType->get('typeCode'))
  	{
  		case StationType::STATION_TYPE_REG:
  			$this->set('regScore',$points);
  			$this->set('regDuration',0);
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
  
  // table assoc array field the field name holding the message to expand
  // the assumption is that the labels in the message the "[label]" will match
  // the keys in the given hash $table.
  // WARNING: Doesn't seem to work if the table holds nested arrays.
  
  function expandMessage($msg,$table=null) {
  	if ($table == null)  $table=array("team"=>$this->get('name'));
  	else                 $table['team'] = $this->get('name');   // add team name
  	foreach ($table as $key => $value) {
  		if (is_array($value)) $value = print_r($value,true); // convert to a string
  		$msg = str_replace("[$key]", $value, $msg);
  	}
  	return $msg;
  }

  static function makePrimes($n) {
  	/* Return a list of between 2 and n (inclusive) prime numbers.
  	  
  	    Create a list of the prime numbers between 2 and n inclusive. The
  	    method used is a essentially the "Sieve of Eratosthenes" whereby the
  	    initial prime number 2 is seeded. Thereafter, if the next candidate
  	    integer can not be evenly divided by any prime number already in the
  	    list, then the candidate is found to be prime and added to the list.
  	    */
  	 $pList = array();
  	 $_range =range(2, $n + 1,1);
  	 foreach ($_range as $i) { 
  	    $isPrime = true;
  	    foreach ($pList as $t) {
  	    	if (($i % $t) == 0) {
  	    		$isPrime = false;
  	    		break;
  	    	}
  	    }
  	    if ($isPrime) {
  	    	$pList[] = $i;
  	    }
  	 }
  	 return $pList;
  }

  static function getPrimeFactors($n) {
  	if (!isset($GLOBALS['primes'])) $GLOBALS['primes'] = Team::makePrimes(500);
  	$fList = array();
  	foreach($GLOBALS['primes'] as $t) {
  		if (($n % $t) == 0) {
  			$fList[] = $t;
  			if (floor($n/$t) < $t) break;
  		}
  	}
  	$c = count($fList);
  	return $fList;
  }
  static function getEncodingParameters($text) {
  	$lng = strlen($text);
  	$augment = 0;
  	while(true) {
  		if ($lng >= 255) { // fail safe
  			return array($text,null);
  		}
  	  $factors = Team::getPrimeFactors($lng);
  	  if (count($factors) == 2 and ($factors[0] * $factors[1] == $lng)){
  	  	break;
  	  }
  	  else {
  	  	$lng += 1;
  	    $augment += 1;
  	  }
  	}
  	$text = $text . str_repeat("~", $augment);
  	return array($text,$factors);
  }
  function encodeText($clearText) {
  	$clearText = strtr($clearText,' ',"_");
  	list($clearText,$factors) = Team::getEncodingParameters($clearText);
  	if ($factors == null ) { // fail safe
  		return $clearText;
  	}
  	$cipherText = array();
  	foreach (range(0,$factors[1]-1) as $j) {
  		foreach(range(0,$factors[0]-1) as $k) {
  			$cipherText[] = ($clearText[$k * $factors[1] + $j]);
  		}
  	}
  	return implode($cipherText);
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