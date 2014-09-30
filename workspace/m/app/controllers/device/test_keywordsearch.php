<?php
function _test_keywordsearch($storeId=0,$keywords="", $n=0) {
  
  if ($keywords != "")
  {

    $keywordsX = urldecode($keywords);
//echo $keywords ."=>" .$keywordsX;
    $keywordsX =  preg_replace('/[^a-zA-Z0-9\s\-]/', '', $keywordsX);  // remove punctuation, keep '-' white space(\s) etc.
    $keywordArray = explode(" ", $keywordsX);
//echo $keywordsX;
    $tmp = new StoreFrontView();
    $whereWhat = $tmp->makeKeywordSearch($storeId,$keywordArray);
    $total = $tmp->count($whereWhat['where'],$whereWhat['what']);
    $limit=$GLOBALS['pagination']['per_page'];
    $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
    $data['body'][]=pagination::makePagination($n,$total,myUrl("device/test_keyword_search_op/$storeId/$keywords"),$GLOBALS['pagination']);

    $tablearr[]=explode(',','title,snip');

    $list = $tmp->retrieve_page($n,$limit,$whereWhat['where'],$whereWhat['what']);
    foreach ($list as $object) {
      $OID=$object->get('OID');
      $row = null;
      $row['title']=htmlspecialchars($object->get('title'));
      $row['ship']=htmlspecialchars($object->get('snip'));
      $row[]='<a href="'.myUrl("device/test_purchase/$OID").'">Purchase</a>';
      $row[]="<p>".$object->get('keywords')."</p>";
      $tablearr[]=$row;
    }
  }

  $fdata['keywords']=$keywords == "" ? "" : urldecode($keywords);
  $fdata['actionUrl']=myUrl("device/test_keyword_search_op/$storeId");
  $form = View::do_fetch(VIEW_PATH.'device/test_keywordsearchform.php',$fdata);
  $data['storeId'] = $storeId;
  $data['body'][] = $form;
  if ($keywords)  $data['body'][]=table::makeTable($tablearr);
  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

