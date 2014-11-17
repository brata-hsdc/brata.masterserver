<?php
//  unfortunatly join is also used as a keep alive

//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//	"station_id": "97531",
//	"station_type": "hmb",
//	"station_url": "http://192.168.0.2:9876"
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
//
function _join()
{
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("message_version,station_id,station_type,station_url", $json);

	$rpi = RPI::getByURL($json['station_url']);
	if ($rpi === false)  // new join
	{
	  $station= Station::getFromTag($json['station_id']);
	  if ($station === false) rest_sendBadRequestResponse(400,"station_id not present");
	  // output
	  $rpi = new RPI();
	  $rpi->set('stationId',$station->get('OID'));
	  $rpi->set('URL',$json['station_url']);
	  $rpi->set('debug',json_encode($json));
	  if ($rpi->create() === false) {
	     rest_sendBadRequestResponse(500,"create faled");
	  }
	}
	else
	{
       $rpi->contact();
	}
	rest_sendSuccessResponse(202,"Accepted");
}