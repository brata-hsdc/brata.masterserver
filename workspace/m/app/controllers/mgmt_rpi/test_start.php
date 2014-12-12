<?php
function _test_start($OID=0,$CID=0) {
	$OID=max(0,intval($OID));
	$CID=max(0,intval($CID));
	$msg='';

	loginRequireMgmt();
	if (!loginCheckPermission(USER::MGMT_RPI)) redirect("errors/401");
	$itemName="RPI";
	$urlPrefix="mgmt_rpi";
	$object=new RPI($OID,$CID);

	if (!$object->exists())
		$msg="$itemName not found!";
	else {
	  $tmp = new CTSData(0,-1); // hack
      $combo = $tmp->generateParameters();
      var_dump($combo);
      $object->start_challenge($combo);
	}
	//redirect("$urlPrefix/manage",$msg);
}
