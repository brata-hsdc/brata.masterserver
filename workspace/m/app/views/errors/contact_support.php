<?php 
if ( isset($_GET['msg']) )
   $msg = urldecode($_GET['msg']);
else
   $msg = "internal error not redirected";
   
 if ( isset($_GET['supportEmail']) )
   $supportEmail = urldecode($_GET['supportEmail']);
 else
   $supportEmail = ""   
?>
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<title>Internal Error!</title>
</head>
<body>
<h1>Internal Error!</h1>
<hr />
<p style="font-weight: bold; color: #F00"><?=$msg?></p>
<p>Contact <a href="mailto:<?=$supportEmail?>" >Customer Support</a>.</p>
<hr />
<p>Powered By: <a href="http://kissmvc.com">KISSMVC</a></p>
</body>
</html>
