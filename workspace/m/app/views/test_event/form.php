<?php
function makeTypeList($currentType) {
	return '<select name="type">'
		. Event::getTypesAsHTMLOptions($currentType)
		. '</select>';
}
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Team</td>
			<td><input type="text" name="teamId" style="width:150px" value="<?php echo $object->get('teamId')?>" /></td>
		</tr>
		<tr>
			<td>Station Name</td>
			<td><input type="text" name="stationId" style="width:150px" value="<?php echo $object->get('stationId')?>" /></td>
		</tr>
			<tr>
			<td>Event type</td>
			<td><?php echo makeTypeList($object->get('type')) ?> </td>
		</tr>	
		<tr>
			<td>Points</td>
			<td><input type="text" name="points" style="width:150px" value="<?php echo $object->get('points')?>" /></td>
		</tr>		
		<tr>
			<td>Description</td>
			<td><input type="text" name="description" style="width:150px" value="<?php echo $object->get('description')?>" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>