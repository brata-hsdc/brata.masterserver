<?php
function _edit_score($OID=0, $CID=0) {
  loginRequireMgmt();
  if (!loginCheckPermission(USER::MGMT_TEAM)) redirect("errors/401");
  $item="Team";
  $urlPrefix="mgmt_team";
  $object=new Team();
  $object->retrieve($OID,$CID);
  if (!$object->exists())
  $data['body'][]="<p>$item Not Found!</p>";
  else {
    $fdata['form_heading']="Edit $item Score";
    $fdata['object']=$object;
    $fdata['actionUrl']=myUrl("$urlPrefix/ops_update_score");
    $fdata['actionLabel']="Submit";
    $fdata['cancelUrl']=myUrl("$urlPrefix/manage");
    $fdata['cancelLabel']="Cancel";
    $form = View::do_fetch(VIEW_PATH."$urlPrefix/score_form.php",$fdata);
    $data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/score_form_js.php");
    $data['body'][]="<h2>Edit $item Score</h2>";
    $data['body'][]=$form;
  }
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}