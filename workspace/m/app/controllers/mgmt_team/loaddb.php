<?php
function _loaddb()
{
	loginRequireMgmt();
	if (!loginCheckPermission(USER::MGMT_TEAM)) redirect("errors/401");
	$fdata['actionUrl'] = myUrl('mgmt_team/ops_loaddb');
	$fdata['cancelUrl'] = myUrl('mgmt_team/index');
 	$data['pagename']='Load Database';
  $data['body'][]='<h2>Warning Submitting this form will replace all existing Team data in the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'mgmt_team/loaddb.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}