<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>	
		<tr>
			<td>1st On</td>
			<td><input type="text" name="_1st_on" style="width:150px" value="<?php echo $object->get('_1st_on')?>" /></td>
		</tr>
		<tr>
		    <td>1st Off</td>
			<td><input type="text" name="_1st_off" style="width:150px" value="<?php echo $object->get('_1st_off')?>" /></td>
		</tr>
		<tr>
			<td>2nd On</td>
			<td><input type="text" name="_2nd_on" style="width:150px" value="<?php echo $object->get('_2nd_on')?>" /></td>
		</tr>
		<tr>
		    <td>2nd Off</td>
			<td><input type="text" name="_2nd_off" style="width:150px" value="<?php echo $object->get('_2nd_off')?>" /></td>
		</tr>
		<tr>
			<td>3rd On</td>
			<td><input type="text" name="_3rd_on" style="width:150px" value="<?php echo $object->get('_3rd_on')?>" /></td>
		</tr>
		<tr>
		    <td>3rd Off</td>
			<td><input type="text" name="_3rd_off" style="width:150px" value="<?php echo $object->get('_3rd_off')?>" /></td>
		</tr>				
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
	</table>
</form>