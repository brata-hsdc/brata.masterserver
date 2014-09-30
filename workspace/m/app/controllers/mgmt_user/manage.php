<?php
function _manage($n=0) {
  loginRequireMgmt();
  $n=(int)$n;
  $data['body'][]='<h2>Manage Users</h2><br />';
  if (loginCheckPermission(USER::MGMT_USER))
  {
    _make_html_table($n,$data);
    $data['body'][]='<p><a href="'.myUrl('mgmt_user/add').'">Add New User</a></p>';
  }
  else
  {
    $data['body'][] = '<p>You do not have permission for this operation';
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}

function _make_html_table($n,&$data) {
  $dbh=getdbh();

  //pagination
  $stmt = $dbh->query('SELECT count(OID) total FROM t_user');
  $total=$stmt->fetchColumn();
  $limit=$GLOBALS['pagination']['per_page'];
  $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
  $data['body'][]=pagination::makePagination($n,$total,myUrl('mgmt_user/manage'),$GLOBALS['pagination']);

  //table
  $stmt = $dbh->query("SELECT OID,CID,permissions,username,fullname FROM t_user LIMIT $n,$limit");
  $tablearr[]=explode(',','username,roll,fullname');
  while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $OID=$rs['OID'];
    $CID=$rs['CID'];
    $row=null;
    $row['username']=htmlspecialchars($rs['username']);
    $row['roll']=htmlspecialchars(User::getPermissionsAsRollText($rs['permissions']));
    $row['fullname']=htmlspecialchars($rs['fullname']);
    $row[]='<a href="'.myUrl("mgmt_user/edit/$OID/$CID").'">Edit</a> | <a href="javascript:jsconfirm(\'Really Delete User?\',\''.myUrl("mgmt_user/ops_delete/$OID/$CID").'\')">Delete</a>';
    $tablearr[]=$row;
  };
  $data['body'][]=table::makeTable($tablearr);
  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}
