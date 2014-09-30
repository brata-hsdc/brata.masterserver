<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Lat</td>
			<td><input type="text" name="lat" style="width:150px" value="<?php echo $object->get('lat')?>" /></td>
		</tr>	
		<tr>
			<td>Lng</td>
			<td><input type="text" name="lng" style="width:150px" value="<?php echo $object->get('lng')?>" /></td>
		</tr>
		<tr>
			<td>Lat</td>
			<td><input type="text" name="description" style="width:150px" value="<?php echo $object->get('description')?>" /></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>