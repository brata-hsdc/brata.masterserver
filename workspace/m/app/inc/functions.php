<?php
function myUrl($url='',$fullurl=false) {
  $s=$fullurl ? WEB_DOMAIN : '';
  $s.=WEB_FOLDER.$url;
  return $s;
}
function redirectSupport($url,$msg='') {
  if ($msg) $msg="&msg=".urlencode($msg);
  header('Location: '.myUrl($url)."?supportEmail=".urlencode(getSupportEmail()).$msg);
  exit;
}

function redirect($url,$alertmsg='') {
  if ($alertmsg)
  addjAlert($alertmsg,$url);
  header('Location: '.myUrl($url));
  exit;
}
function isSetList($nameList) {
  foreach ($nameList as $name) {
    if ( !isset($_POST[$name])) {
      return false;
    }
  }
  return true;
}
function loginRequireMgmt() {
  if (!isset($_SESSION['mgmt_user']))
  redirect('mgmt_main/login');
}
function loginIsMgmt() {
  return isset($_SESSION['mgmt_user']);
}
function loginCheckPermission($permission) {
  return isset($_SESSION['mgmt_user']) ? $_SESSION['mgmt_user']->isPermissionSet($permission) : false;
}
function loginSetMgmt($user) {
  $_SESSION['mgmt_user']=$user;
}
function loginClearMgmt() {
  unset($_SESSION['mgmt_user']);
}
function loginGetMgmtId() {
  return isset($_SESSION['mgmt_user']) ? $_SESSION['mgmt_user']->get('OID') : 0 ;
}

function isDebug() {
  return isset($GLOBALS['SYSCONFIG_DEBUG']) ? $GLOBALS['SYSCONFIG_DEBUG'] : 0;
}
function getMgmtBanner() {
  return isset($GLOBALS['SETTINGS_MGMT_BANNER']) ? $GLOBALS['SETTINGS_MGMT_BANNER'] : "not set" ;
}
function getMgmtLogo() {
  return isset($GLOBALS['SETTINGS_MGMT_LOGO']) ? $GLOBALS['SETTINGS_MGMT_LOGO'] : "not set" ;
}
function getMgmtFooter() {
  return isset($GLOBALS['SETTINGS_MGMT_FOOTER']) ? $GLOBALS['SETTINGS_MGMT_FOOTER'] : "not set" ;
}
function getWritersBanner() {
  return isset($GLOBALS['SETTINGS_WRITERS_BANNER']) ? $GLOBALS['SETTINGS_WRITERS_BANNER'] : "not set" ;
}
function getWritersLogo() {
  return isset($GLOBALS['SETTINGS_WRITERS_LOGO']) ? $GLOBALS['SETTINGS_WRITERS_LOGO'] : "not set" ;
}
function getWritersFooter() {
  return isset($GLOBALS['SETTINGS_WRITERS_FOOTER']) ? $GLOBALS['SETTINGS_WRITERS_FOOTER'] : "not set" ;
}
function getSupportEmail() {
  return isset($GLOBALS['SETTINGS_SUPPORTEMAIL']) ? $GLOBALS['SETTINGS_SUPPORTEMAIL'] : "not set" ;
}
function getSupportNumber() {
  return isset($GLOBALS['SETTINGS_SUPPORTNUMBER']) ? $GLOBALS['SETTINGS_SUPPORTNUMBER'] : "not set" ;
}
function getTaxFaxNumber() {
  return isset($GLOBALS['SETTINGS_TAXFAXNUMBER']) ? $GLOBALS['SETTINGS_TAXFAXNUMBER'] : "not set" ;
}
function saveSetting($setting,$value)
{
  $fd = fopen("settings_data.php","r");
  $data = "";

  if ($fd)
  {
    $data = fgets($fd);  // skip <?php
    while (!feof($fd))
    {
      $line = fgets($fd);
      $parts=explode("=",$line);
      if ($parts[0] == $setting)
      {
        $line = $setting."='".$value."';\n";
      }
      $data=$data.$line;
    }
    fclose($fd);
    $fd = fopen("settings_data.php","w");
    fwrite($fd,$data);
    fclose($fd);
  }

}

//session must have started
//$uri indicates which uri will activate the alert (substring check)
function addjAlert($msg,$uri='') {
  if ($msg) {
    $s="alert(\"$msg\");";
    $_SESSION['jAlert'][]=array($uri,$s);
  }
}

function getjAlert() {
  if (!isset($_SESSION['jAlert']) || !$_SESSION['jAlert'])
  return '';
  $pageuri=$_SERVER['REQUEST_URI'];
  $current=null;
  $remainder=null;
  foreach ($_SESSION['jAlert'] as $x) {
    $uri=$x[0];
    if (!$uri || strpos($pageuri,$uri)!==false)
    $current[]=$x[1];
    else
    $remainder[]=$x;
  }
  if ($current) {
    if ($remainder)
    $_SESSION['jAlert']=$remainder;
    else
    unset($_SESSION['jAlert']);
    return '<script type="text/javascript">'."\n".implode("\n",$current)."\n</script>\n";
  }
  return '';
}
function generatePassword($length=6,$level=2){

  // as of PHP 4.2 we don't need to seed
  //list($usec, $sec) = explode(' ', microtime());
  //srand((float) $sec + ((float) $usec * 100000));

  $validchars[1] = "0123456789abcdfghjkmnpqrstvwxyz";
  $validchars[2] = "0123456789abcdfghjkmnpqrstvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  $validchars[3] = "0123456789_!@#$%&*()-=+/abcdfghjkmnpqrstvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_!@#$%&*()-=+/";

  $password  = "";
  $counter   = 0;

  while ($counter < $length) {
    $actChar = substr($validchars[$level], mt_rand(0, strlen($validchars[$level])-1), 1);

    // All character must be different
    if (!strstr($password, $actChar)) {
      $password .= $actChar;
      $counter++;
    }
  }

  return $password;
}