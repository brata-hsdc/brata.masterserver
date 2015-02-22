<?php
function _clear_scores()
{
	$fdata['actionUrl'] = myUrl('student/ops_clear_scores');
	$fdata['cancelUrl'] = myUrl('student/index');
 	$data['pagename']='Clear Scores';
  $data['body'][]='<h2>Warning Submitting this form will clear all scoring data the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'student/clear_scores_form.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/studentlayout.php',$data);

}