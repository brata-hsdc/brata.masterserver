<?php
function makeOptionList($currentType) {
	return '<select name="waypointId">'
		. '<option value=-1>Select One'	
		. Waypoint::getAllAsHTMLOptions($currentType)
		. '</select>';
}
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Waypoint</td>
			<td><?php echo makeOptionList($object->get('waypointId')) ?> </td>
		</tr>		
		<tr>
			<td>Message Text</td>
			<td><input type="text" name="text" style="width:150px" value="<?php echo $object->get('text')?>" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>