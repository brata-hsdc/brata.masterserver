<?php
function _ops_update_score() {
  $OID=max(0,intval($_POST['OID']));
  $CID=max(0,intval($_POST['CID']));
  $msg="";
  
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_TEAM)) redirect("errors/401");
  $itemName="Team";
  $urlPrefix="mgmt_team";
  $object=new Team();
  
  if ($OID) 
  {
    $object->retrieve($OID,$CID);
    if (!$object->exists())
    {
      $msg="$itemName not found!";
    }
    else
    {
      transactionBegin();
      if ($object->updateTotalScore() )
      {
      	Event::createEvent(EVENT::TYPE_EDIT, $object, Station::getRegistrationStation(), 0, $_POST); // just put the post data into the event
        transactionCommit();
        $msg="$itemName updated!";
      }
      else
      {
        transactionRollback();
        $msg="$itemName update failed";
      }
    }
  }
  else 
  {
    $msg = "attempting to create team from ops_update_score which is not supported";
  }
  redirect("$urlPrefix/manage",$msg);
}