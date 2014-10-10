<?php
class Waypoint extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_waypoint'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['lat'] = '';
    $this->rs['lng'] = '';
    $this->rs['encode'] = true;
    $this->rs['description'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  static function getFromLatLng($lat,$lng) {
  	$waypoint = new Waypoint();
  	return $waypoint->retrieve_one('lat=? and lng=?',array($lat,$lng));
  }
  
}