<?php
class EXTData extends ModelEx {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_ext_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['waypoint1_lat'] = 0;
    $this->rs['waypoint1_lng'] = 0;
    $this->rs['waypoint2_lat'] = 0;
    $this->rs['waypoint2_lng'] = 0;
    $this->rs['waypoint3_lat'] = 0;
    $this->rs['waypoint3_lng'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
}
