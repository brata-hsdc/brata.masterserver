<?php 
 $parms = $object->generateParameters();
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>	
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
			<td>1st on</td>
			<td><input type="text" style="width:150px" value="<?php echo $parms[0] ?>" /></td>
			<td>1st off</td>
			<td><input type="text" style="width:150px" value="<?php echo $parms[1] ?>" /></td>
		</tr>
		<tr>
			<td>2nd on</td>
			<td><input type="text" style="width:150px" value="<?php echo $parms[2] ?>" /></td>
			<td>2nd off</td>
			<td><input type="text" style="width:150px" value="<?php echo $parms[3] ?>" /></td>			
		</tr>
		<tr>
			<td>3rd on</td>
			<td><input type="text" style="width:150px" value="<?php echo $parms[4] ?>" /></td>
			<td>3rd off</td>
			<td><input type="text" style="width:150px" value="<?php echo $parms[5] ?>" /></td>			
		</tr>							
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
		</tr>
	</table>
</form>