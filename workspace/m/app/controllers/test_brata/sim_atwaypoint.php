<?php
function _sim_atwaypoint()
{
   $waypointId = $_POST['waypointId'];
   $teamId = $_POST['teamId'];
   trace("_sim_atwaypoint");
   $json = array("teamId"=>$teamId, "message" => "");
   // hack just to reuse do_post_request code
   RPI::do_post_request("http://localhost/m/brata/at_waypoint/".$waypointId, $json);
   redirect("test_brata/index","done with sim_atwaypoint");
};