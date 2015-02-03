<?php
class Event extends ModelEx {

	const TYPE_BAD      = 0;
	const TYPE_REGISTER = 1;
	const TYPE_START    = 2;
	const TYPE_SUBMIT   = 3;
	const TYPE_END      = 4;

	static private function isSelected($value, $selectValue) {
		return $value == $selectValue ? " selected " : "";
	}
	static function getTypesAsHtmlOptions($selectValue) {
		return
		"<option "  . Event::isSelected(Event::TYPE_BAD      , $selectValue) . "value=" . Event::TYPE_BAD    . "> Select one"
		."<option " . Event::isSelected(Event::TYPE_REGISTER , $selectValue) . "value=" . Event::TYPE_REGISTER . "> Register"
		."<option " . Event::isSelected(Event::TYPE_START    , $selectValue) . "value=" . Event::TYPE_START  . "> Start"
		."<option " . Event::isSelected(Event::TYPE_SUBMIT   , $selectValue) . "value=" . Event::TYPE_SUBMIT . "> Submit"
		."<option " . Event::isSelected(Event::TYPE_END      , $selectValue) . "value=" . Event::TYPE_END    . "> End";
	}
	
	static function getTypeAsText($value) {
		switch ($value)
		{
			case Event::TYPE_REGISTER : return "Register";
			case Event::TYPE_START    : return "Start";
			case Event::TYPE_SUBMIT   : return "Submit";
			case Event::TYPE_END      : return "End";
			default: return "Error - unknown event type";
			 	
        }	
    }	
	
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_event'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['created_dt'] = unixToMySQL(time());
    $this->rs['teamId'] = '';
    $this->rs['stationId'] = '';
    $this->rs['eventType'] = Event::TYPE_BAD;
    $this->rs['points'] = 0;
    $this->rs['data'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  static function createEvent($eventType,$team,$station,$points,$data="") {
  	if (is_array($data)) $data = json_encode($data);  // if data is an array assume its json and convert it to text
  	$o = new Event();
  	$o->set('eventType', $eventType);
  	$o->set('teamId',$team->get('OID'));
  	$o->set('stationId',$station->get('OID'));
  	$o->set('points',$points);
  	$o->set('data',$data);
  	return $o->create();
  }
  //todo recode to use team state object
  static function teamIdAtStation($stationId) {
	$dbh=getdbh();
	$stmt = $dbh->query("SELECT teamId,max(created_dt) total FROM $this->tablename where stationId=$stationId");
	return $stmt->fetchColumn();
  }
  static function countEvents($type,$teamId,$stationId) {
  	$o = new Event();
  	return $o->count("type=? and stationId=? and teamId=?", array($type,$teamId,$stationId));
  } 
}