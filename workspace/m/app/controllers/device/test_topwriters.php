<?php
function _test_topwriters($storeId=0,$n=0) {
  
  if ($storeId == 0) redirect("device/test_index","Please enter a store first");
  //require_device_login();
  $n=(int)$n;
  $data['body'][]='<h2>Top 10 Authors</h2><br />';
  _make_html_table($storeId,$n,$data);
  //$data['body'][]='<p><a href="'.myUrl('mgmt_topic/add').'">Add New Topic</a></p>';

  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

function _make_html_table($storeId,$n,&$data) {
  $dbh=getdbh();


  //table
  $stmt = $dbh->query("SELECT * FROM v_topwriters where storeId=$storeId LIMIT 0,10");//  LIMIT $n,$limit");
  $tablearr[]=explode(',','Total Sales,Author');
  while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $OID = $rs['writerId'];
    $row=null;
    $row[]=htmlspecialchars($rs['TotalCount']);
    $row[]=htmlspecialchars($rs['name']);
    $row[]='<a href="' . myUrl("device/test_browsestoriesbyauthor/$storeId/$OID") . '">Browse Stories</a>';
    $tablearr[]=$row;
  };
  $data['storeId']=$storeId;
  $data['body'][]=table::makeTable($tablearr);
  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}