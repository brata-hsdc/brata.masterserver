<?php
function _loaddb()
{
  if (!loginCheckPermission(USER::MGMT_EXT_DATA)) redirect("errors/401");
  $fdata['actionUrl'] = myUrl('mgmt_ext_data/ops_loaddb');
  $fdata['cancelUrl'] = myUrl('mgmt_ext_data/index');
  $data['pagename']='Load Database';
  $data['body'][]='<h2>Warning Submitting this form will replace all existing EXT data in the Database</h2><br/>';
  $data['body'][]=View::do_fetch(VIEW_PATH.'mgmt_ext_data/loaddb.php', $fdata); 
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);

}