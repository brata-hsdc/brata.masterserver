<?php
function _about($mode="version") {
  $form = View::do_fetch(VIEW_PATH.'student/'.$mode.'.php');
  //$data['body'][]='<h2>Add New Topic</h2>';
  $data['body'][]= $form;
  View::do_dump(VIEW_PATH.'layouts/student.php',$data);
}