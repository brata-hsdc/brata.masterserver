<?php
function makeOptionList() {
	return '<select name="waypointId">'
		. '<option value=-1>Select One'	
		. Waypoint::getAllAsHTMLOptions(-1)
		. '</select>';
}
?>

<table>
  <form method="post" action="<?=$actionUrl[0]?>">
		<tr><th colspan="2">atWaypoint Test</th></tr>
		<tr>
			<td>atWaypoint</td>
			<td><?php echo makeOptionList() ?> </td>
		</tr>			
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="submit();" /></td>
		</tr>
		
  </form>
    <form method="post" action="<?=$actionUrl[1]?>">
		<tr><th colspan="2">atWaypoint Test</th></tr>		
		<tr>
			<td>Submit</td>
			<td><input type="text" name="guess" style="width:150px" value="" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$actionLabel?>" onclick="submit()" /></td>
		</tr>
		
  </form>
</table>
