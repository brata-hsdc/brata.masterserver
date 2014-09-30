<?php
header("HTTP/1.0 500 Internal Server Error: Form Error");
if ( isset($_GET['msg']) )
   $msg = urldecode($_GET['msg']);
else
   $msg = "Unknown Form Error";
?>
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<title>Form Data Mismatch</title>
</head>
<body>
<h1>Data does not match Form</h1>
<p><?=$msg?></p>
<hr />
<p>Powered By: <a href="http://kissmvc.com">KISSMVC</a></p>
</body>
</html>
