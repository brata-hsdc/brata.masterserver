
<?php

function _ops_loaddb() 
{
  $urlPrefix="mgmt_ext_data";
  $item = "EXTData";
  if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
  {		
    // open the csv file for reading
    $file_path = $_FILES ['csv_file'] ['tmp_name'];
    $handle = fopen ( $file_path, 'r' );
    try 
    {
      transactionBegin ();
      $o = new EXTData ();
      if ($o->truncateTable () === false) throw new Exception ( " truncate $item" );
      while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE ) 
      {
      	if (count($data) != 9) throw new Exception("wrong number of value for $item object");
      	$o = new EXTData ();
      	$o->set ( 'a_lat',  $data [0] );
		$o->set ( 'a_lng' , $data [1] );
		$o->set ( 'b_lat' , $data [2] );
		$o->set ( 'b_lng' , $data [3] );
		$o->set ( 'c_lat' , $data [4] );
		$o->set ( 'c_lng' , $data [5] );
		$o->set ( 't_lat' , $data [6] );
		$o->set ( 't_lng' , $data [7] );
		$o->set ( 'height', $data [8] );
		if ($o->create () === false) throw new Execption ( "Can't create $item object" );
	  }
      transactionCommit ();
      $msg = "Load $item completed";
    } 
    catch ( Exception $e ) 
    {
      transactionRollback ();
	  $msg = "caught exception ".$e->getMessage ();
	}
    // delete csv file
    unlink ( $file_path );
  } 
  else 
  {
    $msg = "error no file uploaded";
  }
  redirect("$urlPrefix/manage",$msg);
}

