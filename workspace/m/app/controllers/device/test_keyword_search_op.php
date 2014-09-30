<?php

function _test_keyword_search_op($storeId,$keywords="",$n=0)
{
  if (isset($_POST['keywords'])) $keywords=urlencode($_POST['keywords']);
  //echo $keywords;
  redirect("device/test_keywordsearch/$storeId/$keywords/$n");
}
