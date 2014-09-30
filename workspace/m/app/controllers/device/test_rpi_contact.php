<?php
function _test_rpi_contact() {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_RPI)) redirect("errors/401");
  $object=new RPI();
  $urlPrefix="device";
  $fdata['form_heading']='Test rPI Cotact';
  $fdata['object']=$object;
  $fdata['actionUrl']=myUrl("$urlPrefix/test_ops_rpi_contact");
  $fdata['actionLabel']="Submit";
  $fdata['cancelUrl']=myUrl("$urlPrefix/test_index.php");
  $fdata['cancelLabel']="Cancel";
  $form = View::do_fetch(VIEW_PATH."$urlPrefix/test_rpi_contact_form.php",$fdata);
 // $data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/test_rpi_contact_form_js.php");
  $data['body'][]="<h2>Test Contact</h2>";
  $data['body'][]= $form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}