<?php
class HMBData extends ModelEx {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_hmb_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['_1st_on'] = 0;
    $this->rs['_1st_off'] = 0;
    $this->rs['_2nd_on']  = 0;
    $this->rs['_2nd_off'] = 0;
    $this->rs['_3rd_on']  = 0;
    $this->rs['_3rd_off'] = 0;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
}
