<?php

function _sim_start_challenge()
{
   $stationTag = $_POST['stationId'];
   $teamId = $_POST['teamId'];
   $json = array("team_id"=>$teamId, "message" => "");
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/brata/start_challenge/".$stationTag, $json);
   $string = htmlspecialchars(json_encode($json));
   redirect("test_brata/index","done with start challenge -".$string);
}
