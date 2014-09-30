<?php
function _add() {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_USER)) redirect("errors/401");
  $object=new User();
  $fdata['form_heading']='Add User';
  $fdata['object']=$object;
  $fdata['actionUrl']=myUrl('mgmt_user/ops_update');
  $fdata['actionLabel']="Submit";
  $fdata['cancelUrl']=myUrl('mgmt_user/manage');
  $fdata['cancelLabel']="Cancel";
  $form = View::do_fetch(VIEW_PATH.'mgmt_user/form.php',$fdata);
  $data['head'][]=View::do_fetch(VIEW_PATH.'mgmt_user/form_js.php');
  $data['body'][]='<h2>Add New User</h2>';
  $data['body'][]= $form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}