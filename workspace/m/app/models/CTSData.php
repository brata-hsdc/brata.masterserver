<?php
class CTSData extends ModelEx {
		
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_cts_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['tag'] = "";
    $this->rs['_1st'] = 0.0;
    $this->rs['_2nd'] = 0.0;
    $this->rs['_3rd'] = 0.0;
    $this->rs['_4th'] = 0.0;
    $this->rs['_5th'] = 0.0;
    $this->rs['tolerance'] = 0.0 ;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
}
