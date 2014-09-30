<?php
function _test_ops_rpi_contact()
{
	if (!isset($_POST['rPIUrl']))
	{
		echo "no url given";
		return;
	}
	$url = $_POST['rPIUrl'];
	$method = isset($_POST['method']) ? $_POST['method'] : "GET";
	$data = isset($_POST['data']) ? $_POST['data'] : "";
	echo "using curl to $method on $url<br>";
	if       ($method == "GET") {
		$result = RPI::do_get_request($url);
	}
	else if  ($method == "POST") {
		$json= json_decode($data,true);
		if ($json == null)
		{
			echo "json_decode failed data was $data";
			return;
		}
		$result = RPI::do_post_request($url, $json,false);
	} else {
	  echo "unsupported method";	
	} 
	if ($result === false)
	{
		echo "requested failed";
		return;
			
	}
	$result = htmlentities($result);
	echo "<pre>$result</pre>";
}