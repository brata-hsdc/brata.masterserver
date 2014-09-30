<?php 
function makeRollList($currentPermissions) {
	return '<select name="permissions">'
		.'<option > - Select roll'
		. User::getAllAsHTMLOptions($currentPermissions)
		. '</select>';
}
?>
<form method="post" action="<?=$actionUrl?>">
<input type="hidden" name="OID" value="<?php echo $object->get('OID')?>" />
<input type="hidden" name="CID" value="<?php echo $object->get('CID')?>" />
	<table>
		<tr><th colspan="2"><?php echo $form_heading?></th></tr>
		<tr>
			<td>Full Name</td>
			<td><input type="text" name="fullname" style="width:150px" value="<?php echo $object->get('fullname')?>" /></td>
		</tr>	
		<tr>
			<td>User Name</td>
			<td><input type="text" name="username" style="width:150px" value="<?php echo $object->get('username')?>" /></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:center">Rolls control user permissions</td>
		</tr>	
		<tr>
			<td>Roll</td>
			<td><?php echo makeRollList($object->get('permissions')) ?> </td>
		</tr>		
		<tr>
		<td colspan="2" style="text-align:center">Complete the next two fields to change password</td>
		</tr>	
		<tr>
			<td>Password</td>
			<td><input type="text" name="password" style="width:150px" value="" /></td>
		</tr>
		<tr>
			<td>Confirm Password</td>
			<td><input type="text" name="confirm" style="width:150px" value="" /></td>
		</tr>		
	
		<tr>
			<td colspan="2" style="text-align:right">
      	    <input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="validateForm(this.form);return false;" /></td>
		</tr>
		
	</table>
</form>