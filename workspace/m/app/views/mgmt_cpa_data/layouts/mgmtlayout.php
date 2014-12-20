<?php
  $authoid=isset($_SESSION['authoid']) ? $_SESSION['authoid'] : 0;
  $pagetitle=isset($pagename) ? $GLOBALS['sitename'].' - '.$pagename : $GLOBALS['sitename'];
  $foot[]=getjAlert();
  
  header("Content-Type: text/html; charset=UTF-8");
  header("Expires: " . gmdate('D, d M Y H:i:s \G\M\T') );
  header("Cache-Control: no-cache");
  header("Pragma: no-cache");
?>
<!DOCTYPE html>
<html>
<head>
<title><?php echo $pagetitle?></title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Bootstrap -->
<link href="<?php echo myUrl('css/bootstrap.min.css')?>" rel="stylesheet" media="screen">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php echo (isset($head) && is_array($head)) ? implode("\n",$head) : ''?>
</head>
<body>
<div class="row"><div class="col-md-12"><h1><a href="/m">M</a> - The Master Server</h1></div></div>

<div class="row"><div class="col-md-12">
<!--  top bar -->
    <ul class="nav nav-pills pull-right" >
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
</div></div>
<div class="row">
   <div class="col-md-4">
   <!--  right side -->
    <h3>Manage</h3>
    <ul>      
      <li><a href="<?php echo myUrl('mgmt_school/manage')?>">Schools</a></li>
      <li><a href="<?php echo myUrl('mgmt_team/manage')?>">Teams</a></li>
      <li><a href="<?php echo myUrl('mgmt_stationtype/manage')?>">Station Types</a></li>
      <li><a href="<?php echo myUrl('mgmt_station/manage')?>">Stations</a></li>
      <li><a href="<?php echo myUrl('mgmt_rpi/manage')?>">rPI</a></li>
      <li><a href="<?php echo myUrl('mgmt_cts_data/manage')?>">CTS Data</a></li>
      <li><a href="<?php echo myUrl('mgmt_fsl_data/manage')?>">FSL Data</a></li>      
      <li><a href="<?php echo myUrl('mgmt_hmb_data/manage')?>">HMB Data</a></li>
      <li><a href="<?php echo myUrl('mgmt_cpa_data/manage')?>">CPA Data</a></li>
      <li><a href="<?php echo myUrl('mgmt_ext_data/manage')?>">EXT Data</a></li>                   
      <li><a href="<?php echo myUrl('mgmt_user/manage')?> ">Users</a></li>
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
    </ul></div><!-- end right side -->
   <div class="col-md-8"><!-- left side -->
   <?php echo (isset($body) && is_array($body)) ? implode("\n",$body) : ''?>
   </div> <!-- end left side -->
</div>
<div class="row"><div class="col-md-12">
<!-- footer -->
<?php echo (isset($foot) && is_array($foot)) ? implode("\n",$foot) : ''?>
<!-- end footer -->
</div></div>

<script src="http://code.jquery.com/jquery.js"></script>
<script src="<?php echo myUrl('js/bootstrap.min.js')?>"></script>
</body>
</html>