
<?php
function _ops_loaddb()
{
	$urlPrefix="mgmt_cpa_data";
	$item = "CPAData";
	if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
	{
		// open the csv file for reading
		$file_path = $_FILES ['csv_file'] ['tmp_name'];
		$handle = fopen ( $file_path, 'r' );
		try
		{
			transactionBegin ();
			$o = new CPAData ();
			if ($o->truncateTable () === false) throw new Exception ( "CTSData" );
			while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE )
			{
				if (count($data) != 4) throw new Exception("wrong number of values for $item record");
				$o = new CPAData ();
			    $o->set ( 'label'    , $data [0] );
			    $o->set ( 'fence'    , $data [1] );
			    $o->set ( 'building' , $data [2] );
			    $o->set ( 'sum' , $data [3] );
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



