<?php
function _index() {
  loginRequireMgmt();
  $data['pagename']='Welcome';
  $data['body'][]=View::do_fetch(VIEW_PATH.'mgmt_main/index.php');
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}