<?php
function makeOptionList($stationId) {
	return '<select name="stationId">'
		. '<option value=-1>Select One'	
		. Station::getAllCPAAsHTMLOptions($stationId)
		. '</select>';
}
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Station</td>
			<td><?php echo makeOptionList($object->get('stationId')) ?></td>
		</tr>
		<tr>
			<td>Velocity</td>
			<td><input type="text" name="velocity" style="width:150px" value="<?php echo $object->get('velocity')?>" /></td>
		</tr>
		<tr>
			<td>Velocity Tolerance</td>
			<td><input type="text" name="velocity_tolerance" style="width:150px" value="<?php echo $object->get('velocity_tolerance')?>" /></td>
		</tr>
		<tr>
			<td>Window Time</td>
			<td><input type="text" name="window_time" style="width:150px" value="<?php echo $object->get('window_time')?>" /></td>
		</tr>
		<tr>
			<td>Window Time Tolerance</td>
			<td><input type="text" name="window_time_tolerance" style="width:150px" value="<?php echo $object->get('window_time_tolerance')?>" /></td>
		</tr>		
		<tr>
			<td>Pulse Width</td>
			<td><input type="text" name="pulse_width" style="width:150px" value="<?php echo $object->get('pulse_width')?>" /></td>
		</tr>
		<tr>
			<td>Pulse Width Tolerance</td>
			<td><input type="text" name="pulse_width_tolerance" style="width:150px" value="<?php echo $object->get('pulse_width_tolerance')?>" /></td>
		</tr>			
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>