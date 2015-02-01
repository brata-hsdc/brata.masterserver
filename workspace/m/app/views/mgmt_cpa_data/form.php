
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Label</td>
			<td><input type="text" name="label" style="width:150px" value="<?php echo $object->get('label')?>" /></td>
		</tr>
		<tr>
			<td>Fence</td>
			<td><input type="text" name="fence" style="width:150px" value="<?php echo $object->get('fence')?>" /></td>
		</tr>
		<tr>
			<td>Building</td>
			<td><input type="text" name="building" style="width:150px" value="<?php echo $object->get('building')?>" /></td>
		</tr>
		<tr>
			<td>Sum</td>
			<td><input type="text" name="sum" style="width:150px" value="<?php echo $object->get('sum')?>" /></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>
