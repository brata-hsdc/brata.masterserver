<?php
// output headers for json respone
function rest_CacheHeaders()
{
  header("Expires: " . gmdate('D, d M Y H:i:s \G\M\T') );
  header("Cache-Control: no-cache");
  header("Pragma: no-cache");
}

// call this when we get and invalid request
function rest_sendBadRequestResponse($sts,$stsmsg)

{
	rest_CacheHeaders();
	header("HTTP/1.1 $sts Bad Request $stsmsg", true, $sts);
	die;
}
// call signal all is well
function rest_sendSuccessResponse($sts=200,$stsmsg="OK",$body=null)
{
	rest_CacheHeaders();
	header("HTTP/1.1 $sts - $stsmsg", true, $sts);
	if ($body != null) {
		trace("sending ".$body,__FILE__,__LINE__,__METHOD__);
		echo $body;
	}
}