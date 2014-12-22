<?php
function mock_set_brata_response($toBrata) {
	$_SESSION['mock_brata'] = $toBrata;
}
function mock_get_brata_response() {
	trace("get to brata isset=".isset($_SESSION['mock_brata']));
	if (isset($_SESSION['mock_to_brata'])) return $_SESSION['mock_brata'];
	else return "none";
}
function mock_set_rpi_response($torPI) {
	$_SESSION['mock_rpi'] = $torPIB;
}
function mock_get_rpi_response() {
	if (isset($_SESSION['mock_rpi'])) return $_SESSION['mock_rpi'];
	else return "none";
}