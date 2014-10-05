<?php
//
//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//	"station_key": "97531",
//	"station_type": "hmb",
//	"station_callback_url": "http://192.168.0.2:9876"

include_once "app/controllers/rest-v0/json_functions.php";
function _join($key=null)
{
	if ($key === null) {
		json_sendBadRequestResponse("missing station_key");
	}
	$json = json_getObjectFromRequest("PUT");
	//if ($json === NULL) return;
	json_checkMembers("message_version,station_type,station_callback_url", $json);
	
	// output
	$dbh = getdbh();
	$rpi = new RPI();
	$rpi->set('key',$key);
	$rpi->set('URL',$json['station_callback_url']);
	$rpi->set('debug',json_encode($json));
	if ($rpi->create() === false) {
	   json_sendBadRequestResponse("duplicate station_key");
	}
	json_sendObject($json);
}