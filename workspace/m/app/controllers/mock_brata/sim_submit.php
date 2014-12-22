<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_submit()
{
	$teamid = $_POST['teamId'];
	$candidateAnswer =$_POST['candidateAnswer'];
	$json = array("team_id"=>$teamId, "message" => $candidateAnswer);
	// hack just to reuse do_post_request code
	$json = RPI::do_post_request("http://localhost/m/brata/submit/".$stationTag, $json);
	if ($json === false) mock_set_brata_response("error");
	else                 mock_set_brata_response(json_encode($json));
	redirect("mock_brata/index","done with sim submit");
}