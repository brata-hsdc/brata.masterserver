<?php
function _ops_website_update() {
  $errors="";
  if ( !isset($_POST['mgmtbanner']) || $_POST['mgmtbanner'] =="" )
  {
    $errors .= ", invalid management banner";
  }
  //if ( !isset($_POST['mgmtlogo']) || $_POST['mgmtlogo'] =="" )
  // {
  //	   	$errors .= ", invalid management logo";
  //}
  if ( !isset($_POST['mgmtfooter']) || $_POST['mgmtfooter'] =="" )
  {
    $errors .= ", invalid management footer";
  }
  if ( !isset($_POST['writersbanner']) || $_POST['writersbanner'] =="" )
  {
    $errors .= ", invalid writers banner";
  }
  //if ( !isset($_POST['writerslogo']) || $_POST['writerslogo'] =="" )
  //{
    //	   	$errors .= ", invalid writers logo";
    //}
    if ( !isset($_POST['writersfooter']) || $_POST['writersfooter'] =="" )
    {
      $errors .= ", invalid writers footer";
    }
     
    if ( !isset($_POST['supportemail']) || $_POST['supportemail'] =="" )
    {
      $errors .= ", invalid support email";
    }
    if ( !isset($_POST['supportnumber']) || $_POST['supportnumber'] =="" )
    {
      $errors .= ", invalid support number";
    }
    if ( !isset($_POST['taxfaxnumber']) || $_POST['taxfaxnumber'] =="" )
    {
      $errors .= ", invalid tax fax number";
    }
     
    $_POST['debug'] = isset($_POST['debug'] ) ?  1 : 0;
    $_POST['sendmail'] = isset($_POST['sendmail'] ) ?  1 : 0;
     
    if ($errors =="")
    {
      $fd = fopen("settings_data.php","w");
      fwrite($fd,"<?php\n");
      fwrite($fd,"\$SETTINGS_MGMT_BANNER='".$_POST['mgmtbanner']."';\n");
      fwrite($fd,"\$SETTINGS_MGMT_LOGO='".$_POST['mgmtlogo']."';\n");
      fwrite($fd,"\$SETTINGS_MGMT_FOOTER='".$_POST['mgmtfooter']."';\n");
      fwrite($fd,"\$SETTINGS_WRITERS_BANNER='".$_POST['writersbanner']."';\n");
      fwrite($fd,"\$SETTINGS_WRITERS_LOGO='".$_POST['writerslogo']."';\n");
      fwrite($fd,"\$SETTINGS_WRITERS_FOOTER='".$_POST['writersfooter']."';\n");
      fwrite($fd,"\$SETTINGS_SUPPORTEMAIL='".$_POST['supportemail']."';\n");
      fwrite($fd,"\$SETTINGS_SUPPORTNUMBER='".$_POST['supportnumber']."';\n");
      fwrite($fd,"\$SETTINGS_TAXFAXNUMBER='".$_POST['taxfaxnumber']."';\n");
      fclose($fd);
      $errors = "Web Site Configured";
    }
    redirect('mgmt_website/manage',$errors);
}