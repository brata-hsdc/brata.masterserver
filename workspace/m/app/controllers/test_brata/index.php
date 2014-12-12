<?php
function _index() {
  $urlPrefix="test_brata";
  $data['body'][]='<h2>Brata Testing</h2><br />';
  //_make_html_table($n,$data); 
  $fdata['startUrl']=myUrl("$urlPrefix/ops_atwaypoint");
  $fdata['startLabel']="At Waypoint";
  
  $fdata['submitUrl']=myUrl("$urlPrefix/ops_atwaypoint")
  $fdata['submitLabel']="At Waypoint";
  
  $fdata['atwayPointUrl']=array(myUrl("$urlPrefix/ops_atwaypoint"),myUrl("$urlPrefix/ops_submit"));
  $fdata['aawayPointLabel']="At Waypoint";
  
  $fdata['cancelUrl']=myUrl("$urlPrefix/index");
  $fdata['cancelLabel']="Cancel";
  $form = View::do_fetch(VIEW_PATH."$urlPrefix/main.php",$fdata);
  //$data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/form_js.php");
  $data['body'][]=$form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}

