<?php
class RPI extends ModelEx {

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_rpi'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['URL'] = '';
    $this->rs['debug'] ='';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  static function do_get_request($path)
  {
  	$ch = curl_init($path);
  	curl_setopt($ch, CURLOPT_RETURNTRANSFER,true);
  	$retValue = curl_exec($ch);
  	curl_close($ch);
  	return $retValue;
  }
static function do_post_request($path, array $json, $decode=true) 
{  
  $ch = curl_init($path);
  $json = json_encode($json);
  curl_setopt($ch, CURLOPT_CUSTOMREQUEST,"POST");
  curl_setopt($ch, CURLOPT_POSTFIELDS,$json);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER,true);
  curl_setopt($ch, CURLOPT_HTTPHEADER,
  array('Content-Type: application/json','Content-Length: '.strlen($json))
  );
  $retValue = curl_exec($ch);
  curl_close($ch);
  if ($retValue === false) return false;  // request failed
  return $decode ? json_decode($retValue,true) : $retValue;     // put the response back into object form
  }
  /* todo if needed
  static function getStationNameFromId($stationId) {
    $station = new Station($stationId,-1);
    return $station->get('name');
  }
  
  
  static function getAllAsHTMLOptions($stationId=-1) {
    $station = new Station();
    $aray = $station->retrieve_many();
    $options ="";
    foreach ($aray as $station) {
      $stationOID = $station->get('OID');
      $selected = $station->rs['OID'] == sationId ? "selected" : "";
      $options .= '<option value='. $stationOID. ' ' . $selected . '>' . $station->get("name");
    }
    return $options;
  }
  
  static function getAllOrderByName() {
    $station = new Station();
    return $station->retrieve_many("OID !=0 order by name");

  }
  */
}