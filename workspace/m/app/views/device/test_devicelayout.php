<?php
//$device_id=isset($_SESSION['device_id']) ? $_SESSION['device_id'] : 0;
$pagetitle=isset($pagename) ? $GLOBALS['sitename'].' - '.$pagename : $GLOBALS['sitename'];
$jalert[]=getjAlert();
header("Content-Type: text/html; charset=UTF-8");
header("Expires: " . gmdate('D, d M Y H:i:s \G\M\T') );
header("Cache-Control: no-cache");
header("Pragma: no-cache");
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title><?php echo $pagetitle?></title>
<style type="text/css">
  @import "<?php echo myUrl('css/device-reset.css')?>";
  @import "<?php echo myUrl('css/device-text.css')?>";
  @import "<?php echo myUrl('css/device-2col.css')?>";
</style>
<?php echo (isset($head) && is_array($head)) ? implode("\n",$head) : ''?>
</head>
<body>
<div id="wrap">
  <div id="header"><h1><a href="<?php echo myURL('')?> " >M's Home</a> - M Device Test Framework </h1></div>
  <div id="nav">
    <ul>
    <!-- 
      <li><a href="<?php echo myUrl('mgmt_main')?>">Main</a></li>
      <li><a href="<?php echo myUrl('users/manage')?>">Manage Users</a></li>
            <li><a href="<?php echo myUrl('writers/index')?>">Writer's Page</a></li>
     -->

    </ul>
  </div>
  <div id="main">
<?php echo (isset($body) && is_array($body)) ? implode("\n",$body) : ''?>
  </div>
  <div id="sidebar">
    <h3>Device</h3>
    <ul>
      <li>Test Links</li>
      <li><a href="<?php echo myUrl('device/test_rpi_contact')?>">Test Contact</a></li>   
    </ul>
<?php
if (isset($leftnav) && is_array($leftnav))
  foreach ($leftnav as $blockhtml)
    echo "$blockhtml\n";
?>
  </div>
  <div id="footer">
    <?php echo (isset($foot) && is_array($foot)) ? implode("\n",$foot) : '<p>Footer </p>'?>
  </div>
</div>
<?php echo (isset($jalert) && is_array($jalert)) ? implode("\n",$jalert) : ''?>
</body>
</html>