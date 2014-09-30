<?php
function _test_authorsearch($storeId=0,$author="", $n=0) {
  
  if ($author != "")
  {

    $authorX = urldecode($author);
    $autorX =  preg_replace('/[^a-zA-Z0-9\s]/', '', $authorX);  // remove punctuation, keep white space(\s) etc.

    $tmp = new WriterProfile();
    $total = $tmp->count("name rlike ?" , $authorX);
    $limit=$GLOBALS['pagination']['per_page'];
    $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
    $data['body'][]=pagination::makePagination($n,$total,myUrl("device/test_author_search_op/$storeId/$author"),$GLOBALS['pagination']);

    $tablearr[]=explode(',','name');

    $list = $tmp->retrieve_page($n,$limit,"name rlike ?", $authorX);
    foreach ($list as $object) {
      $OID=$object->get('OID');
      $row = null;
      $row['title']=htmlspecialchars($object->get('name'));
      $row[]='<a href="'.myUrl("device/test_browsestoriesbyauthor/$storeId/$OID").'">Browse Stories</a>';
      //$row[]="<p>".$object->get('keywords')."</p>";
      $tablearr[]=$row;
    }
  }

  $fdata['author']=$author == "" ? "" : urldecode($author);
  $fdata['actionUrl']=myUrl("device/test_author_search_op/$storeId");
  $form = View::do_fetch(VIEW_PATH.'device/test_authorsearchform.php',$fdata);
  $data['storeId'] = $storeId;
  $data['body'][] = $form;
  if ($author)  $data['body'][]=table::makeTable($tablearr);
  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}

/* search store front
 if ($author != "")
  {

    $authorX = urldecode($author);
    $autorX =  preg_replace('/[^a-zA-Z0-9\s]/', '', $authorX);  // remove punctuation, keep white space(\s) etc.

    $tmp = new StoreFrontView();
    $whereWhat = $tmp->makeAuthorSearch($storeId,$autorX);
    $total = $tmp->count($whereWhat['where'],$whereWhat['what']);
    $limit=$GLOBALS['pagination']['per_page'];
    $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
    $data['body'][]=pagination::makePagination($n,$total,myUrl("device/test_author_search_op/$storeId/$author"),$GLOBALS['pagination']);

    $tablearr[]=explode(',','title,snip');

    $list = $tmp->retrieve_page($n,$limit,$whereWhat['where'],$whereWhat['what']);
    foreach ($list as $object) {
      $OID=$object->get('OID');
      $row = null;
      $row['title']=htmlspecialchars($object->get('title'));
      $row['ship']=htmlspecialchars($object->get('snip'));
      $row[]='<a href="'.myUrl("device/test_purchase/$OID").'">Purchase</a>';
      //$row[]="<p>".$object->get('keywords')."</p>";
      $tablearr[]=$row;
    }
  }

  $fdata['author']=$author == "" ? "" : urldecode($author);
  $fdata['actionUrl']=myUrl("device/test_author_search_op/$storeId");
  $form = View::do_fetch(VIEW_PATH.'device/test_authorsearchform.php',$fdata);
  $data['storeId'] = $storeId;
  $data['body'][] = $form;
  if ($author)  $data['body'][]=table::makeTable($tablearr);
  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
*/
