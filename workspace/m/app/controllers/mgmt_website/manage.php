<?php
function _manage($n=0) {

  loginRequireMgmt();
  $n=(int)$n;
  $data['body'][]='<h2>Web Site</h2><br />';

  if (loginCheckPermission(USER::MGMT_WEBSITE))
  {
    $data['body'][]= '<a href="'.myUrl("mgmt_website/website").'">Edit Web Site Settings</a>';
    $data['body'][]= '<br>';
    $data['body'][]= '<a href="'.myUrl("mgmt_website/sysconfig").'">Edit System Configuration</a>';
    $data['body'][]= '<br>';
    $data['body'][]= '<a href="'.myUrl("mgmt_website/documents").'">Upload Documents (term of use)</a>';
  }
  else
  {
    $data['body'][] = '<p>You do not have permission for this operation';
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}

