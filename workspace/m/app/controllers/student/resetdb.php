<?php
function _resetdb()
{
  $fdata['actionUrl'] = myUrl('student/ops_resetdb');
  $fdata['cancelUrl'] = myUrl('student/index');
  $data['pagename']='Reset Database';
  $data['body'][]='<h2>Warning Submitting this form will reset the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'student/resetdb_form.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/studentlayout.php',$data);

}