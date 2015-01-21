<?php
function makeOptionList($stationId) {
	return '<select name="stationId">'
		. '<option value=-1>Select One'	
		. Station::getAllCTSAsHTMLOptions($stationId)
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
			<td>1st</td>
			<td><input type="text" name="_1st" style="width:150px" value="<?php echo $object->get('_1st')?>" /></td>
		</tr>
		<tr>
			<td>2nd</td>
			<td><input type="text" name="_2nd" style="width:150px" value="<?php echo $object->get('_2nd')?>" /></td>
		</tr>
		<tr>
			<td>3rd</td>
			<td><input type="text" name="_3rd" style="width:150px" value="<?php echo $object->get('_3rd')?>" /></td>
		</tr>
		<tr>
			<td>4th</td>
			<td><input type="text" name="_4th" style="width:150px" value="<?php echo $object->get('_4th')?>" /></td>
		</tr>
		<tr>
			<td>5th</td>
			<td><input type="text" name="_5th" style="width:150px" value="<?php echo $object->get('_5th')?>" /></td>
		</tr>				
		<tr>
			<td>Tolerance</td>
			<td><input type="text" name="tolerance" style="width:150px" value="<?php echo $object->get('tolerance')?>" /></td>
		</tr>								
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>