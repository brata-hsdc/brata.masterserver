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
<?php echo (isset($head) && is_array($head)) ? implode("\n",$head) : ''?>
</head>
<body>
<div class="row-fluid"><div class="span12"><h1><a href="/staff2_demo">Staff II Demo</a> - Simple Web Site for Staff 2 Demo </h1></div></div>

<div class="row-fluid"><div class="span12">
<!--  top bar -->
    <ul class="nav nav-pills pull-right" >
      <li><a href="<?php echo myUrl('main')?>">Main</a></li>
      <li><a href="<?php echo myUrl('users/manage')?>">Manage Users</a></li>
      <li><a href="<?php echo myUrl('main/resetdb')?>">Reset DB</a></li>
<?php
  if ($authoid)
    echo '<li><a href="'.myUrl('ops/logout').'">Logout</a></li>'."\n";
  else
    echo '<li><a href="'.myUrl('main/login').'">Login</a></li>'."\n";  
?>
    </ul>
</div></div>
<div class="row-fluid">
   <div class="span4">
   <!--  right side -->
    <h3>Main Menu</h3>
    <ul>
      <li>These are for demo support</li>
      <li><a href="<?php echo myUrl('tweets') ?>">Manage Mock Tweets</a></li>
      <li><a href="<?php echo myUrl('apan_query') ?>">Manage APAN Queries</a></li>
      <li><a href="<?php echo myUrl('keywords') ?>">Manage Keywords</a></li>
      <li><a href="<?php echo myUrl('keywords/tweet_report') ?>">Create Tweets by keyword report</a></li>
      <li><a href="<?php echo myUrl('keywords/suspect_tweet_report') ?>">Create Suspect (tweets with no keywords) report</a></li>
      <li><a href="<?php echo myUrl('keywords/apan_report') ?>">Create APAN by keyword report</a></li>            
      <li><a href="<?php echo myUrl('mock_cron/apan_report') ?>">Create Apan Cron Report</a></li>
      <li><a href="<?php echo myUrl('mock_cron/tweet_report') ?>">Create Tweet Cron Report</a></li>
      <li>These are for demo prep</li>
      <li><a href="<?php echo myUrl('apan_query/fill_cache') ?>">Fill Cache</a></li>
      <li><a href="<?php echo myUrl('apan_query/generate') ?>">Generate APAN Queries</a></li>
      <li>These are for testing</li>
      <li><a href="<?php echo myUrl('apan_test') ?>">Test APAN Search</a></li>
      <li><a href="<?php echo myUrl('dib_test') ?>">Test DIB Search</a></li>
      <li><a href="<?php echo myUrl('mock_cron/mock_cron') ?>">Test Mock Cron</a></li>
      <li><a href="#">TODO</a></li>
      <li><a href="#">TODO</a></li>
      <li><a href="#">TODO</a></li>
      <li><a href="<?php echo myUrl('main/endsession') ?>">Clear Session Data</a></li>
    </ul>
   </div> <!-- end right side -->
   <div class="span8"><!-- left side -->
   <?php echo (isset($body) && is_array($body)) ? implode("\n",$body) : ''?>
   </div> <!-- end left side -->
</div>
<div class="row-fluid"><div class="span12">
<!-- footer -->
<?php echo (isset($foot) && is_array($foot)) ? implode("\n",$foot) : ''?>
<!-- end footer -->
</div></div>

<script src="http://code.jquery.com/jquery.js"></script>
<script src="<?php echo myUrl('js/bootstrap.min.js')?>"></script>
</body>
</html>