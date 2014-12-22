<?php
function mock_set_to_brata($toBrata) {
	$_SESSION['mock_to_brata'] = $toBrata;
}
function mock_get_to_brata_response() {
	if (isset($_SESSION['mock_to_brata'])) return $_SESSION['mock_to_brata'];
	else return "none";
}