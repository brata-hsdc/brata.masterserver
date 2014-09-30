<?php
function file_upload_error_message($error_code) {
  switch ($error_code) {
    case UPLOAD_ERR_INI_SIZE:
      return 'The uploaded file exceeds the upload_max_filesize directive in php.ini';
    case UPLOAD_ERR_FORM_SIZE:
      return 'The uploaded file exceeds the MAX_FILE_SIZE directive that was specified in the HTML form';
    case UPLOAD_ERR_PARTIAL:
      return 'The uploaded file was only partially uploaded';
    case UPLOAD_ERR_NO_FILE:
      return 'No file was uploaded';
    case UPLOAD_ERR_NO_TMP_DIR:
      return 'Missing a temporary folder';
    case UPLOAD_ERR_CANT_WRITE:
      return 'Failed to write file to disk';
    case UPLOAD_ERR_EXTENSION:
      return 'File upload stopped by extension';
    default:
      return 'Unknown upload error';
  }
}
function getLogo()
{
  $fileName = $_FILES['ismsstory']['name'];
  $tmpName  = $_FILES['ismsstory']['tmp_name'];
  $fileSize = $_FILES['ismsstory']['size'];
  $fileType = $_FILES['ismsstory']['type'];

  $fp      = fopen($tmpName, 'r');
  $content = fread($fp, filesize($tmpName));
  fclose($fp);
  return $content;
}

function _ops_logo_update()
{
  // In PHP versions earlier than 4.1.0, $HTTP_POST_FILES should be used instead
  // of $_FILES.

  if (!isset($_POST['logosite'])) redirect('mgmt_website/website',"error missing logosite value");
  $site = $_POST['logosite'];

  if ($_FILES['logo']['error'] != UPLOAD_ERR_OK)
  {
    $error_code = $_FILES['logo']['error'];
    redirect('mgmt_website/website',file_upload_error_message($error_code));
  }
  else // file upload OK
  {
    $fileName  = $site . "-" . $_FILES['logo']['name'];//  . '' .$_FILES['logo']['type'];
    move_uploaded_file($_FILES['logo']['tmp_name'], "img/".$fileName);
    saveSetting("\$SETTINGS_".$site."_LOGO",$fileName);
  } // _checkCreditials
  redirect('mgmt_website/website',"logo updated");
}
?>