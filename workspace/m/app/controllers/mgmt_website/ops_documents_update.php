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


function _ops_documents_update()
{
  // In PHP versions earlier than 4.1.0, $HTTP_POST_FILES should be used instead
  // of $_FILES.

  if (!isset($_POST['document_slot'])) redirect('mgmt_website/documents',"error missing document type value");
  $document_slot = $_POST['document_slot'];
  
  if ($document_slot != "terms" && $document_slot != "privacy" ) {
    redirect('mgmt_website/documents',"unknown document slot");    
  }
  
  if ($_FILES['document']['error'] != UPLOAD_ERR_OK)
  {
    $error_code = $_FILES['document']['error'];
    redirect('mgmt_website/documents',file_upload_error_message($error_code));
  }
  else // file upload OK
  {
    if ($_FILES["document"]["type"] != "application/pdf") {
      redirect('mgmt_website/documents',"not a PDF document");
    } else {
      move_uploaded_file($_FILES['document']['tmp_name'], "documents/".$document_slot.".pdf");
    }
  } // _checkCreditials
  redirect('mgmt_website/documents',"document updated");
}
?>