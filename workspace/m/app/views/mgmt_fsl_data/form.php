<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Tag</td>
			<td><input type="text" name="tag" style="width:150px" value="<?php echo $object->get('tag')?>" /></td>
		</tr>
		<tr>
			<td>Lat1</td>
			<td><input type="text" name="lat1" style="width:150px" value="<?php echo $object->get('lat1')?>" /></td>
		</tr>
		<tr>
			<td>Lng1</td>
			<td><input type="text" name="lng1" style="width:150px" value="<?php echo $object->get('lng1')?>" /></td>
		</tr>
		<tr>
			<td>Lat2</td>
			<td><input type="text" name="lat2" style="width:150px" value="<?php echo $object->get('lat2')?>" /></td>
		</tr>
		<tr>
			<td>Lng2</td>
			<td><input type="text" name="lng2" style="width:150px" value="<?php echo $object->get('lng2')?>" /></td>
		</tr>
		<tr>
			<td>Lat3</td>
			<td><input type="text" name="lat3" style="width:150px" value="<?php echo $object->get('lat3')?>" /></td>
		</tr>
		<tr>
			<td>Lng3</td>
			<td><input type="text" name="lng3" style="width:150px" value="<?php echo $object->get('lng3')?>" /></td>
		</tr>
		<tr>
			<td>Rad1</td>
			<td><input type="text" name="rad1" style="width:150px" value="<?php echo $object->get('rad1')?>" /></td>
		</tr>
		<tr>
			<td>Rad2</td>
			<td><input type="text" name="rad2" style="width:150px" value="<?php echo $object->get('rad2')?>" /></td>
		</tr>
		<tr>
			<td>Rad3</td>
			<td><input type="text" name="rad3" style="width:150px" value="<?php echo $object->get('rad3')?>" /></td>
		</tr>					
	    <tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>