<form action="<?=$actionUrl?>" method="post" enctype="multipart/form-data" >
<table>
  <tr><th colspan="2">EXT Load Data</th></tr>	
  <tr>
    <td style="text-align:right">
	  <input type="file" name="csv_file">
	</td>
	<td></td>
  </tr>
  <tr>
      <td colspan="2" style="text-align:right">
        <input type="button" value="Cancel" onclick="location.href='<?=$cancelUrl ?>' " />
	    <input type="submit" name="Load EXT" value="Upload CSV File">
	  </td>
  </tr>
</table>
</form>
