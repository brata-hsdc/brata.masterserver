<?php
function _ops_delete($OID=0,$CID=0) {
  $OID=max(0,intval($OID));
  $CID=max(0,intval($CID));
  $msg='';
  
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_FSL_DATA)) redirect("errors/401");
  $itemName="FSL Data";
  $urlPrefix="mgmt_fsl_data";
  $object=new FSLData($OID,$CID);
  
  if (!$object->exists())
  $msg="$itemName not found!";
  else {
    transactionBegin();
    if ($object->delete() )
    {
      transactionCommit();
      $msg="$itemName deleted!";
    }
    else
    {
      TransactionRollback();
      $msg="$itemName delete failed!";
    }

  }
  redirect("$urlPrefix/manage",$msg);
}