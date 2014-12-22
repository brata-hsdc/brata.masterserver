<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_join()
{
   $stationId = $_POST['stationId'];
   $stationType = $_POST['stationType'];
   $json = array("message_versoion"=>0, "station_type"=>$stationType,"station_url"=>$_POST['station_url']);
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/brata/register/$stationId", $json);
   if ($json === false) mock_set_to_brata("error");
   else                 mock_set_to_brata(json_encode($json));
   redirect("mock_brata/index","done with register ");
}
