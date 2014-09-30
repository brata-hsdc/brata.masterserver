<?php
class Team extends ModelEx {

  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_team'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['schoolId'] = -1;
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  function getSchoolName() {
  	return School::getSchoolNameFromId($this->rs['schoolId']);
  }
  
  static function getNameFromId($id) {
    $team = new Team($id,-1);
    return $team->get('name');
  }
  

}