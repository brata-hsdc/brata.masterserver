<?php
function makeOptionList($currentType) {
	return '<select name="schoolId">'
		. '<option value=-1>Select One'	
		. School::getAllAsHTMLOptions($currentType)
		. '</select>';
}
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Team Name</td>
			<td><input type="text" name="name" style="width:150px" value="<?php echo $object->get('name')?>" /></td>
		</tr>
		<tr>
			<td>School</td>
			<td><?php echo makeOptionList($object->get('schoolId')) ?> </td>
		</tr>			
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>