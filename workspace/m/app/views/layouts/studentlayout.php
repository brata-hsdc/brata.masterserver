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
    <li><a href="<?php echo myUrl('student/about/whatsnew')?>">What's New</a></li>
    <li><a href="<?php echo myUrl('student/about/todo')?>">To Do</a></li>
    <li><a href="<?php echo myUrl('student/about/version')?>">Version</a></li>
    <li><a href="<?php echo myUrl('student/about/help')?>">Help</a></li>
    </ul>
</div></div>
<div class="row">
   <div class="col-md-4">
   <!--  right side -->
     <li>Below is for Public Access</li>      
      <li><a href="<?php echo myUrl('leader-board/index')?>">View Leader Board</a></li>
     <li>Below is for Student Access</li>
      <li><a href="<?php echo myUrl('student/showevents')?>">Show Events</a></li>
      <li><a href="<?php echo myUrl('student/showlog')?>">Show M's Log</a></li>  
      <li><a href="<?php echo myUrl('student/resetdb') ?>">Reset Database</a></li>
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