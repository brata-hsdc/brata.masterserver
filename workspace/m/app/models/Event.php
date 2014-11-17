<?php
class Event extends ModelEx {

	const TYPE_BAD     = 0;
	const TYPE_START   = 1;
	const TYPE_SUBMIT  = 2;
	const TYPE_END     = 3;

	static private function isSelected($value, $selectValue) {
		return $value == $selectValue ? " selected " : "";
	}
	static function getTypesAsHtmlOptions($selectValue) {
		return
		"<option "  . Event::isSelected(Event::TYPE_BAD    , $selectValue) . "value=" . Event::TYPE_BAD    . "> Select one"
		."<option " . Event::isSelected(Event::TYPE_START  , $selectValue) . "value=" . Event::TYPE_START  . "> Start"
		."<option " . Event::isSelected(Event::TYPE_SUBMIT , $selectValue) . "value=" . Event::TYPE_SUBMIT . "> Submit"
		."<option " . Event::isSelected(Event::TYPE_END    , $selectValue) . "value=" . Event::TYPE_END    . "> End";
	}
	
	static function getTypeAsText($value) {
		switch ($value)
		{
			case Event::TYPE_START  : return "Start";
			case Event::TYPE_SUBMIT : return "Submit";
			case Event::TYPE_END    : return "End";
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
  
  static function makeEvent($type,$teamId,$stationId,$points=0,$description="") {
  	$o = new Event();
  	$o->set('type', $type);
  	$o->set('teamId',$teamId);
  	$o->set('stationId',$stationId);
  	$o->set('points',$points);
  	$o->set('description',$description);
  	return $o;
  } 
}