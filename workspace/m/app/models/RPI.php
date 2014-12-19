<?php
class RPI extends ModelEx {

  const PIN = "31415"; // a useless piece of information
  
  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_rpi'); 
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['stationId'] = -1;
    $this->rs['URL'] = '';
    $this->rs['lastContact'] = "";
    $this->rs['debug'] ='';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
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
  function set_contact_data(&$json) {
  	$this->rs['lastContact']= unixToMySQL(time());
  	$this->rs['URL'        ]= $json ['station_url'];
  	$this->rs['debug'      ]= json_encode ( $json );
  }
 
  
  function start_challenge($parms)  {
  	$json = array("message_version" =>0 , 
  			"message_timestamp"=> date("Y-m-d H:i:s"), 
  			"theatric_delay_ms"=>1000 );
  	$json = array_merge($json,$parms);  // over ride / merge in parms
  	trace(json_encode($json),__FILE__,__LINE__,__METHOD__);
  	// todo remove this is just for testing don't send it URL start with test
  	if (substr($this->rs['URL'],0,4) == "test") return true;
  	return RPI::do_post_request($this->rs['URL']."/start_challenge", $json);
  }
  
  function reset() {
  	return RPI::do_get_request($this->rs['URL']."/reset/".RPI::PIN);
  }
  
  function shutdown() {
  	return RPI::do_get_request($this->rs['URL']."/shutdown/".RPI::PIN);
  }
  
  static function getFromStationId($stationId) {
  	$rpi = new RPI();
  	return $rpi->retrieve_one("stationId=?", $stationId);
  }
  
  static function do_get_request($path, $returnTransfer=false) {
  	$ch = curl_init($path);
  	if ($returnTransfer) curl_setopt($ch, CURLOPT_RETURNTRANSFER,true);
  	$retValue = curl_exec($ch);
  	//var_dump($retValue);
  	// todo check return codes
  	curl_close($ch);
  	return $retValue;
  }
  static function do_post_request($path, array $json, $decode=true) {
  	$ch = curl_init($path);
  	$json = json_encode($json);
trace("sending ".$json." to ".$path,__FILE__,__LINE__,__METHOD__);  	
  	curl_setopt($ch, CURLOPT_CUSTOMREQUEST,"POST");
  	curl_setopt($ch, CURLOPT_POSTFIELDS,$json);
  	curl_setopt($ch, CURLOPT_RETURNTRANSFER,true);
  	curl_setopt($ch, CURLOPT_HTTPHEADER,
  	array('Content-Type: application/json','Content-Length: '.strlen($json))
  	);
  	$retVal = curl_exec($ch);
  	curl_close($ch);
  	if ($retVal === false) {
  	trace("RPI::do_post failed returning false",__FILE__,__LINE__,__METHOD__);
  	  return false;  // request failed
    }
trace("returning ".$retVal,__FILE__,__LINE__,__METHOD__);
  	$retVal = $decode ? json_decode($retVal,true) : $retVal;     // put the response back into object form
  	return $retVal;
  }
  
}