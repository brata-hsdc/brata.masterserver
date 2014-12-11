<?php
class FSLData extends ModelEx {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_fsl_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['tag'] = "";
    $this->rs['lat1'] = 0;
    $this->rs['lng1'] = 0;
    $this->rs['lat2'] = 0;
    $this->rs['lng2'] = 0;
    $this->rs['lat3'] = 0;
    $this->rs['lng3'] = 0;    
    $this->rs['rad1'] = 0;
    $this->rs['rad2'] = 0;
    $this->rs['rad3'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
}
