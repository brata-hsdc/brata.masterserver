<?php
function _sim_submit()
{
	$teamid = $_POST['teamId'];
	$candidateAnswer =$_POST['candidateAnswer'];
	trace("_sim_submit");
	$json = array("teamId"=>$teamId, "message" => $candidateAnswer);
	// hack just to reuse do_post_request code
	RPI::do_post_request("http://localhost/m/brata/submit/".$stationTag, $json);
	redirect("test_brata/index","done with sim submit");
}