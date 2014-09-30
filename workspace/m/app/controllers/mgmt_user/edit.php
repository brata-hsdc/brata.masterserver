<?php
function _edit($OID=0, $CID=0) {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_USER)) redirect("errors/401");

  $object=new User();
  $object->retrieve($OID,$CID);
  if (!$object->exists())
  $data['body'][]='<p>User Not Found!</p>';
  else {
    $fdata['form_heading']='Edit User';
    $fdata['object']=$object;
    $fdata['actionUrl']=myUrl('mgmt_user/ops_update');
    $fdata['actionLabel']="Submit";
    $fdata['cancelUrl']=myUrl('mgmt_user/manage');
    $fdata['cancelLabel']="Cancel";
    $form = View::do_fetch(VIEW_PATH.'mgmt_user/form.php',$fdata);
    $data['head'][]=View::do_fetch(VIEW_PATH.'mgmt_user/form_js.php');
    $data['body'][]='<h2>Edit User</h2>';
    $data['body'][]=$form;
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}