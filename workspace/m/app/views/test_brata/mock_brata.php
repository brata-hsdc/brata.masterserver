<?php
/*
function makeWaypointList() {
	return '<select name="waypointId">'
		. '<option value=-1>Select One'	
		. Waypoint::getAllAsHTMLOptions(-1)
		. '</select>';
}
<!--
<table>
  <form method="post" action="<?=$atWayPointUrl?>">
		<tr><th colspan="2">atWaypoint Test</th></tr>
		<tr>
			<td>TeamId (a.k.a. team ping)</td>
			<td><?php echo makeTeamList() ?> </td>
		</tr>		
		<tr>
		<tr>
			<td>Waypoint Id</td>
			<td><?php echo makeWaypointList() ?> </td>
		</tr>			
		<tr>
			<td colspan="2" style="text-align:right">
	     	<input type="button" value="<?=$cancelLabel?>" onclick="location.href='<?=$cancelUrl ?>' " />
			<input type="button" value="<?=$atWayPointLabel?>" onclick="submit();" /></td>
		</tr>
		
  </form>
  </table>
-->
*
*
*
*
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
    <form method="post" action="<?=$registerUrl?>">
		<tr><th colspan="2">Register</th></tr>
		<tr>
			<td>TeamId (a.k.a. team ping)</td>
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
			<td>TeamId (a.k.a. team ping)</td>
			<td><?php echo makeTeamList() ?> </td>
		</tr>		
		<tr>
			<td>StationId (a.k.a. station Tag)</td>
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
			<td>TeamId (a.k.a. team ping)</td>
			<td><?php echo makeTeamList() ?> </td>
		</tr>		
		<tr>			
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

