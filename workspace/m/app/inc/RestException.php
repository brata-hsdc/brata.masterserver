<?php
// used to capture HTTP status code and message when processing REST API
class RestException extends Exception {
	public $statusCode;
	public $statusMsg;
	
	function __construct($statusCode,$statusMsg) {
		$this->statusCode = $statusCode;
		$this->statusMsg = $statusMsg;
	}
}