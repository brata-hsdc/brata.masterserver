<?php
class School extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_school'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['name'] = '';
    $this->rs['mascot'] = '';
    $this->rs['logo'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  
  static function getSchoolNameFromId($schoolId) {
    $school = new School($schoolId,-1);
    return $school->get('name');
  }
  
  
  static function getAllAsHTMLOptions($stationId=-1) {
    $school = new School();
    $aray = $school->retrieve_many();
    $options ="";
    foreach ($aray as $school) {
      $schoolOID = $school->get('OID');
      $selected = $school->rs['OID'] == schoolId ? "selected" : "";
      $options .= '<option value='. $schoolOID. ' ' . $selected . '>' . $school->get("name");
    }
    return $options;
  }
  
  static function getAllOrderByName() {
    $school = new School();
    return $station->retrieve_many("OID !=0 order by name");

  }
}