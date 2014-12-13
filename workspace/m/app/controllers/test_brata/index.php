<?php
// create mock brata form
function _index() {
  $urlPrefix="test_brata";
  $data['body'][]='<h2>Brata Testing</h2><br />';
  $fdata['startUrl']=myUrl("$urlPrefix/sim_start_challenge");
  $fdata['startLabel']="Start Challenge";
  
  $fdata['submitUrl']=myUrl("$urlPrefix/sim_submit");
  $fdata['submitLabel']="Submit";
  
  $fdata['atWayPointUrl']=myUrl("$urlPrefix/sim_atwaypoint");
  $fdata['atWayPointLabel']="At Waypoint";
  
  $fdata['cancelUrl']=myUrl("$urlPrefix/index");
  $fdata['cancelLabel']="Cancel";
  $form = View::do_fetch(VIEW_PATH."$urlPrefix/mock_brata.php",$fdata);
  //$data['head'][]=View::do_fetch(VIEW_PATH."$urlPrefix/form_js.php");
  $data['body'][]=$form;
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}

