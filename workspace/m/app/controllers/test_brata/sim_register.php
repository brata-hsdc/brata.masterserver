<?php

function _sim_register()
{
   $teamId = $_POST['teamId'];
   $json = array("team_id"=>$teamId, "message" => "hello");
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/brata/register/REG", $json);
   $string = htmlspecialchars(json_encode($json));
   redirect("test_brata/index","done with register ".$string);
}
