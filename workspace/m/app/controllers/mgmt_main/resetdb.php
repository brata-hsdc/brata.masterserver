<?php
function _resetdb()
{
	$fdata['actionUrl'] = myUrl('ops/resetdb');
	$fdata['cancelUrl'] = myUrl('mgmt_main/index');
 	$data['pagename']='Reset Database';
  $data['body'][]='<h2>Warning Submitting this form will reset the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'mgmt_main/resetdb_form.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}