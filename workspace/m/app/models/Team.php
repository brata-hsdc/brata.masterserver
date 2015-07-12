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
    $this->rs['fslScore0'] = 0;
    $this->rs['fslScore1'] = 0;
    $this->rs['fslScore2'] = 0;
    $this->rs['fslScore3'] = 0;
    $this->rs['hmbScore'] = 0;
    $this->rs['cpaScore'] = 0;
    
    $this->rs['regDuration'] = 0;
    $this->rs['ctsDuration'] = 0;
    $this->rs['fslDuration'] = 0;
    $this->rs['hmbDuration'] = 0;
    $this->rs['cpaDuration'] = 0;
    
    $this->rs['extDuration'] = 0;
    $this->rs['towerH'] = 0;
    $this->rs['towerD'] = 0;
    
    $this->rs['count'] = 0;
    $this->rs['started'] = 0;
    $this->rs['json'] = ""; // json string holding challenge data
    
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

  function getSchoolName() {
  	return School::getSchoolNameFromId($this->rs['schoolId']);
  }

  function getPin() {
  	return $this->rs['pin'];
  }  

  // setup the common data fields needed to start a challenge
  private function startXXXChallenge($jsonObject=null) {
  	$this->rs['count'] = 0;
  	$this->rs['started'] = time();                       // get system time
  	$this->rs['json']    = $jsonObject?json_encode($jsonObject):"";
  	return $this->update();  	
  }

  // Must be called to put the challenge data into the started state
  //  basiclly the try count is cleared the started time is set (used to calculate duration) and the
  // the station type code is needed to clear any stale challenge data when a team restarts a challenge like when their phone dies
  // option challenge data can be saved to the DB.
  function startRegChallenge($jsonObject=null) {	
    $this->set('regScore',0);
    $this->set('regDuration',0);
    return $this->startXXXChallenge($jsonObject);
  }
  function startCTSChallenge($jsonObject=null)
  {
  	$this->set('ctsScore',0);
  	$this->set('ctsDuration',0);
  	return $this->startXXXChallenge($jsonObject);
  }
  function startFSLChallenge($jsonObject=null)
  {
  	$this->set('fslScore0',0);
  	$this->set('fslScore1',0);
  	$this->set('fslScore2',0);
  	$this->set('fslScore3',0);
  	$this->set('fslDuration',0);
  	return $this->startXXXChallenge($jsonObject);
  }
  function startHMBChallenge($jsonObject=null)
  {
  	$this->set('hmbScore',0);
  	$this->set('hmbDuration',0);
  	return $this->startXXXChallenge($jsonObject);
  }
  function startCPAChallenge($jsonObject=null)
  {
  	$this->set('cpaScore',0);
  	$this->set('cpaDuration',0);
  	return $this->startXXXChallenge($jsonObject);
  }
  function startEXTChallenge($jsonObject=null) 
  {
  	$this->set('towerH',0);
  	$this->set('towerD',0);
  	$this->set('extDuration',0);
  	return $this->startXXXChallenge($jsonObject);
  }
  
  // get the json object holding the challenge state
  function getChallengeData()  {
  	return json_decode($this->rs['json'],true);
  }
  
  // set the json object holding the challenge state
  function setChallengeData($json) {
  	$this->rs['json'] = json_encode($json);
  	$this->update();  	
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
  // TODO deprecate this
  function _updateScore($stationType,$points) {
  
  	switch ($stationType->get('typeCode'))
  	{
  		case StationType::STATION_TYPE_REG:
  			return $this->updateREGScore($points);
  		case StationType::STATION_TYPE_CTS:
  			return $this->updateCTSSCore($points);
  		//case StationType::STATION_TYPE_FSL:
  		//	return $this->updateFSLScore($points);
  		case StationType::STATION_TYPE_HMB:
  			return $this->updateHMBScore($points);
  		case StationType::STATION_TYPE_CPA:
  			return $this->updateCPAScore($points);
  	}
  }
  
  // called after updateXXXScore to compute new totals and update the DB.
  // returns updated object or false on error
  // used to update totalScore/totalDuration after edit
  /*private*/ function updateTotalScore() {
  	$this->set('totalScore',$this->get('regScore')+$this->get('ctsScore')+
  			  $this->get('fslScore0')+$this->get('fslScore1')+$this->get('fslScore2')+$this->get('fslScore3')+$this->get('cpaScore'));
  	$this->set('totalDuration',$this->get('regDuration')+$this->get('ctsDuration')+$this->get('fslDuration')+$this->get('cpaDuration'));
  	return $this->update();  	
  }
  
  // update Registration portion of the score and then the totals
  function updateREGScore($points) {
    $this->set('regScore',$points);
  	$this->set('regDuration',0);
  	return $this->updateTotalScore();
  }
  
  // update the CTS portion of the score and then the totals
  function updateCTSSCore($points) {
    $this->set('ctsScore',$points);
  	$this->set('ctsDuration',time()-$this->get('started'));
  	return $this->updateTotalScore();
  }
  // update the FSL portion of the score and then the totals
  function updateFSLScore($points,$section) {
    $this->set('fslScore'.$section,$points);
  	$this->set('fslDuration',time()-$this->get('started'));
  	return $this->updateTotalScore();
  }
  
  // update the HMB portion of the score and then the totals
  function updateHMBScore($points) {
    $this->set('hmbScore',$points);
  	$this->set('regDuration',time()-$this->get('started'));
  	return $this->updateTotalScore();
  }
  
  // update the CPA portion of the score and then the totals
  function updateCPAScore($points) {
    $this->set('cpaScore',$points);
  	$this->set('cpaDuration',time()-$this->get('started'));
  	return $this->updateTotalScore();
  }
  
  // update the EXT portion of the score NOTE this is not part of the total
  function updateEXTScore($towerD,$towerH) {
  	$this->set('extDuration',time()-$this->get('started'));
  	$this->rs['towerD'] = $towerD;
  	$this->rs['towerH'] = $towerH;
  	return $this->update();
  }
  // clear all score related data
  function clearScore() {
  	$this->rs['totalScore'] = 0;
  	$this->rs['totalDuration'] = 0;
  	
  	$this->rs['regScore'] = 0;
  	$this->rs['ctsScore'] = 0;
  	$this->rs['fslScore0'] = 0;
  	$this->rs['fslScore1'] = 0;
  	$this->rs['fslScore2'] = 0;
  	$this->rs['fslScore3'] = 0;
  	$this->rs['hmbScore'] = 0;
  	$this->rs['cpaScore'] = 0;
  	
  	$this->rs['regDuration'] = 0;
  	$this->rs['ctsDuration'] = 0;
  	$this->rs['fslDuration'] = 0;
  	$this->rs['hmbDuration'] = 0;
  	$this->rs['cpaDuration'] = 0;
  	
  	//todo ext score lat,lng,height abs(height) abs(location)?
  	$this->rs['extDuration'] = 0;
  	$this->rs['towerH'] = 0;
  	$this->rs['towerD'] = 0;
  	
  	$this->rs['count'] = 0;
  	$this->rs['started'] = 0;
  	$this->rs['json'] = ""; // json string holding challenge data
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
  
  // encode the message
  // unless debug or in student server mode then encode only even pin
  function encodeText($clearText) {
  	// Not sure why but this was not working so killed for nw
        if ($this->rs['pin'] == 74449) return $clearText;  
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
