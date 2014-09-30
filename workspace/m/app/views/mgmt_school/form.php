<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>School Name</td>
			<td><input type="text" name="name" style="width:150px" value="<?php echo $object->get('name')?>" /></td>
		</tr>
		<tr>
			<td>Mascot</td>
			<td><input type="text" name="mascot" style="width:150px" value="<?php echo $object->get('mascot')?>" /></td>
		</tr>		
		<tr>
			<td>Logo todo allow upload of logo</td>
			<td><input type="text" name="logo" style="width:150px" value="<?php echo $object->get('logo')?>" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>