<?php
class CPAData extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_cpa_data'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;

    $this->rs['velocity'] = 0;
    $this->rs['velocity_tolerance'] = 0;
    $this->rs['window_time'] =  0;
    $this->rs['window_time_tolerance'] = 0;
    $this->rs['pulse_width'] = 0;
    $this->rs['pulse_width_tolerance'] = 0;
    $this->rs['combo'] = 0;
    
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
}


