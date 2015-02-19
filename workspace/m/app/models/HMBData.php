<?php
class HMBData extends XXXData {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_hmb_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['_1st_on'] = 0;
    $this->rs['_1st_off'] = 0;
    $this->rs['_2nd_on'] = 0;
    $this->rs['_2nd_off'] = 0;
    $this->rs['_3rd_on'] = 0;
    $this->rs['_3rd_off'] = 0;
    $this->rs['cycle'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }

//
//  convert Pulsator tripple to array of on/off pairs
//
protected function generateParameters() {

  	return array("hmb_vibration_pattern_ms" => 
	  array(
       $this->rs['_1st_on'] , $this->rs['_1st_off'],
        $this->rs['_2nd_on'], $this->rs['_2nd_off'], 
        $this->rs['_3rd_on'], $this->rs['_3rd_off'],
        $this->rs['cycle'])
    );

}
protected function fetchData($stationId) {
	$this->retrieveRandom();
}
// implement this to start a challenge for the given team
protected function teamStartChallenge($team, $state) {
	$team->startHMBChallenge($state);
}
protected function markTeamAtStation($team,$station) {
	//$station->updateTeamAtStation($team);
}
protected function testSolution($msg,$rPI=null) {
	$answer = $this->getOneValue("answer", $msg);
	if($answer===false){
		trace("Answer not provided in submit message.msg=".$msg,__FILE__,__LINE__,__METHOD__);
	    rest_sendBadRequestResponse(500,"The [answer=ddd] field was not provided in your message or was malformed.");
	}
	$correctAnswer = (
			((int)$this->rs['_1st_on'] + (int)$this->rs['_1st_off']) *
	        ((int)$this->rs['_2nd_on'] + (int)$this->rs['_2nd_off']) *
	        ((int)$this->rs['_3rd_on'] + (int)$this->rs['_3rd_off'])
	);
	return ($answer > $correctAnswer - $correctAnswer * 0.01 and $answer < $correctAnswer + $correctAnswer * 0.01);

}
protected function updateTeamScore($team,$points) {
	$team->updateHMBScore($points);
}
function brataSubmit($msg,$team,$station,$stationType)
{
	$isCorrect = false;
	$challengeComplete = false;

	$json = $team->getChallengeData();
	$this->rs['_1st_on']  = $json['_1st_on'];
	$this->rs['_1st_off'] = $json['_1st_off'];
	$this->rs['_2nd_on']  = $json['_2nd_on'];
	$this->rs['_2nd_off'] = $json['_2nd_off'];
	$this->rs['_3rd_on']  = $json['_3rd_on'];
	$this->rs['_3rd_off'] = $json['_3rd_off'];
	$this->rs['cycle']    = $json['cycle'];
	
	$count = $team->get('count');
	$points = 3-$count;
	$team->set('count',$count+1);
	$team->updateHMBScore(0);                   // save count 
    $isCorrect = $this->testSolution($msg);
	$challengeComplete=($count<3?false:true);

	if ($rpi!=null){
      $json = $rpi->handle_hmb_submission($stationType->get('delay'),$isCorrect, $challengeComplete);
	 }
	 else {
      trace("RPI null not allowed for HMB configuration see admin for DB integrity check.",__FILE__,__LINE__,__METHOD__);
	  rest_sendBadRequestResponse(500,"MS DB configuration is suspect as HMB requires an RPI.");
	}
	trace("count before update = ".$count);
	$team->updateScore($stationType, $points);
	
	
	if ($challenge_complete) {
		$station->endChallenge();
		$team->endChallenge();
	}

	if (Event::createEvent(Event::TYPE_SUBMIT, $team, $station,$points) === false) {
		trace("can't create event object",__FILE__,__LINE__,__METHOD__);
		throw new InternalError("Can't create event object");
	}

	if       ($isCorrect) $msg = $stationType->get('success_msg');
	else if  ($count >=3) $msg = $stationType->get('failed_msg');
	else                  $msg = $stationType->get('retry_msg');
	$msg = $team->expandMessage($msg, $parms );
	$msg = $team->encodeText($msg);
	return $msg;
}
// fetch the Station object for the given key
// depreciated
static function _getFromStationId($stationId) {
	$o = new HMBData();
	return $o->retrieve_one("stationId=?", $stationId);
}
// depreciated
static function _startChallenge($stationId) {
	$hmb = HMBData::getFromStationId($stationId);
	$parms['hmb_vibration_pattern_ms'] = $hmb->generateParameters(); // TODO : Jaron check this code
	return $parms; // TODO : Jaron check this code
}

}
