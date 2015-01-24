<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>	
		<tr>
			<td>Waypoint1 Lat (nn.nnnnnn)</td>
			<td><input type="text" name="waypoint1_lat" style="width:150px" value="<?php echo $object->get('waypoint1_lat')?>" /></td>
		</tr>
		<tr>
			<td>Waypoint1 Lng(nn.nnnnnn)</td>
			<td><input type="text" name="waypoint1_lng" style="width:150px" value="<?php echo $object->get('waypoint1_lng')?>" /></td>
		</tr>
		<tr>
			<td>Waypoint2 Lat (nn.nnnnnn)</td>
			<td><input type="text" name="waypoint2_lat" style="width:150px" value="<?php echo $object->get('waypoint2_lat')?>" /></td>
		</tr>
		<tr>
			<td>Waypoint2 Lng(nn.nnnnnn)</td>
			<td><input type="text" name="waypoint2_lng" style="width:150px" value="<?php echo $object->get('waypoint2_lng')?>" /></td>
		</tr>
		<tr>
			<td>Waypoint3 Lat (nn.nnnnnn)</td>
			<td><input type="text" name="waypoint3_lat" style="width:150px" value="<?php echo $object->get('waypoint3_lat')?>" /></td>
		</tr>
		<tr>
			<td>Waypoint3 Lat(nn.nnnnnn)</td>
			<td><input type="text" name="waypoint3_lng" style="width:150px" value="<?php echo $object->get('waypoint3_lng')?>" /></td>
		</tr>				
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>