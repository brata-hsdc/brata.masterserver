
<?php

function _ops_loaddb() 
{
  $urlPrefix="mgmt_ext_data";
  if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
  {		
    // open the csv file for reading
    $file_path = $_FILES ['csv_file'] ['tmp_name'];
    $handle = fopen ( $file_path, 'r' );
    try 
    {
      transactionBegin ();
      $o = new EXTData ();
      if ($o->truncateTable () === false) throw new Exception ( "ExtData" );
      while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE ) 
      {
      	if (count($data) != 6) throw new Exception("wrong number of value");
      	if (count($data) != 6) continue;
      	$o = new EXTData ();
      	$o->set ( 'waypoint1_lat', $data [0] );
		$o->set ( 'waypoint1_lng', $data [1] );
		$o->set ( 'waypoint2_lat', $data [2] );
		$o->set ( 'waypoint2_lng', $data [3] );
		$o->set ( 'waypoint3_lat', $data [4] );
		$o->set ( 'waypoint3_lng', $data [5] );
		if ($o->create () === false) throw new Execption ( "Can't create EXTData object" );
	  }
      transactionCommit ();
      $msg = "Load EXTData completed";
    } 
    catch ( Exception $e ) 
    {
      transactionRollback ();
	  $msg = "caught exception ".$e->getMessage ();
	  echo $msg;
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

