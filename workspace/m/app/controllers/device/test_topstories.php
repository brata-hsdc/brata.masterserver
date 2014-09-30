<?php
function _test_topstories($storeId=0,$n=0) {
  //require_device_login();
  if ($storeId == 0) redirect("device/test_index","Please enter a store first");
  $n=(int)$n;
  $data['body'][]='<h2>Top 10 Stories</h2><br />';
  _make_html_table($storeId,$n,$data);
  //$data['body'][]='<p><a href="'.myUrl('mgmt_topic/add').'">Add New Topic</a></p>';

  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

function _make_html_table($storeId,$n,&$data) {
  $dbh=getdbh();

  //table
  $stmt = $dbh->query("SELECT * FROM v_topstories where storeId=$storeId LIMIT 0,10");
  $tablearr[]=explode(',','TotalCount,Title,Snip,Author');
  while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $OID=$rs['storyId'];
    $row=null;
    $row[]=htmlspecialchars($rs['TotalCount']);
    $row[]=htmlspecialchars($rs['title']);
    $row[]=htmlspecialchars($rs['snip']);
    $row[]=htmlspecialchars($rs['name']);
    $row[]='<a href="' . myUrl("device/test_purchase/$OID") . '">Purchase</a>';
    $tablearr[]=$row;
  };
  $data['storeId']=$storeId;
  $data['body'][]=table::makeTable($tablearr);
  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}