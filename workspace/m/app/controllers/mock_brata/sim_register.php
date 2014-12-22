<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_register()
{
   $teamId = $_POST['teamId'];
   $json = array("team_id"=>$teamId, "message" => "hello");
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/brata/register/reg00", $json);
   if ($json === false) mock_set_to_brata("error");
   else                 mock_set_to_brata(json_encode($json));
   redirect("mock_brata/index","done with register ");
}
