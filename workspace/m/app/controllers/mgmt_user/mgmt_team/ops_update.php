<?php
function _ops_update() {
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
      $object->merge($_POST);
      var_dump($object);
      if ($object->update() )
      {
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
    $object->merge($_POST);
    transactionBegin();
    if ($object->create() )
    {
      transactionCommit();
      $msg="$itemName created!";
    }
    else
    {
      transactionRollback();
      $msg="$itemName Create failed";
    }
  }
  redirect("$urlPrefix/manage",$msg);
}