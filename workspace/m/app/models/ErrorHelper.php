<?php
class ErrorHelper {

  protected $data = array ();

  function __construct() {
     
  }
  function get($key) {
    if (isset($this->data[$key])) return $this->data[$key];
    return "";
  }

  function set($key, $val) {
    $this->data[$key] = $val;
    return $this;
  }
  function hasErrors() {
    return sizeof($this->data) != 0;
  }
}
