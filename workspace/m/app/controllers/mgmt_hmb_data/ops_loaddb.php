
<?php
function _ops_loaddb()
{
	$urlPrefix="mgmt_hmb_data";
	$item = "HMBData";
	if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
	{
		// open the csv file for reading
		$file_path = $_FILES ['csv_file'] ['tmp_name'];
		$handle = fopen ( $file_path, 'r' );
		try
		{
			transactionBegin ();
			$o = new HMBData ();
			if ($o->truncateTable () === false) throw new Exception ( "truncate $item" );
			while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE )
			{
				if (count($data) != 7) throw new Exception("wrong number of value of $item");
				$o = new HMBData ();
			    $o->set ( '_1st_on' , $data [0] );
			    $o->set ( '_1st_off', $data [1] );
			    $o->set ( '_2nd_on' , $data [2] );
			    $o->set ( '_2nd_off', $data [3] );
			    $o->set ( '_3rd_on' , $data [4] );
			    $o->set ( '_3rd_off', $data [5] );
			    $o->set ( 'cycle'   , $data [6] );
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



