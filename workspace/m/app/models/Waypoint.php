<?php
class Waypoint extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_waypoint'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['lat'] = '';
    $this->rs['lng'] = '';
    $this->rs['description'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  static function getFromLatLng($lat,$lng) {
  	$waypoint = new Waypoint();
  	return $waypoint->retrieve_one('lat=? and lng=?',array($lat,$lng));
  }
  static function getName($waypointId) {
  	$object = new Waypoint($waypointId,-1);
  	return $object->get('name');
  }
  
  static function getAllAsHTMLOptions($itemId=-1) {
  	$object = new Waypoint();
  	$aray = $object->retrieve_many();
  	$options ="";
  	foreach ($aray as $item) {
  		$itemOID = $item->get('OID');
  		$selected = $item->rs['OID'] == $itemId ? "selected" : "";
  		$options .= '<option value='. $itemOID. ' ' . $selected . '>' . $item->get("name");
  	}
  	return $options;
  }
  
  
}