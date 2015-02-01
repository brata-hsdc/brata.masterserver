
<?php
class ErrorInfo extends Exception
{
	function __construct($msg=null) {
		parent::__construct($msg);
	}
}
//database connect info here
const MAX_LINE = 1000;
function loadCTSData($handle) {
	try {
		transactionBegin ();
		$o = new CTSData ();
		if ($o->truncateTable () === false)
			throw new ErrorInfo ( "CTSData can't truncate table" );

		while ( ($data = fgetcsv ( $handle, MAX_LINE, ',' )) !== false ) {
			if (count($data) == 1 ) break;
			$o = new CTSData ();
			if (($station=Station::getFromTag($data[0])) === false) throw new ErrorInfo("CTSData can't find station $name[0]");
			$o->set ( 'stationId', $station->get('OID'));
			$o->set ( '_1st', $data [1] );
			$o->set ( '_2nd', $data [2] );
			$o->set ( '_3rd', $data [3] );
			$o->set ( '_4th', $data [4] );
			$o->set ( '_5th', $data [5] );
			$o->set ( 'tolerance', $data [6] );
			if ($o->create () === false) {
				transactionRollback ();
				var_dump($data);
				var_dump($o);
				throw new ErrorInfo ( "CTSData create object failed" );
			}
		}
		transactionCommit ();
	} catch ( ErrorInfo $e ) {
		echo $e->getMessage ();
		return false;
	}
	return $data;
}
function loadEXTData($handle) {
	try {
		transactionBegin ();
		$o = new EXTData ();
		if ($o->truncateTable () === false)
			throw new ErrorInfo ( "ExtData" );
		
		while ( ($data = fgetcsv ( $handle, MAX_LINE, ',' )) !== FALSE ) {
			if (count($data) == 1 ) break;
			$o = new EXTData ();
			$o->set ( 'waypoint1_lat', $data [0] );
			$o->set ( 'waypoint1_lng', $data [1] );
			$o->set ( 'waypoint2_lat', $data [2] );
			$o->set ( 'waypoint2_lng', $data [3] );
			$o->set ( 'waypoint3_lat', $data [4] );
			$o->set ( 'waypoint3_lng', $data [5] );
			if ($o->create () === false) {
				transactionRollback ();
				throw new ErrorInfo ( $dbh, $sql );
			}
		}
		transactionCommit ();
	} catch ( ErrorInfo $e ) {
		echo $e->getMessage ();
		return false;
	}
	return $data;
}
//check for file upload
function _loaddb() {
	if (isset ( $_FILES ['csv_file'] ) && is_uploaded_file ( $_FILES ['csv_file'] ['tmp_name'] )) {
		
		// open the csv file for reading
		$file_path = $_FILES ['csv_file'] ['tmp_name'];
		$handle = fopen ( $file_path, 'r' );
		$data = fgetcsv ( $handle, MAX_LINE, ',' ); // get first line which marks the data type
		while ($data !== FALSE ) {
			if    ($data[0] == "EXTData" ) {
				$data = loadEXTData($handle);
			}
			elseif  ($data[0] == "CTSData" ) {	
				$data = loadCTSData($handle);
			} else {
				echo "error missing data marker data=$data";
				break;
			}
		}
		// delete csv file
		unlink ( $file_path );
	} else {
		echo "error no file uploaded";
	}
	redirect("$urlPrefix/manage",$msg);
}

