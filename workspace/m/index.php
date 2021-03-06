<?php
include_once "sysconfig_data.php"; 
define('DBHOST',$SYSCONFIG_DBHOST);
define('DBNAME',$SYSCONFIG_DBNAME);
define('DBUSER',$SYSCONFIG_DBUSER);
define('DBPASS',$SYSCONFIG_DBPASS);
define('PIN_RETRY_MAX',1000);
$GLOBALS['SYSCONFIG_DEBUG'] = $SYSCONFIG_DEBUG;
$GLOBALS['SYSCONFIG_SENDMAIL'] = $SYSCONFIG_SENDMAIL;
$GLOBALS['LOGLEVEL'] = $SYSCONFIG_LOGLEVEL;
$GLOBALS['LOGFILE'] = $SYSCONFIG_LOGFILE;
$GLOBALS['SYSCONFIG_STUDENT'] = $SYSCONFIG_STUDENT;
$GLOBALS['leaderBoardRefresh'] = $SYSCONFIG_LEADERBOARD_REFRESH;

function isStudentServer() {
	return $GLOBALS['SYSCONFIG_STUDENT'] == 1;
}

//===============================================
// Debug
//===============================================
ini_set('display_errors','On');
error_reporting(E_ALL);
//error_reporting(E_ALL ^ E_STRICT);
define("ERROR",1);
define("WARN",2);
define("INFO",3);
define("DEBUG",4);
define("TRACE",5);
function logit($lvl,$file,$line,$fun,$msg) {
	if ($lvl >= $GLOBALS['LOGLEVEL']) {
    	error_log($file."|".$line."|".$fun."|".$msg."\n",3,"/tmp/m.log");
	}
}
function trace($msg,$file="",$line="",$fun="") {
	logit(TRACE,$file,$line,$fun,$msg);
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
$GLOBALS['pagination']['per_page'] = 25;

//===============================================
// Uncaught Exception Handling
//===============================================s
set_exception_handler('uncaught_exception_handler');

function uncaught_exception_handler($e) {
  ob_end_clean(); //dump out remaining buffered text
  $vars['message']=$e;
  die(View::do_fetch(VIEW_PATH.'errors/exception_uncaught.php',$vars));
}

function custom_error($msg='') {
  $vars['msg']=$msg;
  die(View::do_fetch(VIEW_PATH.'errors/custom_error.php',$vars));
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
if (isStudentServer()) {	
  $controller = new Controller(APP_PATH.'controllers/',WEB_FOLDER,'student','index');
} else {
  $controller = new Controller(APP_PATH.'controllers/',WEB_FOLDER,'mgmt_main','index');
}
