<?php
function _ops_update() {
  $OID=max(0,intval($_POST['OID']));
  $CID=max(0,intval($_POST['CID']));
  $encode=isset($_POST["encode"]);
  $msg="";
  
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_HMB_DATA)) redirect("errors/401");
  $itemName="HMB Data";
  $urlPrefix="mgmt_hmb_data";
  $object=new HMBData();
  
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
      $object->set("encode",$encode);
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
    $object->set("encode",$encode);
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