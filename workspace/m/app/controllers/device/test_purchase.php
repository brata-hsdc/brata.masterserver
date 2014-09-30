<?php

function _test_purchase($storyId=0)
{
  $object=new SmsStory();
  $object->retrieve($storyId,-1);  // -1 means get any version

  if (!$object->exists())
  {
    $data['body'][]='<p>SMS Story Not Found!</p>';
  }
  else
  {
    $storeId  = $object->get('storeId');
    $writerId = $object->get('writerId');
    $profileId = $object->get('profileId');
    $purchase = new Purchase($storeId, $storyId, $writerId, $profileId, $object->get('price') );
    $account = WriterAccount::getAccountFromWriterId($writerId);
    if ($account === false)
    {
      $data['body'][]='<p>Writer Account Not Found!</p>';
    }
    else
    {
  	   $account->creditSale($purchase->get('price'));
  	   TransactionBegin();
  	   if ( $purchase->create() === false || $account->update() === false )
  	   {
  	   	var_dump($purchase);
  	     TransactionRollback();
  	     $data['body'][]='<p>Database error purchase creation or account update!</p>';
  	   }
  	   else
  	   {
  	     TransactionCommit();
  	     $story= SmsStoryBody::getBodyFromStoryId($storyId);
  	     $data['body'][]='<h2>Story Purchased</h2>';
  	     $data['body'][]=$story->makeHtml();
  	   }
    }
  }
  View::do_dump(VIEW_PATH.'device/test_devicelayout.php',$data);
}