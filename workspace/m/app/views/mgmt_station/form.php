<?php
function makeTypeList($currentType) {
	return '<select name="typeId">'
		."<option value=-1>Select One"	
		. StationType::getAllAsHTMLOptions($currentType)
		. '</select>';
}
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Station Tag</td>
			<td><input type="text" name="tag" style="width:150px" value="<?php echo $object->get('tag')?>" /></td>
		</tr>	
			<tr>
			<td>Station type</td>
			<td><?php echo makeTypeList($object->get('typeId')) ?> </td>
		</tr>				
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>