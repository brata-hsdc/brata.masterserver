<?php
include_once "sysconfig_data.php";

function writeSysconfig()
{
  $errors="";

  if ( !isset($_POST['webdomain']) || $_POST[webdomain] =="" )
  {
  	$errrors .= ", invalid webdomain";
  }
  
   if ( !isset($_POST['webfolder']) || $_POST['webfolder'] =="" )
   {
   	$errrors .= ", invalid webfolder";
   }
 
   if ( !isset($_POST['loglevel']))
   {
   	$errrors .= ", invalid loglevel";
   }
   
   if ( !isset($_POST['dbhost']) || $_POST['dbhost'] =="" )
   {
   	   	$errrors .= ", invalid dbhost";
   }
   if ( !isset($_POST['dbname']) || $_POST['dbname'] =="" )
   {
   	   	$errrors .= ", invalid dbname";
   }
   if ( !isset($_POST['dbuser']) || $_POST['dbuser'] =="" )
   {
   	   	$errrors .= ", invalid dbuser";
   }
   if ( !isset($_POST['dbpass']) || $_POST['dbpass'] =="" )
   {
   	   	$errrors .= ", invalid dbpass";
   } 
   if ( !isset($_POST['leaderBoardRefersh']) || $_POST['leaderBoardRefersh'] =="" )
   {
   	$errrors .= ", invalid dbpass";
   }
   
   $_POST['debug'] = isset($_POST['debug'] ) ?  1 : 0;
   $_POST['sendmail'] = isset($_POST['sendmail'] ) ?  1 : 0;
   $_POST['student'] = isset($_POST['student'] ) ?  1 : 0;
   
   if ($errors =="")
   {
      //$fd = fopen("/tmp/sysconfig_data.php","w"); // when you can't write directly to sysconfig_data.php ...
      $fd = fopen("sysconfig_data.php","w");
      if ($fd === false) {
      	$a= error_get_last();
      	$errors = "can't open sysconfig_data.php for writing reason=". $a['message'];
      	return $errors;
      }
      fwrite($fd,"<?php\n");
      fwrite($fd,"\$SYSCONFIG_WEBDOMAIN='".$_POST['webdomain']."';\n");
      fwrite($fd,"\$SYSCONFIG_WEBFOLDER='".$_POST['webfolder']."';\n"); 
      fwrite($fd,"\$SYSCONFIG_DBHOST='".$_POST['dbhost']."';\n"); 
      fwrite($fd,"\$SYSCONFIG_DBNAME='".$_POST['dbname']."';\n");
      fwrite($fd,"\$SYSCONFIG_DBUSER='".$_POST['dbuser']."';\n");
      fwrite($fd,"\$SYSCONFIG_DBPASS='".$_POST['dbpass']."';\n");
      fwrite($fd,"\$SYSCONFIG_DEBUG=".$_POST['debug'].";\n");
      fwrite($fd,"\$SYSCONFIG_SENDMAIL=".$_POST['sendmail'].";\n");      
      fwrite($fd,"\$SYSCONFIG_LOGLEVEL=".$_POST['loglevel'].";\n");
      fwrite($fd,"\$SYSCONFIG_STUDENT=".$_POST['student'].";\n");
      fwrite($fd,"\$SYSCONFIG_ENCODE=".$_POST['encode'].";\n");
      fwrite($fd,"\$SYSCONFIG_LEADERBOARD_REFRESH=".$_POST['leaderBoardRefersh'].";\n");
      fclose($fd);
   }
   return $errors;
}
$errors="";
if ( isset($_GET['write']) ) {
	$errors=writeSysconfig();
	?>
	<html>
	<body>
	<H1>Setup Complete</H1>
	<div><?php echo $errors; ?></div>
	<a href=setup.php>again</a>
	<br>
	<a href=<?php echo $SYSCONFIG_WEBHOST.$SYSCONFIG_WEBFOLDER ?>>Start using application</a>
	</body>
	</html>
	<?php
	exit;

}
?>
<html>
<body>
<p>
<?php 
   if ($errors != "")
   {
	foreach (explode(",",$errors) as $msg) {
		if ($msg !="") echo $msg;
	}
   }
?>
</p>
<form method="post" action="setup.php?write=1">
<table>
<tr><td>Web Domain[with trailing slash]</td><td><input name=webdomain value='<?php echo $SYSCONFIG_WEBDOMAIN?>'/></td></tr>
<tr><td>Web Folder[with trailing slash]</td><td><input name=webfolder value='<?php echo $SYSCONFIG_WEBFOLDER?>'/></td></tr>
<tr><td>Database Host</td><td><input name=dbhost value='<?php echo $SYSCONFIG_DBHOST?>'/></td></tr>
<tr><td>Database Name</td><td><input name=dbname value='<?php echo $SYSCONFIG_DBNAME?>'/></td></tr>
<tr><td>Database User</td><td><input name=dbuser value='<?php echo $SYSCONFIG_DBUSER?>'/></td></tr>
<tr><td>Database Password</td><td><input name=dbpass value='<?php echo $SYSCONFIG_DBPASS?>'/></td></tr>
<tr><td>Leader Board Refresh Rate(seconds)</td><td><input name=leaderBoardRefersh value='<?php echo $SYSCONFIG_LEADERBOARD_REFRESH?>'/></td></tr>
<tr><td>Log Level</td><td><input name=loglevel value='<?php echo $SYSCONFIG_LOGLEVEL?>'/></td></tr>
<tr><td>Send Mail (to new users)</td><td><input type=checkbox name=sendmail value='1' <?php if ($SYSCONFIG_SENDMAIL) echo "checked"; ?> /> </td></tr>
<tr><td>Debug Mode</td><td><input type=checkbox name=debug value='1' <?php if ($SYSCONFIG_DEBUG) echo "checked"; ?> /> </td></tr>
<tr><td>Student Mode Server</td><td><input type=checkbox name=student value='1' <?php if ($SYSCONFIG_STUDENT) echo "checked"; ?> /> </td></tr>
<tr><td>Encode Messages</td><td><input type=checkbox name=encode value='1' <?php if ($SYSCONFIG_ENCODE) echo "checked"; ?> /> </td></tr>

</table>
<input class="button" type="submit" name=submit />
</form>
</body>
</html>