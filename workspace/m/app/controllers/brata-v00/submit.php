<?php
//
//	"message_version": 0,
//	"message_timestamp": "2014-09-15 14:08:59",
//	"value": "true",
//	"station_type": "hmb",
require(APP_PATH.'inc/json_functions.php');
//
function _submit($key=null)
{
	if ($key === null) {
		json_sendBadRequestResponse("missing station_key");
	}
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("message_version,station_type,value", $json);

	// output
	$dbh = getdbh();
	$rpi->set('key',$key);
	json_sendObject($json);
}