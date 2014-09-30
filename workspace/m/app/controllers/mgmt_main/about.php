<?php
function _about($mode="version") {
  //loginRequireMgmt();
  //if (!loginCheckPermission(USER::MGMT_TOPIC)) redirect("errors/401");
  $form = View::do_fetch(VIEW_PATH.'mgmt_main/'.$mode.'.php');
  //$data['body'][]='<h2>Add New Topic</h2>';
  $data['body'][]= $form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}