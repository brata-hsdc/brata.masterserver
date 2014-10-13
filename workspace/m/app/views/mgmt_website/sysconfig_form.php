<?php
include "sysconfig_data.php";
?>
<form method="post" action="<?= $action ?>">
<table>
  <tr><th colspan="2"><?php echo $form_heading?></th></tr>
  <tr>
    <td>Web Folder[with trailing slash]</td>
    <td><input name=webfolder value='<?php echo $SYSCONFIG_WEBFOLDER?>'/></td>
  </tr>
  <tr>
    <td>Web Domain [with NO trailing slash]</td>
    <td><input name=webdomain value='<?php echo $SYSCONFIG_WEBDOMAIN?>' /></td>
  </tr> 
  <tr>
    <td>Database Host</td>
    <td><input name=dbhost value='<?php echo $SYSCONFIG_DBHOST?>'/></td>
  </tr>
  <tr>
    <td>Database Name</td>
    <td><input name=dbname value='<?php echo $SYSCONFIG_DBNAME?>'/></td>
  </tr>
  <tr>
    <td>Database User</td>
    <td><input name=dbuser value='<?php echo $SYSCONFIG_DBUSER?>'/></td>
  </tr>
  <tr>
    <td>Database Password</td>
    <td><input name=dbpass value='<?php echo $SYSCONFIG_DBPASS?>'/></td>
  </tr>
  <tr>
    <td>Debug Mode</td>
    <td><input type=checkbox name=debug value='1' <?php if ($SYSCONFIG_DEBUG) echo "checked"; ?> /> </td>
  </tr>
  <tr>
    <td>Send Mail</td>
    <td><input type=checkbox name=sendmail value='1' <?php if ($SYSCONFIG_SENDMAIL) echo "checked"; ?> /> </td>
  </tr>  
   <tr> 
	<td colspan="2" style="text-align:right">
		<input type="button" value="Cancel" onclick="location.href='<?=$cancel ?>' " />
		<input type="button" value="Submit" onclick="validateForm(this.form);return false;" />
     </td>
   </tr>
</table>

</form>