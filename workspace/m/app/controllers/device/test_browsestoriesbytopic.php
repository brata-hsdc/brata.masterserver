<?php
function _test_browsestoriesbytopic($storeId=0, $topicId=0,$n=0) {
  //require_device_login();
  $topicId=(int)$topicId;
  $n=(int)$n;

  if ($storeId == 0) redirect("device/test_index","Please enter a store first");
  if ($topicId == 0) redirect("device/test_index","Please select a topic first");

  $topic = new Topic($topicId,-1);
  $topicName = $topic->get('name');

  $data['storeId'][] = $storeId;
  $data['body'][]='<h2>Browse Stories in topic '. $topicName . '</h2><br />';
  _make_html_table($storeId, $topicId, $n, $data);

  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

function _make_html_table($storeId, $topicId, $n, &$data) {

  $where="storeId=? and topicId=?";
  $what=array($storeId,$topicId);
  
  $storeFrontView = new StoreFrontView();
  $total = $storeFrontView->count($where, $what);

  $limit=$GLOBALS['pagination']['per_page'];
  $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
  $data['body'][]=pagination::makePagination($n,$total,myUrl('device/test_browsestoriesbytopic/'.$storeId.'/'.$topicId),$GLOBALS['pagination']);

  //table
  $array = $storeFrontView->retrieve_page($n,$limit,$where,$what);
  $tablearr[]=explode(',','title,writerId,snip');
  foreach ($array as $storeFrontView)
  {
    $OID=$storeFrontView->get('OID');
    $row=null;
    $row[]=htmlspecialchars($storeFrontView->get('title'));
    $row[]=htmlspecialchars($storeFrontView->get('writerId'));    
    $row[]=htmlspecialchars($storeFrontView->get('snip'));
    $row[]='<a href="' . myUrl("device/test_purchase/$OID") . '">Purchase</a>';
    $tablearr[]=$row;
  };

  $data['body'][]=table::makeTable($tablearr);

  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}
