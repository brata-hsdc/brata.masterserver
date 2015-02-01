
<?php
function _ops_loaddb()
{
	$urlPrefix="mgmt_cts_data";
	$item = "CTSData";
	if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
	{
		// open the csv file for reading
		$file_path = $_FILES ['csv_file'] ['tmp_name'];
		$handle = fopen ( $file_path, 'r' );
		try
		{
			transactionBegin ();
			$o = new CTSData ();
			if ($o->truncateTable () === false) throw new Exception ( "error on truncate of $item" );
			while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE )
			{
				if (count($data) != 8) throw new Exception("wrong number of value in $item record");
				$o = new CTSData ();
				$station = Station::getFromTag($data[0]);
				if ($station === false) throw new Exception("could not find station ".$data[0]);
				$o->set ( 'stationId', $station->get('OID'));
			    $o->set ( '_1st', $data [1] );
			    $o->set ( '_2nd', $data [2] );
			    $o->set ( '_3rd', $data [3] );
			    $o->set ( '_4th', $data [4] );
			    $o->set ( '_5th', $data [5] );
			    $o->set ( 'tolerance', $data [6] );
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



