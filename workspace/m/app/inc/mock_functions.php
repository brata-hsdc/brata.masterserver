<?php
function mock_set_to_brata($toBrata) {
	$_SESSION['mock_to_brata'] = $toBrata;
}
function mock_get_to_brata_response() {
	if (isset($_SESSION['mock_to_brata'])) return $_SESSION['mock_to_brata'];
	else return "none";
}
function mock_set_to_rpi($torPI) {
	$_SESSION['mock_to_rpi'] = $torPIB;
}
function mock_get_to_rpi_response() {
	if (isset($_SESSION['mock_to_rpi'])) return $_SESSION['mock_to_rpi'];
	else return "none";
}