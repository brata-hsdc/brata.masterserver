<?php
function _ops_delete($OID=0,$CID=0) {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_USER)) redirect("errors/401");
  $msg='';
  $OID=max(0,intval($OID));
  $CID=max(0,intval($CID));
  $object=new User($OID,$CID);
  if (!$object->exists())
  $msg='User not found!';
  else {
    if ($object->delete())
    $msg='User deleted!';
    else
    $msg='User delete failed!';
  }
  redirect('mgmt_user/manage',$msg);
}