<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_start_challenge()
{
   $stationTag = $_POST['stationId'];
   $teamId = $_POST['teamId'];
   $json = array("team_id"=>$teamId, "message" => "");
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/brata/start_challenge/".$stationTag, $json);
   trace("json ".$json);
   if ($json === false) mock_set_to_brata("error");
   else                 mock_set_to_brata(json_encode($json));
   redirect("test_brata/index","done with start challenge");
}
