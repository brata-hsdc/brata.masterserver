<?php

function _sim_start_challenge()
{
   $stationTag = $_POST['stationId'];
   $teamId = $_POST['teamId'];
   trace("_sim_start_challenge");
   $json = array("teamId"=>0, "message" => "hello");
   // hack just to reuse do_post_request code
   RPI::do_post_request("http://localhost/m/brata/start_challenge/".$stationTag, $json);
   redirect("test_brata/index","done with start challenge");
}
