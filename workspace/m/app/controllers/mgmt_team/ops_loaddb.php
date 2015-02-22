
<?php
function generatePin() {
	for ($retry=0;$retry<PIN_RETRY_MAX;$retry++) {
	  $pin = Team::generatePIN();
	  if (Team::getFromPin($pin) === false) return $pin;  // not a duplicate
	}
	return false;
}

function _ops_loaddb()
{
	$urlPrefix="mgmt_team";
	$item = "Team";
	if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] ))
	{
		// open the csv file for reading
		$file_path = $_FILES ['csv_file'] ['tmp_name'];
		$handle = fopen ( $file_path, 'r' );
		try
		{
			transactionBegin ();
			$o = new Team ();
			if ($o->deleteAll () === false) throw new Exception ( "delete all $item" );
			while ( ($data = fgetcsv ( $handle, 1000, ',' )) !== FALSE )
			{
				if (count($data) != 2) throw new Exception("wrong number of value of $item");
				$s = School::getFromName($data[1]);
				if ($s === false) throw new Exception("Can't find shool $data[1]");
				$pin = generatePin();
				if ($pin === false) throw new Exception("Couldn't create unique pin");
				$o = new Team();
				$o->set ( 'name' , $data[0] );
				$o->set ( 'pin'  , $pin);
				$o->set ('schoolId', $s->get('OID'));
			    if ($o->create() === false) throw new Exception ( "Can't create $item object" );						
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



