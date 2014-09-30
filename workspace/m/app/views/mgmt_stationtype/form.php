
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Short Name</td>
			<td><input type="text" name="shortName" style="width:150px" value="<?php echo $object->get('shortName')?>" /></td>
		</tr>
		<tr>
			<td>Long name</td>
			<td><input type="text" name="longName" style="width:150px" value="<?php echo $object->get('longName')?>" /></td>
		</tr>			
		<tr>
			<td>Instructions</td>
			<td><textarea name="instructions" style="width:150px"><?php echo $object->get('instructions')?></textarea></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>