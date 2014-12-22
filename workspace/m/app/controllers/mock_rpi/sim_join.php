<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_join()
{
   $stationId = $_POST['stationId'];
   $stationType = $_POST['stationType'];
   $json = array("message_version"=>0, "station_type"=>$stationType,"station_url"=>$_POST['station_url']);
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/rpi/join/$stationId", $json);
   if ($json === false) mock_set_rpi_response("error");
   else                 mock_set_rpi_response(json_encode($json));
   redirect("mock_rpi/index","done with join ");
}
