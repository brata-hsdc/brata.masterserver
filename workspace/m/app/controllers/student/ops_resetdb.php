<?php


function _ops_resetdb() {

  try
  {
    $dbh=getdbh();

   redirect('TODO implement me student','Database Initialized test data!');
    
  }
  catch(ErrorInfo $e)
  {
    echo $e->getMessage();
  }

}
