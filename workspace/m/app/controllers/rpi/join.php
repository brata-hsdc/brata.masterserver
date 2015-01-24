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
require(APP_PATH.'inc/RestException.php');
//
function _join($stationTag = null) {
	try {
		if ($stationTag === false) { 
			trace("stationTag not present",__FILE__,__LINE__,__METHOD__);
			throw new RestException( 400, "stationTag not present" );
		}
		
		$station = Station::getFromTag ( $stationTag );
		if ($station === false) {
			trace ( "_join station not found stationTag=" . $stationTag,__FILE__,__LINE__,__METHOD__ );
			throw new RestException( 500, "station not found stationTag=" . $stationTag );
		}
		
		trace ( "tag=" . $stationTag . " station OID=" . $station->get ( 'OID' ),__FILE__,__LINE__,__METHOD__ );
		$json = json_getObjectFromRequest ( "POST" );
		// if ($json === NULL) return;
		json_checkMembers ( "message_version,station_type,station_url", $json );
		
		$rpi = RPI::getFromStationId($station->get('OID') );
		if ($rpi === false) 		// new join
		{
			// output
			$rpi = new RPI ();
			$rpi->set ( 'stationId', $station->get ( 'OID' ) );
			$rpi->set_contact_data($stationTag,$json);

			if ($rpi->create () === false) {
				trace("create failed",__FILE__,__LINE__,__METHOD__);
				throw new RestException ( 500, "join create failed" );
			}
		} else {
 			$rpi->set_contact_data($stationTag,$json);
			if ($rpi->update() === false){
				trace("update failed",__FILE__,__LINE__,__METHOD__);
				throw new RestException(500,"join update failed");
			}
		}
		rest_sendSuccessResponse ( 202, "Accepted","$stationTag has joined M" );
	} catch ( RestException $e ) {
		rest_sendBadRequestResponse ( $e->statusCode, $e->statusMsg ); // doesn't return
	}
}