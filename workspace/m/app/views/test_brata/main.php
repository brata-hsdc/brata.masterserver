<?php
function makeOptionList() {
	return '<select name="waypointId">'
		. '<option value=-1>Select One'	
		. Waypoint::getAllAsHTMLOptions(-1)
		. '</select>';
}
?>
  <table>
    <form method="post" action="<?=$startUrl?>">
		<tr><th colspan="2">Submit Test</th></tr>		
		<tr>
			<td>Start Challenge</td>
			<td><input type="text" name="stationId" style="width:150px" value="" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$startLabel?>" onclick="submit()" /></td>
		</tr>
		
  </form>
</table>
  <hr>
  <table>
    <form method="post" action="<?=$submitUrl?>">
		<tr><th colspan="2">Submit Test</th></tr>		
		<tr>
			<td>Submit</td>
			<td><input type="text" name="guess" style="width:150px" value="" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$submitLabel?>" onclick="submit()" /></td>
		</tr>
		
  </form>
</table>
<table>
  <form method="post" action="<?=$atWaypoingUrl?>">
		<tr><th colspan="2">atWaypoint Test</th></tr>
		<tr>
			<td>atWaypoint</td>
			<td><?php echo makeOptionList() ?> </td>
		</tr>			
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$atWaypoingLabel?>" onclick="submit();" /></td>
		</tr>
		
  </form>
  </table>

