
<?php

function _ops_loaddb() 
{
  $urlPrefix="mgmt_fsl_data";
  $item = "FSLData";
  if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
  {		
    // open the csv file for reading
    $file_path = $_FILES ['csv_file'] ['tmp_name'];
    $handle = fopen ( $file_path, 'r' );
    try 
    {
      transactionBegin ();
      $o = new FSLData ();
      if ($o->truncateTable () === false) throw new Exception ( " truncate $item" );
      while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE ) 
      {
      	if (count($data) != 15) throw new Exception("wrong number of value for $item object");
      	$o = new FSLData ();
      	$o->set ( 'a_tag',  $data [0] );
      	$o->set ( 'a_lat',  $data [1] );
		$o->set ( 'a_lng' , $data [2] );
		$o->set ( 'b_tag',  $data [3] );
		$o->set ( 'b_lat' , $data [4] );
		$o->set ( 'b_lng' , $data [5] );
		$o->set ( 'c_tag',  $data [6] );
		$o->set ( 'c_lat' , $data [7] );
		$o->set ( 'c_lng' , $data [8] );
		$o->set ( 'l_tag',  $data [9] );
		$o->set ( 'l_lat' , $data [10] );
		$o->set ( 'l_lng' , $data [11] );
		$o->set ( 'a_rad',  $data [12] );
		$o->set ( 'b_rad',  $data [13] );
		$o->set ( 'c_rad',  $data [14] );
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

