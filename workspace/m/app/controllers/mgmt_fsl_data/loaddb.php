<?php
function _loaddb()
{
	$fdata['actionUrl'] = myUrl('mgmt_fsl_data/ops_loaddb');
	$fdata['cancelUrl'] = myUrl('mgmt_fsl_data/index');
 	$data['pagename']='Load Database';
  $data['body'][]='<h2>Warning Submitting this form will replace all existing FSL data in the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'mgmt_fsl_data/loaddb.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}