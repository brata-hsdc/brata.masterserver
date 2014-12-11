<?php
function _ops_update() {
  $OID=max(0,intval($_POST['OID']));
  $CID=max(0,intval($_POST['CID']));
  $msg="";
  
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_FSL_DATA)) redirect("errors/401");
  $itemName="FSL Data";
  $urlPrefix="mgmt_fsl_data";
  $object=new FSLData();
  
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