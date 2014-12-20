
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Type Code(read only)</td>
			<td><input readonly type="text" name="typeCode" style="width:150px" value="<?php echo $object->get('typeCode')?>" /></td>
		</tr>
		<tr>
			<td>Name(read only)</td>
			<td><input readonly type="text" name="name" style="width:150px" value="<?php echo $object->get('name')?>" /></td>
		</tr>			
		<tr>
			<td>Has rPI(read only)</td>
			<td><input readonly type="text" name="hasrPI" style="width:150px" value="<?php echo $object->get('hasrPI')?>" /></td>
		</tr>		
		<tr>
			<td>Delay</td>
			<td><input type="text" name="delay" style="width:150px" value="<?php echo $object->get('delay')?>" /></td>
		</tr>		
		<tr>
			<td>Instructions</td>
			<td><textarea name="instructions" style="width:150px"><?php echo $object->get('instructions')?></textarea></td>
		</tr>
		<tr>
			<td>Correct Message</td>
			<td><textarea name="correct_msg" style="width:150px"><?php echo $object->get('correct_msg')?></textarea></td>
		</tr>
		<tr>
			<td>Incorrect Message</td>
			<td><textarea name="incorrect_msg" style="width:150px"><?php echo $object->get('incorrect_msg')?></textarea></td>
		</tr>
		<tr>
			<td>Failed Message</td>
			<td><textarea name="failed_msg" style="width:150px"><?php echo $object->get('failed_msg')?></textarea></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>