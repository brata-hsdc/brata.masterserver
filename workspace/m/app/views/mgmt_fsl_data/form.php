<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>A Tag</td>
			<td><input type="text" name="a_tag" style="width:150px" value="<?php echo $object->get('a_tag')?>" /></td>
		</tr>
		<tr>
			<td>A Lat</td>
			<td><input type="text" name="a_lat" style="width:150px" value="<?php echo $object->get('a_lat')?>" /></td>
		</tr>
		<tr>
			<td>A Lng</td>
			<td><input type="text" name="a_lng" style="width:150px" value="<?php echo $object->get('a_lng')?>" /></td>
		</tr>
		<tr>
			<td>B Tag</td>
			<td><input type="text" name="b_tag" style="width:150px" value="<?php echo $object->get('b_tag')?>" /></td>
		</tr>
		<tr>
			<td>B Lat</td>
			<td><input type="text" name="b_lat" style="width:150px" value="<?php echo $object->get('b_lat')?>" /></td>
		</tr>
		<tr>
			<td>B Lng</td>
			<td><input type="text" name="b_lng" style="width:150px" value="<?php echo $object->get('b_lng')?>" /></td>
		</tr>
		<tr>
			<td>C Tag</td>
			<td><input type="text" name="c_tag" style="width:150px" value="<?php echo $object->get('c_tag')?>" /></td>
		</tr>	
		<tr>
			<td>C Lat</td>
			<td><input type="text" name="c_lat" style="width:150px" value="<?php echo $object->get('c_lat')?>" /></td>
		</tr>
		<tr>
			<td>C Lng</td>
			<td><input type="text" name="c_lng" style="width:150px" value="<?php echo $object->get('c_lng')?>" /></td>
		</tr>
		<tr>
			<td>Lat Tag</td>
			<td><input type="text" name="l_tag" style="width:150px" value="<?php echo $object->get('l_tag')?>" /></td>
		</tr>	
		<tr>
			<td>Lab Lat</td>
			<td><input type="text" name="l_lat" style="width:150px" value="<?php echo $object->get('l_lat')?>" /></td>
		</tr>
		<tr>
			<td>Lab Lng</td>
			<td><input type="text" name="l_lng" style="width:150px" value="<?php echo $object->get('l_lng')?>" /></td>
		</tr>		
		<tr>
			<td>A Rad</td>
			<td><input type="text" name="a_rad" style="width:150px" value="<?php echo $object->get('a_rad')?>" /></td>
		</tr>
		<tr>
			<td>B Rad</td>
			<td><input type="text" name="b_rad" style="width:150px" value="<?php echo $object->get('b_rad')?>" /></td>
		</tr>
		<tr>
			<td>C Rad</td>
			<td><input type="text" name="c_rad" style="width:150px" value="<?php echo $object->get('c_rad')?>" /></td>
		</tr>					
	    <tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>