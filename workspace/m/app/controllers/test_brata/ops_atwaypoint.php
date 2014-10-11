<?php
$waypointId=$_POST['waypointId'];
$location=myUrl("brata-v00/atWaypoint/$waypointId");
header("Location: $location");
die();