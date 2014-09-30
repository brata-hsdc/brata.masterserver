<?php

function _test_browsenewstories_op()
{
  $storeId=trim($_POST['storeId']);
  $days=trim($_POST['days']);
  redirect("device/test_browsenewstories/$storeId/$days");
}
