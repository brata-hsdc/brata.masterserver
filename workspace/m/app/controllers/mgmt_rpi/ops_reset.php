<?php
function _ops_reset($OID=0,$CID=0) {
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
       if ($object->reset() === false) $msg="reset failed";
       else                            $msg="reset worked";  
	}
	redirect("$urlPrefix/manage",$msg);
}