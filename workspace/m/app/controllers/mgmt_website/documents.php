<?php
function _documents() {

  loginRequireMgmt();
  $data['body'][]='<h2>Documents</h2><br />';

  if (loginCheckPermission(USER::MGMT_WEBSITE))
  {

   	$fdata['form_heading']='Manage Documents';
   	$fdata['cancel']=myUrl("mgmt_website/manage");
   	$fdata['action']=myUrl("mgmt_website/ops_documents_update");
   	$form = View::do_fetch(VIEW_PATH.'mgmt_website/documents_form.php',$fdata);
//   	$data['head'][]=View::do_fetch(VIEW_PATH.'mgmt_website/documents_form_js.php');
//    $data['head'][]='<script type="text/javascript" src="'.myUrl('js/isvalid.js').'"></script>';
   	$data['body'][]= $form;
  }
  else
  {
    $data['body'][] = '<p>You do not have permission for this operation';
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}

