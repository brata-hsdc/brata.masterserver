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
function makeStationTypeList() {
	return '<select name="stationType">'
			. '<option value=-1>Select One'
					. StationType::getAllAsHTMLOptions(-1)
					. '</select>';
}
?>
  <table>
  <tr><th>Last Response from M</th></tr>
  <tr><td><?php echo htmlspecialchars(mock_get_to_rpi_response()) ?></td></tr>
  </table>
  <table>
    <form method="post" action="<?=$joinUrl?>">
		<tr><th colspan="2">Join</th></tr>
		<tr>
			<td>Station Id (a.k.a. tag)</td>
			<td><?php echo makeStationList() ?> </td>
		</tr>
		<tr>
			<td>Station Type</td>
			<td><?php echo makeStationTypeList() ?> </td>
		</tr>
		<tr>
			<td>rPI URL</td>
			<td><input type="text" name="station_url" style="width:150px" value="" /></td>
		</tr>			
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$joinLabel?>" onclick="submit()" /></td>
		</tr>	
  </form>
</table>
  <hr>
  <table>
    <form method="post" action="<?=$submitUrl?>">
		<tr><th colspan="2">Submit Test</th></tr>
		<tr>
			<td>StationId (a.k.a. tag)</td>
			<td><?php echo makeStationList() ?> </td>
		</tr>			
		<tr>
			<td>Candidate Answer</td>
			<td><input type="text" name="candidate_answer" style="width:150px" value="" /></td>
		</tr>
		<tr>
			<td>Is Correct</td>
			<td><input type="checkbox" name="is_correct" style="width:150px" value="" /></td>
		</tr>
		<tr>
			<td>Fail Message</td>
			<td><input type="text" name="fail_message" style="width:150px" value="" /></td>
		</tr>
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$submitLabel?>" onclick="submit()" /></td>
		</tr>
		
  </form>
</table>

