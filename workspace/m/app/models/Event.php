<?php
class Event extends ModelEx {

	const TYPE_BAD    = 0;
	const TYPE_ARRIVE = 1;
	const TYPE_SOLUTION  = 2;
	const TYPE_LEAVE  = 3;

	static private function isSelected($value, $selectValue) {
		return $value == $selectValue ? " selected " : "";
	}
	static function getTypesAsHtmlOptions($selectValue) {
		return
		"<option "  . Event::isSelected(Event::TYPE_BAD      , $selectValue) . "value=" . Event::TYPE_BAD      . "> Select one"
		."<option " . Event::isSelected(Event::TYPE_ARRIVE   , $selectValue) . "value=" . Event::TYPE_ARRIVE   . "> Arrive"
		."<option " . Event::isSelected(Event::TYPE_SOLUTION , $selectValue) . "value=" . Event::TYPE_SOLUTION . "> Solution"
		."<option " . Event::isSelected(Event::TYPE_LEAVE    , $selectValue) . "value=" . Event::TYPE_LEAVE    . "> Leave";
	}
	
	static function getTypeAsText($value) {
		switch ($value)
		{
			case Event::TYPE_ARRIVE  : return "Arrive";
			case Event::TYPE_SOLUTION: return "Solution";
			case Event::TYPE_LEAVE   : return "Leave";
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
    $this->rs['type'] = Event::TYPE_BAD;
    $this->rs['points'] = 0;
    $this->rs['description'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
}