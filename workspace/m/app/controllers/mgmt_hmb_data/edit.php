<?php
function _edit($OID=0, $CID=0) {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_HMB_DATA)) redirect("errors/401");
  $item="HMB Data";
  $urlPrefix="mgmt_hmb_data";
  $object=new HMBData();
  $object->retrieve($OID,$CID);
  if (!$object->exists())
  $data['body'][]="<p>$item Not Found!</p>";
  else {
    $fdata['form_heading']="Edit $item";
    $fdata['object']=$object;
    $fdata['actionUrl']=myUrl("$urlPrefix/ops_update");
    $fdata['actionLabel']="Submit";
    $fdata['cancelUrl']=myUrl("$urlPrefix/manage");
    $fdata['cancelLabel']="Cancel";
    $form = View::do_fetch(VIEW_PATH."$urlPrefix/form.php",$fdata);
    $data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/form_js.php");
    $data['body'][]="<h2>Edit $item</h2>";
    $data['body'][]=$form;
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}