<?php
class Station extends ModelEx {
  
  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_station'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['typeId'] = -1;
    $this->rs['tag'] = ""; 
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  // map the given typeId into its text falue
  static function getTypeAsText($typeId) {
  	$stationType = new StationType($typeId,-1);
  	return $stationType->get('name');
  } 
  
  // fetch the Station object for the given skey
  static function getFromTag($tag) {
  	$station = new Station();
  	return $station->retrieve_one("tag=?", $tag);
  }
  // use this if the QR code for the registration station doesn't have the tag inclued.
  static function getRegistrationStation() {
    return Station::getFromTag("reg01");
  }
  // for brata testing only
  static function getAllAsHTMLOptions($itemSelected=-1) {
  	$object = new Station();
  	$aray = $object->retrieve_many();
  	$options ="";
  	foreach ($aray as $item) {
  		$selected = $item->get('tag') == $itemSelected ? "selected" : "";
  		$options .= '<option value='. $item->get('tag'). ' ' . $selected . '>' . $item->get("tag");
  	}
  	return $options;
  } 
  // todo need a better way find by stationType
  static function getAllCTSAsHTMLOptions($itemSelected=-1) {
  	$object = new Station();
  	$aray = $object->retrieve_many("tag like ? ",array("cts%"));
  	$options ="";
  	foreach ($aray as $item) {
  		$selected = $item->get('OID') == $itemSelected ? "selected" : "";
  		$options .= '<option value='. $item->get('OID'). ' ' . $selected . '>' . $item->get("tag");
  	}
  	return $options;
  }  
  // for rPI testing only
  static function getAllRPIAsHTMLOptions($itemSelected=-1) {
  	$object = new Station();
  	$aray = $object->retrieve_many("tag like ? or tag like ? or tag like ?",array("cts%","hmb%","cpa%"));
  	$options ="";
  	foreach ($aray as $item) {
  		$selected = $item->get('tag') == $itemSelected ? "selected" : "";
  		$options .= '<option value='. $item->get('tag'). ' ' . $selected . '>' . $item->get("tag");
  	}
  	return $options;
  }
}
