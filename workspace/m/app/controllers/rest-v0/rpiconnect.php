<?php
include_once "app/controllers/rest-v0/functions.php";
function _rpiconnect()
{
    $json = getJsonObjectFromRequest();
    if ($json === NULL) return;
	// output
	$dbh = getdbh();
	$stmt = $dbh->query('SELECT count(OID) total FROM t_user');
	$total=$stmt->fetchColumn();
	$jsonObject = array('total' => $total, 'b' => array("b.1"=> 4.0, "b.2"=> 4.1), 'c' => 3, 'd' => 4, 'e' => array(1,2,3,4));
	sendJsonObject($jsonObject);
	
}