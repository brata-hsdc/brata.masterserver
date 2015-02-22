<?php
function _clear_scores()
{
	$fdata['actionUrl'] = myUrl('ops/clear_scores');
	$fdata['cancelUrl'] = myUrl('mgmt_main/index');
 	$data['pagename']='Clear Scores';
  $data['body'][]='<h2>Warning Submitting this form will clear all scoring data the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'mgmt_main/clear_scores_form.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}