<?php
function _index() {
  $data['pagename']='Welcome';
  $data['body'][]=View::do_fetch(VIEW_PATH.'student/index.php');
  View::do_dump(VIEW_PATH.'layouts/studentlayout.php',$data);
}