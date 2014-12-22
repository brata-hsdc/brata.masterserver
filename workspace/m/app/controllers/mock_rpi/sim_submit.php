<?php
require(APP_PATH.'inc/mock_functions.php');
function _sim_submit()
{
   $stationId = $_POST['stationId'];
   $candidate_answer =$_POST['candidate_answer'];
   $is_correct = isset($_POST['is_correct']) ? true : false;
   $fail_message = $_POST['fail_message'];
   $json = array("message_version"=>0, "candidate_answer"=>$candidate_answer , 
   		"is_correct"=> $is_correct, "fail_message"=>$fail_message);
   // hack just to reuse do_post_request code
   $json = RPI::do_post_request("http://localhost/m/rpi/submit/$stationId", $json);
   if ($json === false) mock_set_rpi_response("error");
   else                 mock_set_rpi_response(json_encode($json));
   redirect("mock_rpi/index","done with submit ");
}