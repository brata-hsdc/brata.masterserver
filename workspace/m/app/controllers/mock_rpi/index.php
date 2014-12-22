<?php
// create mock brata form
function _index() {
  $urlPrefix="mock_rpi";
  $data['body'][]='<h2>Mock rPI</h2><br />';

  $fdata['joinUrl']=myUrl("$urlPrefix/sim_join");
  $fdata['joinLabel']="Join";
  
  $fdata['submitUrl']=myUrl("$urlPrefix/sim_submit");
  $fdata['submitLabel']="Submit";
  
  //$fdata['timeExpiredUrl']=myUrl("$urlPrefix/sim_timeexpired");
  //$fdata['timeExpiredLabel']="Time Expired(HMB only)";
  
  $fdata['cancelUrl']=myUrl("$urlPrefix/index");
  $fdata['cancelLabel']="Cancel";
  $form = View::do_fetch(VIEW_PATH."$urlPrefix/mock_rpi.php",$fdata);
  //$data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/form_js.php");
  $data['body'][]=$form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}

