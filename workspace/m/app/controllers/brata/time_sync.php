<?php
// brata test time sync message
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
function _time_sync() 
{
   trace("start",__FILE__,__LINE__,__METHOD__);
	
   $json = json_getObjectFromRequest("POST");
   if ($json === null) {
      trace("missing json",__FILE__,__LINE__,__METHOD__);
      rest_sendBadRequestResponse(400,"missing json");  // doesn't return
   }

   json_checkMembers("message", $json);
   $message = $json['message'];
   if ($message === null) {
      trace("missing message",__FILE__,__LINE__,__METHOD__);
      rest_sendBadRequestResponse(400,"missing message");  // doesn't return
   }
   //$n = sscanf($message, "%d", $time);
   //list($time) = sscanf($message, "[time=%d]");
   $n = substr_compare($message,"[time=",0,6,TRUE);
   if ($n == 0 and strlen($message) == 11) {
      $timestr = substr($message, 6, 4);
      $time = (int)$timestr;	
   }
   else {
      trace("createEvent Failes",__FILE__,__LINE__,__METHOD__);
      rest_sendBadRequestResponse(400,"expected format of [time=nnnn] where nnnn is a number greater than 42");  // doesn't return
   }
   if ($time === null) {
      trace("createEvent Failes",__FILE__,__LINE__,__METHOD__);
      rest_sendBadRequestResponse(400,"expected format of [time=nnnn] where nnnn is a number greater than 42");  // doesn't return	
   }
   if ($time <= 42) {
      trace("createEvent Failes",__FILE__,__LINE__,__METHOD__);
      rest_sendBadRequestResponse(400,"The time stamp is invalid! Please try again.");  // doesn't return
      json_sendBadRequestResponse("The time stamp is invalid! Please try again.");	
   }

   json_sendObject(array('message' => "Your timestamp has been synced!" ) );
}
