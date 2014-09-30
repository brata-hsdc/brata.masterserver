<?php
include "settings_data.php";
?>
<form method="post" action="<?= $action ?>">
<input type=hidden name=mgmtlogo value='<?php echo $SETTINGS_MGMT_LOGO?>' />
<input type=hidden name=writerslogo value='<?php echo $SETTINGS_WRITERS_LOGO?>' />
<table>
  <tr><th colspan="2"><?php echo $form_heading?></th></tr>
    <tr>
    <td>Management Banner</td>
    <td><input name=mgmtbanner value='<?php echo $SETTINGS_MGMT_BANNER?>' /></td>
  </tr>
  <tr>
    <td>Management Footer</td>
    <td><input name=mgmtfooter value='<?php echo $SETTINGS_MGMT_FOOTER?>' /></td>
  </tr>
    <tr>
    <td>Writers Banner</td>
    <td><input name=writersbanner value='<?php echo $SETTINGS_WRITERS_BANNER?>' /></td>
  </tr>
  <tr>
  <td>Writers Footer</td>
    <td><input name=writersfooter value='<?php echo $SETTINGS_WRITERS_FOOTER?>' /></td>
  </tr>
  <tr>
    <td>Support e-mail</td>
    <td><input name=supportemail value='<?php echo $SETTINGS_SUPPORTEMAIL?>' /></td>
  </tr>
  <tr>
    <td>Support Number</td>
    <td><input name=supportnumber value='<?php echo $SETTINGS_SUPPORTNUMBER?>' /></td>
  </tr>
  <tr>
    <td>Tax Fax Number</td>
    <td><input name=taxfaxnumber value='<?php echo $SETTINGS_TAXFAXNUMBER?>' /></td>
  </tr>
   <tr> 
	<td colspan="2" style="text-align:right">
		<input type="button" value="Cancel" onclick="location.href='<?=$cancel ?>' " />
		<input type="button" value="Submit" onclick="validateForm(this.form);return false;" />
     </td>
   </tr>
</table>
</form>
<form enctype="multipart/form-data" action="<?=myUrl('mgmt_website/ops_logo_update')?>" method="POST">
    <select name="logosite">
      <option value='WRITERS'>Writer's Logo</option>
      <option value='MGMT'>Managment Logo</option>
    </select>
    <!-- Name of input element determines name in $_FILES array -->
   <div>Logo</div> <input name="logo" type="file" />
    <input type="submit" value="Upload Logo" />
</form>