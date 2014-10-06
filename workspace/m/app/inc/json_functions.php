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
  if ($_SERVER['REQUEST_METHOD'] != $method)          return json_sendBadRequestResponse("incorrect HTTP method");
  if(!isset($_SERVER['CONTENT_TYPE']))                return json_sendBadRequestResponse("missing content-type");
  if ($_SERVER['CONTENT_TYPE'] != "application/json") return json_sendBadRequestResponse("content-type not json");
  $x=file_get_contents( 'php://input');
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
function json_sendObject($jsonObject)
{
	rest_CacheHeaders();
	header("Content-Type: application/json");
	echo json_encode($jsonObject);
}

