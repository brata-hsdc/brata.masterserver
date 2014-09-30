<?php
function _test_browsenewstories($storeId,$days=30,$n=0) {
  //require_device_login();
  $days=(int)$days;
  $n=(int)$n;

  if ($storeId == 0) redirect("device/test_index","Please select store first");

  $data['storeId'] = $storeId;
  $data['body'][]='<h2>Browse New Stories Days='. $days . '</h2><br />';
  _make_html_table($storeId,$days,$n,$data);
  //$data['body'][]='<p><a href="'.myUrl('mgmt_topic/add').'">Add New Topic</a></p>';

  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}
function _make_form($storeId,$days) {
  $options="";
  for ($i=1;$i<=30;$i++) {
    if ($i==$days)
    $options .="<option selected>".$i;
    else
    $options .="<option>".$i;
  }
  return "<table>"
  ."<form method=post action='".myUrl("device/test_browsenewstories_op")."' >"
  ."<input type=hidden name=storeId value=$storeId />"
  ."<tr>"
  ."  <td>Days</td>"
  ."  <td><select name=days>".$options."</select></td>"
  ."  <td><input type=submit value=Submit /></td>"
  ."</tr>"
  ."</form>"
  ."</table>"
  ;
}
function _make_html_table($storeId, $days,$n,&$data) {
  $tmp=new StoreFrontView();

  $where = "storeId=? and submitDate>=?";
  $timeStamp=unixToMySQL(time() - ($days * 24 * 60 * 60)); // days back
  $what = array($storeId,$timeStamp);
  //pagination
  $total=$tmp->count($where,$what);

  $limit=$GLOBALS['pagination']['per_page'];
  $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
  $data['body'][]=pagination::makePagination($n,$total,myUrl('device/test_browsestories/'.$storeId.'/'.$days),$GLOBALS['pagination']);

  //table
  $list = $tmp->retrieve_page($n,$limit,$where,$what);
  $tablearr[]=explode(',','title,writerId,snip');
  foreach ($list as $tmp)  {
    $OID=$tmp->get('OID');
    $row=null;
    $row[]=htmlspecialchars($tmp->get('title'));
    $row[]=htmlspecialchars($tmp->get('writerId'));
    $row[]=htmlspecialchars($tmp->get('snip'));    
    $row[]='<a href="' . myUrl("device/test_purchase/$OID") . '">Purchase</a>';
    $tablearr[]=$row;
  };

  //  $data['body'][] = View::do_fetch(VIEW_PATH.'device/keywordsearchform.php',$fdata);
  $data['body'][]=table::makeTable($tablearr);
  $data['body'][]=_make_form($storeId,$days);

  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}
