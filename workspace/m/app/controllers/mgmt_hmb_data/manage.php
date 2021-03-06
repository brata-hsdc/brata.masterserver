<?php

function _manage($n=0) {
  $table="t_hmb_data";
  $item="HMB Data";
  $urlPrefix="mgmt_hmb_data";
  loginRequireMgmt();
  $n=(int)$n;
  $data['body'][]="<h2>Manage $item</h2><br />";
  if (loginCheckPermission(USER::MGMT_HMB_DATA))
  {
    _make_html_table($table,$item,$urlPrefix,$n,$data);
    $data['body'][]='<p><a href="'.myUrl("$urlPrefix/add").'">Add New '.$item.'</a></p>';
    $data['body'][]='<p><a href="'.myUrl("$urlPrefix/loaddb").'">Load '.$item.' Data</a></p>';
  }
  else
  {
    $data['body'][] = '<p>You do not have permission for this operation';
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}

function _make_html_table($table,$item,$urlPrefix,$n,&$data) {
	$dbh=getdbh();

	//pagination
	$stmt = $dbh->query("SELECT count(OID) total FROM $table");
	$total=$stmt->fetchColumn();

	$limit=$GLOBALS['pagination']['per_page'];
	$data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
	$data['body'][]=pagination::makePagination($n,$total,myUrl("$urlPrefix/manage"),$GLOBALS['pagination']);

	//table
	$fields="_1st_on,_1st_off,_2nd_on,_2nd_off,_3rd_on,_3rd_off,cycle";
	$stmt = $dbh->query("SELECT OID,CID,$fields FROM $table LIMIT $n,$limit");
	if ($stmt === false) {
		var_dump($dbh->errorInfo());
		return;
	}
	$tablearr[]=explode(',',$fields);
	while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
		$OID=$rs['OID'];
		$CID=$rs['CID'];
		$row=null;
		foreach ($tablearr[0] as $f) 
		{
			$row[]=htmlspecialchars($rs[$f]);
		}
		$row[]=	'<a href="'.myUrl("$urlPrefix/show/$OID/$CID").'">Test</a> | '.
				'<a href="'.myUrl("$urlPrefix/edit/$OID/$CID").'">Edit</a> | '.
				'<a href="javascript:jsconfirm(\'Really Delete '.$item.'?\',\''.
		        myUrl("$urlPrefix/ops_delete/$OID/$CID").'\')">Delete</a>';
		$tablearr[]=$row;
	};
	$data['body'][]=table::makeTable($tablearr);
	$data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}