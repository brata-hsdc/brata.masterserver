<?php
$authuid=isset($_SESSION['authuid']) ? $_SESSION['authuid'] : 0;
$pagetitle=isset($pagename) ? $GLOBALS['sitename'].' - '.$pagename : $GLOBALS['sitename'];
$foot[]=getjAlert();
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title><?php echo $pagetitle?></title>
<style type="text/css">
  @import "<?php echo myUrl('css/reset.css')?>";
  @import "<?php echo myUrl('css/text.css')?>";
  @import "<?php echo myUrl('css/2col.css')?>";
</style>
<?php echo (isset($head) && is_array($head)) ? implode("\n",$head) : ''?>
</head>
<body>
<div id="wrap">
  <div id="header"><h1><a href="/m">M</a> - The Master Server</h1></div>
  <div id="nav">
    <ul>
    <!-- 
      <li><a href="<?php echo myUrl('mgmt_main')?>">Main</a></li>
    -->
    <li><a href="<?php echo myUrl('mgmt_main/about/whatsnew')?>">What's New</a></li>
    <li><a href="<?php echo myUrl('mgmt_main/about/todo')?>">To Do</a></li>
    <li><a href="<?php echo myUrl('mgmt_main/about/version')?>">Version</a></li>
    <li><a href="<?php echo myUrl('mgmt_main/about/help')?>">Help</a></li>
<?php
  if (loginIsMgmt())
    echo '<li><a href="'.myUrl('ops/mgmt_logout').'">Logout</a></li>'."\n";
  else
    echo '<li><a href="'.myUrl('mgmt_main/login').'">Login</a></li>'."\n";  
?>
    </ul>
  </div>
  <div id="main">
<?php echo (isset($body) && is_array($body)) ? implode("\n",$body) : ''?>
  </div>
<div id="sidebar">
    <h3>Manage</h3>
    <ul>      
      <li><a href="<?php echo myUrl('mgmt_school/manage')?>">Schools</a></li>
      <li><a href="<?php echo myUrl('mgmt_team/manage')?>">Teams</a></li>
      <li><a href="<?php echo myUrl('mgmt_waypoint/manage')?>">Way Points</a></li>
      <li><a href="<?php echo myUrl('mgmt_message/manage')?>">Messages</a></li>
      <li><a href="<?php echo myUrl('mgmt_stationtype/manage')?>">Station Types</a></li>
      <li><a href="<?php echo myUrl('mgmt_station/manage')?>">Stations</a></li>
      <li><a href="<?php echo myUrl('mgmt_rpi/manage')?>">rPI</a></li>
      <li><a href="<?php echo myUrl('mgmt_cts_data/manage')?>">CTS Data</a></li>
      <li><a href="<?php echo myUrl('mgmt_hmb_data/manage')?>">HMB Data</a></li>
      <li><a href="<?php echo myUrl('mgmt_cpa_data/manage')?>">CPA Data</a></li>
      <li><a href="<?php echo myUrl('mgmt_ext_data/manage')?>">EXT Data</a></li>                   
      <li><a href="<?php echo myUrl('mgmt_user/manage')?> ">Users</a></li>
      <li><a href="<?php echo myUrl('mgmt_website/manage')?>">Web Site</a></li>
      <li>Below is for Public Access</li>      
      <li><a href="<?php echo myUrl('leader-board/index')?>">View Leader Board</a></li>
      <li><a href="<?php echo myUrl('viewscores')?>">View Scores</a></li>
<?php if ( isDebug() ) { ?>      
      <li>Below is for testing</li>
      <li><a href="<?php echo myUrl('test_brata/index')?>">Brata Testing</a></li> 
      <li><a href="<?php echo myUrl('test_event/manage')?>">Event Testing</a></li> 
      <li><a href="<?php echo myUrl('device/test_index')?>">Device Testing</a></li> 
      <li><a href="<?php echo myUrl('mgmt_main/resetdb') ?>">Reset Database</a></li>
<?php  } ?>      
    </ul>
<?php
if (isset($leftnav) && is_array($leftnav))
  foreach ($leftnav as $blockhtml)
    echo "$blockhtml\n";
?>
  </div>
  <div id="footer">
    <p>Footer</p>
  </div>
</div>
<?php echo (isset($foot) && is_array($foot)) ? implode("\n",$foot) : ''?>
</body>
</html>