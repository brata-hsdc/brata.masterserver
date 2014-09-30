<?php
function _test_index($n=0) {
  $n=(int)$n;
  $data['body'][]='<h2>Device Testing</h2><br />';
  //_make_html_table($n,$data);
  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

function _make_html_table($n,&$data) {
  /*
  $store = new Store();
  $allStores = $store->retrieve_many();
     $tablearr[]=explode(',','name,nick name,description');
  foreach ($allStores as $store)
  {
    $OID=$store->get('OID');
//    $CID=$rs['CID'];
    $row=null;
    $row[]=htmlspecialchars($store->get('name'));
    $row[]=htmlspecialchars($store->get('nickName'));
    $row[]=htmlspecialchars($store->get('description'));   
    $row[]='<a href="'.myUrl("device/test_browsetopics/$OID") .'">Enter the Store</a>';
    
    $tablearr[]=$row;
  };
  $data['body'][]=table::makeTable($tablearr);
*/
}