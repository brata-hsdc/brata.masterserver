<?php
require(APP_PATH.'inc/mock_functions.php');
/*
function makeWaypointList() {
	return '<select name="waypointId">'
		. '<option value=-1>Select One'	
		. Waypoint::getAllAsHTMLOptions(-1)
		. '</select>';
}

*/
function makeStationList() {
	return '<select name="stationId">'
			. '<option value=-1>Select One'
					. Station::getAllAsHTMLOptions(-1)
					. '</select>';
}
function makeTeamList() {
	return '<select name="teamId">'
			. '<option value=-1>Select One'
					. Team::getAllAsHTMLOptions(-1)
					. '</select>';
}
?>
  <table>
  <tr><th>Last Response from M</th></tr>
  <tr><td><?php echo htmlspecialchars(mock_get_brata_response()) ?></td></tr>
  </table>
  <table>
    <form method="post" action="<?=$registerUrl?>">
		<tr><th colspan="2">Register</th></tr>
		<tr>
			<td>TeamId (a.k.a. team pin)</td>
			<td><?php echo makeTeamList() ?> </td>
		</tr>		
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$registerLabel?>" onclick="submit()" /></td>
		</tr>	
  </form>
</table>
<hr>
  <table>
    <form method="post" action="<?=$startUrl?>">
		<tr><th colspan="2">Start Challenge</th></tr>
		<tr>
			<td>TeamId (a.k.a. team pin)</td>
			<td><?php echo makeTeamList() ?> </td>
		</tr>		
		<tr>
			<td>StationId (a.k.a. station Tag -- remeber to check for rPI Joins!)</td>
			<td><?php echo makeStationList() ?> </td>
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
			<td>TeamId (a.k.a. team pin)</td>
			<td><?php echo makeTeamList() ?> </td>
		</tr>		
		<tr>
			<td>StationId (a.k.a. station Tag -- remeber to check for rPI Joins!)</td>
			<td><?php echo makeStationList() ?> </td>
		</tr>
		<tr>
			<td>Candidate Answer</td>
			<td><input type="text" name="candidateAnswer" style="width:150px" value="" /></td>
		</tr>	
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$submitLabel?>" onclick="submit()" /></td>
		</tr>
		
  </form>
</table>

