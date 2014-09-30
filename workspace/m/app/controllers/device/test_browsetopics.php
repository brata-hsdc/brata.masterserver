<?php
function _test_browsetopics($storeId=0,$n=0) {
  
  if ($storeId == 0) redirect("device/test_index","Please enter a store first");
  $data['storeId'] = $storeId;
  $storeName = Store::getStoreNameFromId($storeId);
  $n=(int)$n;
  $data['body'][]='<h2>Browsing Topics in ' . $storeName . '</h2><br />';
  _make_html_table($storeId,$n,$data);
  //$data['body'][]='<p><a href="'.myUrl('mgmt_topic/add').'">Add New Topic</a></p>';

  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

function _make_html_table($storeId, $n,&$data) {

  $tmp = new Topic();
  $where = "OID in (select topicId from v_storefront where storeId=?)";
  $what=array($storeId);
  //pagination
  $total=$tmp->count($where,$what);
  
  $limit=$GLOBALS['pagination']['per_page'];
  $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
  $data['body'][]=pagination::makePagination($n,$total,myUrl('device/test_browsetopics/'.$storeId),$GLOBALS['pagination']);

  //table
  $list = $tmp->retrieve_page($n,$limit,$where,$what);
  $tablearr[]=explode(',','name,description');
  foreach ($list as $tmp) {
    $OID=$tmp->get('OID');
    $row=null;
    $row[]=htmlspecialchars($tmp->get('name'));
    $row[]=htmlspecialchars($tmp->get('description'));
    $row[]='<a href="' . myUrl("device/test_browsestoriesbytopic/$storeId/$OID") . '">Browse</a>';
    $tablearr[]=$row;
  };
  $data['body'][]=table::makeTable($tablearr);
  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}