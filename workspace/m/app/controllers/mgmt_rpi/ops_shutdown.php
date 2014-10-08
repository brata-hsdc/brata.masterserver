<?php
function _ops_shutdown($OID=0,$CID=0) {
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
       if ($object->shutdown() === false) $msg="shutdown failed";
       else                            $msg="shutdown worked";  
	}
	redirect("$urlPrefix/manage",$msg);
}
