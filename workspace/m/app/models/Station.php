<?php
class Station extends ModelEx {
  
  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_station'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['typeId'] = -1;
    $this->rs['name'] = "";
    $this->rs['description'] = "";  
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  static function getTypeAsText($typeId) {
  	$stationType = new StationType($typeId,-1);
  	return $stationType->get('shortName');
  } 
}