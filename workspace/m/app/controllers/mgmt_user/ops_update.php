<?php
function _ops_update() {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_USER)) redirect("errors/401");
  $msg='';
  $OID=max(0,intval($_POST['OID']));
  $CID=max(0,intval($_POST['CID']));
  if ($_POST['password'] != $_POST['confirm']) redirect("mgmt_user/edit","password not equal to confirm");

  $object=new User();
  if ($OID) {
    $object->retrieve($OID,$CID);
    $object->merge($_POST);
    if ($_POST['password'] !="") $object->setPassword($_POST['password']);
    if (!$object->exists())
    $msg='User not found!';
    else
    if ($object->update())
    $msg='User updated!';
    else
    $msg='User update failed!';
  }
  else {
    $object->merge($_POST);
    if ($_POST['password'] !="") $object->setPassword($_POST['password']);
    if ($object->create())
    $msg='User inserted!';
    else
    $msg='User insert failed!';
  }
  redirect('mgmt_user/manage',$msg);
}