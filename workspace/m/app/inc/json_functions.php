<?php

// call this when we get and invalid request
function json_sendBadRequestResponse($stsmsg="invalid json",$jsonmsg=null)

{
	rest_CacheHeaders();
	header("HTTP/1.1 400 Bad Request $stsmsg", true, 400);
	if ($jsonmsg != null)
	{
	  echo "{ \"error\": \"$jsonmsg\" }";
	}
	die;
}

// extract a json object from the request stream
// method expected HTTP method
function json_getObjectFromRequest($method)
{
	error_log("getObjectFromRequest starting\n",3,"/var/tmp/m.log");
	$rm= $_SERVER['REQUEST_METHOD'];
	$ct = $_SERVER['CONTENT_TYPE'];
	error_log("getObjectFromRequest method $rm \n",3,"/var/tmp/m.log");
	error_log("getObjectFromRequest content type $ct\n",3,"/var/tmp/m.log");
  if ($_SERVER['REQUEST_METHOD'] != $method)          return json_sendBadRequestResponse("incorrect HTTP method");
  if(!isset($_SERVER['CONTENT_TYPE']))                return json_sendBadRequestResponse("missing content-type");
  if ($_SERVER['CONTENT_TYPE'] != "application/json") return json_sendBadRequestResponse("content-type not json");
  $x=file_get_contents( 'php://input');
  error_log("got $x \n",3,"/var/tmp/m.log");
  $jsonObject =json_decode($x , true);
  if ($jsonObject != NULL) return $jsonObject;  
  json_sendBadRequestResponse("invalid json");
  // don't return return NULL;

}

// given a list of fields check that all exist in the given json object
// return if all is well otherwise send 
function json_checkMembers($fields, &$json)
{
	$missing = null;
	foreach (explode(",", $fields) as $name)
	{
		if (array_key_exists($name,$json)) continue;
		$missing = $missing ?  $missing.",".$name : $name;
	}
	if ($missing == null) return true;
	json_sendBadRequestResponse("missing $msg");
	//return false;
}

//
// writes the json encoded object to the client
// returns true on success, false otherwise
function json_sendObject($jsonObject)
{
	error_log("json_sendObject starts\n",3,"/var/tmp/m.log");
	rest_CacheHeaders();
	header("Content-Type: application/json");
	$string = json_encode($jsonObject);
	if ($string === false) return false;
	error_log("json_sendObject sends $string \n",3,"/var/tmp/m.log");
	echo $string;
	return true;
}


//
//  merge the given fields into the given jsonObject from the given KissmvcObject
function json_merge(&$jsonObject, &$object, &$fields)
{
	foreach ($fields as $item)
	{
		$jsonObject[$item] = $object->get($item);
	}
}