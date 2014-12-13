<?php
include_once "sysconfig_data.php";
define('DBHOST',$SYSCONFIG_DBHOST);
define('DBNAME',$SYSCONFIG_DBNAME);
define('DBUSER',$SYSCONFIG_DBUSER);
define('DBPASS',$SYSCONFIG_DBPASS);
$GLOBALS['SYSCONFIG_DEBUG'] = $SYSCONFIG_DEBUG;
$GLOBALS['SYSCONFIG_SENDMAIL'] = $SYSCONFIG_SENDMAIL;
$GLOBALS['SYSCONFIG_PAYPAL_RETURN'] = $SYSCONFIG_PAYPAL_RETURN;
include_once "settings_data.php";
$GLOBALS['SETTINGS_MGMT_BANNER'] = $SETTINGS_MGMT_BANNER;
$GLOBALS['SETTINGS_WRITER_BANNER'] = $SETTINGS_WRITER_BANNER;
$GLOBALS['SETTINGS_SUPPORTEMAIL'] = $SETTINGS_SUPPORTEMAIL;
$GLOBALS['SETTINGS_SUPPORTNUMBER'] = $SETTINGS_SUPPORTNUMBER;
$GLOBALS['SETTINGS_TAXFAXNUMBER'] = $SETTINGS_TAXFAXNUMBER;

//===============================================
// Debug
//===============================================
ini_set('display_errors','On');
error_reporting(E_ALL);
//error_reporting(E_ALL ^ E_STRICT);
function trace($msg) {
	error_log($msg."\n",3,"/var/tmp/m.log");
}

//===============================================
// mod_rewrite
//===============================================
//Please configure via .htaccess or httpd.conf

//===============================================
// Madatory KISSMVC Settings (please configure)
//===============================================
define('APP_PATH','app/'); //with trailing slash pls
#define('WEB_FOLDER','/isms/'); //with trailing slash pls
define('WEB_FOLDER',$SYSCONFIG_WEBFOLDER); //with trailing slash pls

//===============================================
// Other Settings
//===============================================
#define('WEB_DOMAIN','http://localhost'); //with http:// and NO trailing slash pls
define('WEB_DOMAIN',$SYSCONFIG_WEBDOMAIN); //with http:// and NO trailing slash pls
define('VIEW_PATH','app/views/'); //with trailing slash pls

//===============================================
// Includes
//===============================================
require('kissmvc.php');
require('kissex.php');
require(APP_PATH.'inc/functions.php');

//===============================================
// Session
//===============================================
ini_set('session.use_cookies', 1);
ini_set('session.use_only_cookies', 1);
session_start();

//===============================================
// Globals
//===============================================
$GLOBALS['sitename']='M - The Master Server';

//pagination config
$GLOBALS['pagination']['full_tag_open'] = '<span class="pagination">';
$GLOBALS['pagination']['full_tag_close'] = "</span><br />\n<br />\n";
$GLOBALS['pagination']['cur_tag_open'] = '&nbsp;<span>';
$GLOBALS['pagination']['cur_tag_close'] = '</span>';
$GLOBALS['pagination']['first_link'] = '&lt;&lt;';
$GLOBALS['pagination']['last_link'] = '&gt;&gt;';
$GLOBALS['pagination']['num_links'] = 2;
$GLOBALS['pagination']['per_page'] = 5;

//===============================================
// Uncaught Exception Handling
//===============================================s
set_exception_handler('uncaught_exception_handler');

function uncaught_exception_handler($e) {
  ob_end_clean(); //dump out remaining buffered text
  $vars['message']=$e;
  die(View::do_fetch(APP_PATH.'errors/exception_uncaught.php',$vars));
}

function custom_error($msg='') {
  $vars['msg']=$msg;
  die(View::do_fetch(APP_PATH.'errors/custom_error.php',$vars));
}

//===============================================
// Database
//===============================================
function getdbh() {
  if (!isset($GLOBALS['dbh']))
  try {
    //$GLOBALS['dbh'] = new PDO('sqlite:'.APP_PATH.'db/kissmvc.sqlite');
    $connString = sprintf("mysql:host=%s;dbname=%s",DBHOST,DBNAME);
    $dbh = new PDO($connString, DBUSER,DBPASS);
    //$dbh->setAttribute(PDO::MYSQL_ATTR_USE_BUFFERED_QUERY,true);
    $GLOBALS['dbh'] = $dbh;
    $dbh = new PDO($connString, DBUSER, DBPASS);

  } catch (PDOException $e) {
    die('Connection failed: '.$e->getMessage());
  }
  return $GLOBALS['dbh'];
}

function transactionBegin() {
  $dbh =getdbh();
  $dbh->query("SET AUTOCOMMIT=0");
  $dbh->query("BEGIN");
  return $dbh;
}
function transactionCommit() {
  $dbh =getdbh();
  $dbh->query("COMMIT");
  $dbh->query("SET AUTOCOMMIT=1");
  return $dbh;
}

function transactionRollback() {
  $dbh =getdbh();
  $dbh->query("ROLLBACK");
  $dbh->query("SET AUTOCOMMIT=1");
}
/**
 *
 * @convert UNIX TIMESTAMP to MySQL TIMESTAMP
 *
 * @param int $timestamp
 *
 * @return string
 *
 */
function unixToMySQL($timestamp)
{
  return date('Y-m-d H:i:s', $timestamp);
}
//===============================================
// Autoloading for Business Classes
//===============================================
// Assumes Model Classes start with capital letters and Helpers start with lower case letters
function __autoload($classname) {
  //echo "__autoload $classname";
  $a=$classname[0];
  if ($a >= 'A' && $a <='Z')
  require_once(APP_PATH.'models/'.$classname.'.php');
  else
  require_once(APP_PATH.'helpers/'.$classname.'.php');
}

//===============================================
// Start the controller
//===============================================
$controller = new Controller(APP_PATH.'controllers/',WEB_FOLDER,'mgmt_main','index');
