<?php
function _add() {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_CPA_DATA)) redirect("errors/401");
  $object=new CPAData();
  $item="CPA Data";
  $urlPrefix="mgmt_cpa_data";
  $fdata['form_heading']="Add $item";
  $fdata['object']=$object;
  $fdata['actionUrl']=myUrl("$urlPrefix/ops_update");
  $fdata['actionLabel']="Submit";
  $fdata['cancelUrl']=myUrl("$urlPrefix/manage");
  $fdata['cancelLabel']="Cancel";
  $form = View::do_fetch(VIEW_PATH."$urlPrefix/form.php",$fdata);
  $data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/form_js.php");
  $data['body'][]="<h2>Add New $item</h2>";
  $data['body'][]= $form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}