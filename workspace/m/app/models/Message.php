<?php
class Message extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_message'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['text'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
}