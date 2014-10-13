<?php
function _ops_sysconfig_update() {
  $errors="";

  if ( !isset($_POST['webfolder']) || $_POST['webfolder'] =="" )
  {
   	$errors .= ", invalid webfolder";
  }
  if ( !isset($_POST['webdomain']) || $_POST['webdomain'] =="" )
  {
    $errors .= ", invalid webdomain";
  }
   
  if ( !isset($_POST['dbhost']) || $_POST['dbhost'] =="" )
  {
    $errors .= ", invalid dbhost";
  }
  if ( !isset($_POST['dbname']) || $_POST['dbname'] =="" )
  {
    $errors .= ", invalid dbname";
  }
  if ( !isset($_POST['dbuser']) || $_POST['dbuser'] =="" )
  {
    $errors .= ", invalid dbuser";
  }
  if ( !isset($_POST['dbpass']) || $_POST['dbpass'] =="" )
  {
    $errors .= ", invalid dbpass";
  }

   
  $_POST['debug'] = isset($_POST['debug'] ) ?  1 : 0;
  $_POST['sendmail'] = isset($_POST['sendmail'] ) ?  1 : 0;
   
  if ($errors =="")
  {
    $fd = fopen("sysconfig_data.php","w");
    fwrite($fd,"<?php\n");
    fwrite($fd,"\$SYSCONFIG_WEBFOLDER='".$_POST['webfolder']."';\n");
    fwrite($fd,"\$SYSCONFIG_WEBDOMAIN='".$_POST['webdomain']."';\n");
    fwrite($fd,"\$SYSCONFIG_DBHOST='".$_POST['dbhost']."';\n");
    fwrite($fd,"\$SYSCONFIG_DBNAME='".$_POST['dbname']."';\n");
    fwrite($fd,"\$SYSCONFIG_DBUSER='".$_POST['dbuser']."';\n");
    fwrite($fd,"\$SYSCONFIG_DBPASS='".$_POST['dbpass']."';\n");
    fwrite($fd,"\$SYSCONFIG_DEBUG=".$_POST['debug'].";\n");
    fwrite($fd,"\$SYSCONFIG_SENDMAIL=".$_POST['sendmail'].";\n");
    fclose($fd);
    $errors = "System Configured";
  }
  redirect('mgmt_website/manage',$errors);
}