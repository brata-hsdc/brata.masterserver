<?php
function _ops_update() {
  $OID=max(0,intval($_POST['OID']));
  $CID=max(0,intval($_POST['CID']));
  $msg='';
  
  loginRequireMgmt();
  if (!loginCheckPermission(USER::TEST_EVENT)) redirect("errors/401");
  $itemName="Event";
  $urlPrefix="test_event";
  $object=new Event();
  
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