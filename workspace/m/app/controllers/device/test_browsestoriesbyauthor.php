<?php
function _test_browsestoriesbyauthor($storeId,$profileId=0,$n=0) {
  //require_device_login();
  $profileId=(int)$profileId;
  $n=(int)$n;

  if ($profileId == 0) redirect("device/test_browsestoriesbyauthor","Please select a writer first");

  $writerProfile = new WriterProfile($profileId,-1);

  $data['body'][]='<h2>Browse Stories by '. $writerProfile->get('name') . '</h2><br />';
  _make_html_table($storeId,$profileId,$n,$data);

  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

function _make_html_table($storeId,$profileId,$n,&$data) {
  $dbh=getdbh();

  //pagination
  $stmt = $dbh->query("SELECT count(OID) total FROM v_storefront where storeId=".$storeId." and writerId=".$profileId);
  $total=$stmt->fetchColumn();

  $limit=$GLOBALS['pagination']['per_page'];
  $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
  $data['body'][]=pagination::makePagination($n,$total,myUrl('device/test_browsestoriesbyauthor/'.$storeId.'/'.$profileId),$GLOBALS['pagination']);

  //table
  $stmt = $dbh->query("SELECT * FROM v_storefront where storeId=".$storeId." and writerId=".$profileId."  LIMIT $n,$limit");
  $tablearr[]=explode(',','Title,Snip');
  while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $OID=$rs['OID'];
    //    $CID=$rs['CID'];
    $row=null;
    $row[]=htmlspecialchars($rs['title']);
    $row[]=htmlspecialchars($rs['snip']);
    $row[]='<a href="' . myUrl("device/test_purchase/$OID") . '">Purchase</a>';
    $tablearr[]=$row;
  };

  //$fdata['writerId'] = $writerId;
  //$fdata['keywords']="";
  //$data['body'][] = View::do_fetch(VIEW_PATH.'device/keywordsearchform.php',$fdata);
  $data['storeId']=$storeId;
  $data['body'][]=table::makeTable($tablearr);

  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}
