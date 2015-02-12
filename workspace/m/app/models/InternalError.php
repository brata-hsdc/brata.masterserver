<?php
//
// used signal internal errors up the call chain
class InternalError extends Exception
{
	function __construct($msg,$httpCode=500) {
		$this->httpCode = httpCode;
		parent::__construct($msg);
	}
    function getCode() { return $this->httpCode; }
}