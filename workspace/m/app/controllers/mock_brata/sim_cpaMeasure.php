<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_cpaMeasure()
{
   $stationTag = $_POST['stationTag'];
   $teamId = $_POST['teamId'];
   $json = array("team_id"=>$teamId, "message" => "");
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/brata/cpaMeasure/".$stationTag, $json);
   //trace("json ".$json);
   if ($json === false) mock_set_brata_response("error");
   else                 mock_set_brata_response(json_encode($json));
   redirect("mock_brata/index","done with cpaMeasure");
};
