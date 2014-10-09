<?php
//
//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//	"station_key": "97531",
//	"station_type": "hmb",
//	"station_callback_url": "http://192.168.0.2:9876"
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _join($key=null)
{
	if ($key === null) {
		rest_sendBadRequestResponse(400,"missing station_key");
	}
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("message_version,station_type,station_callback_url", $json);
	
	$station= Station::getFromKey($key);
	if ($station === false) rest_sendBadRequestResponse(400,"invalid key");
	// output
	$rpi = new RPI();
	$rpi->set('stationId',$station->get('OID'));
	$rpi->set('URL',$json['station_callback_url']);
	$rpi->set('debug',json_encode($json));
	if ($rpi->create() === false) {
	   rest_sendBadRequestResponse(500,"create faled");
	}
	rest_sendSuccessResponse(202,"Accepted");
}