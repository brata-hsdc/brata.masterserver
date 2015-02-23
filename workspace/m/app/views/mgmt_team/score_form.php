<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Reg Score</td>
			<td><input type="text" name="regScore" style="width:150px" value="<?php echo $object->get('regScore')?>" /></td>
		</tr>
		<tr>
			<td>CTS Score</td>
			<td><input type="text" name="ctsScore" style="width:150px" value="<?php echo $object->get('ctsScore')?>" /></td>
		</tr>
		<tr>
			<td>CTS Duration</td>
			<td><input type="text" name="ctsDuration" style="width:150px" value="<?php echo $object->get('ctsDuration')?>" /></td>
		</tr>
		<tr>
			<td>FSL Score(waypoint 1)</td>
			<td><input type="text" name="fslScore0" style="width:150px" value="<?php echo $object->get('fslScore0')?>" /></td>
		</tr>
		<tr>
			<td>FSL Score(waypoint 2)</td>
			<td><input type="text" name="fslScore1" style="width:150px" value="<?php echo $object->get('fslScore1')?>" /></td>
		</tr>
		<tr>
			<td>FSL Score(waypoint 3)</td>
			<td><input type="text" name="fslScore2" style="width:150px" value="<?php echo $object->get('fslScore2')?>" /></td>
		</tr>
		<tr>
			<td>FSL Score(Lab)</td>
			<td><input type="text" name="fslScore3" style="width:150px" value="<?php echo $object->get('fslScore3')?>" /></td>
		</tr>		
		<tr>
			<td>FSL Duration</td>
			<td><input type="text" name="fslDuration" style="width:150px" value="<?php echo $object->get('fslDuration')?>" /></td>
		</tr>
		<tr>
			<td>HMB Score</td>
			<td><input type="text" name="hmbScore" style="width:150px" value="<?php echo $object->get('hmbScore')?>" /></td>
		</tr>		
		<tr>
			<td>HMB Duration</td>
			<td><input type="text" name="hmbDuration" style="width:150px" value="<?php echo $object->get('hmbDuration')?>" /></td>
		</tr>
		<tr>
			<td>CPA Score</td>
			<td><input type="text" name="cpaScore" style="width:150px" value="<?php echo $object->get('cpaScore')?>" /></td>
		</tr>		
		<tr>
			<td>CPA Duration</td>
			<td><input type="text" name="cpaDuration" style="width:150px" value="<?php echo $object->get('cpaDuration')?>" /></td>
		</tr>
		<tr>
			<td>EXT Duration</td>
			<td><input type="text" name="extDuration" style="width:150px" value="<?php echo $object->get('extDuration')?>" /></td>
		</tr>
		<tr>
			<td>Tower Height</td>
			<td><input type="text" name="towerH" style="width:150px" value="<?php echo $object->get('towerH')?>" /></td>
		</tr>		
		<tr>
			<td>Tower Distance</td>
			<td><input type="text" name="towerD" style="width:150px" value="<?php echo $object->get('towerD')?>" /></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>