<?php

function _test_author_search_op($storeId,$author="",$n=0)
{
  if (isset($_POST['author'])) $author=urlencode($_POST['author']);
  //echo $keywords;
  redirect("device/test_authorsearch/$storeId/$author/$n");
}
