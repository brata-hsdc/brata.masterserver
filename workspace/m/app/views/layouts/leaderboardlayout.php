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
   <?php echo (isset($body) && is_array($body)) ? implode("\n",$body) : ''?>
</div></div>
<div class="row"><div class="col-md-12">
<!-- footer -->
<?php echo (isset($foot) && is_array($foot)) ? implode("\n",$foot) : ''?>
<!-- end footer -->
</div></div>

<script src="http://code.jquery.com/jquery.js"></script>
<script src="<?php echo myUrl('js/bootstrap.min.js')?>"></script>
</body>
</html>