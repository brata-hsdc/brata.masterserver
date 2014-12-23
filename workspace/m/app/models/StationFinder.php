<?php
class StationFinder extends Model {
	
	function __construct($tag=null) {
		parent::__construct('tag','v_stationfinder');
		$this->rs['tag'] = "";
		$this->rs['stationId'] = "";
		$this->rs['hasrPI'] = "";
		$this->rs['URL'] = "";
		$this->rs['typeId'] = "";
		$this->rs['typeName'] = "";
		trace("tag=".$tag);
		if ($tag != null) {
		    trace("yes");
//		    $this->retrieve($tag);
			$this->retrieve_one("tag=?", $tag);
		}
	}
	
};