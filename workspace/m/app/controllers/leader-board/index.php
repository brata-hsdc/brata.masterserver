<?php

function toWingDing($points) {
	$points = $points % 4;
	switch ($points)
	{
		case  0: return "<font size='5' color='black'>&ndash;</font>";    // dash
		case  1: return "<font size='5' color='red'>&#x2718;</font>";     // heavy ballot x
		case  2: return "<font size='5' color='blue'>&#x2714;</font>";    // check mark
		case  3: return "<font size='5' color='green'>&#x2605;</font>";   // star
		default:
	}
}

function _index() {
  $view="v_leaderboard_main";
  $item="Leader Board";
  $urlPrefix="leader-board";
  $data['body'][]="<h2>$item</h2><br />";
  _make_html_main_table($view,$item,$urlPrefix,$data);

  $view="v_leaderboard_ext";
  $item="Extra (a.k.a. Tower) Challenge Leader Board";
  $urlPrefix="leader-board";
  $data['body'][]="<h2>$item</h2><br />";
  _make_html_ext_table($view,$item,$urlPrefix,$data);
    
  View::do_dump(VIEW_PATH.'layouts/leaderboardlayout.php',$data);
}

function _make_html_main_table($view,$item,$urlPrefix,&$data) {
	$dbh=getdbh();

	//view
	$fields="Name,Reg,CTS,FSL0,FSL1,FSL2,FSL3,HMB,CPA,Duration,Score";
	$stmt = $dbh->query("SELECT $fields FROM $view");
	if ($stmt === false) {
		var_dump($dbh->errorInfo());
		return;
	}
	$tablearr[]=explode(',',"Name,Reg,CTS,Waypoint 1,Waypoint 2,Waypoint 3,FSL,HMB,CPA,Duration,Score");
	
	$fields=explode(',',$fields);
	
	$data['body'][]="<table class='table table-striped'>";
	$data['body'][]="<thead><tr><th>Name</th><th>Reg</th><th>CTS</th><th colspan=4 style=text-align:center>FSL</th><th>HMB</th><th>CPA</th><th>Duration</th><th>Score</th></tr></thead></tbody>";
	
	$data['body'][]="<thead><tr><th></th><th></th><th></th><th>WP1</th><th>WP2</th><th>WP3</th><th>Lab</th><th></th><th></th><th></th><th></th></tr></thead></tbody>";
	
	while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
		$row=null;
		foreach ($fields as $f) {
			if      ($f == "Name")     $row[]="<td>".htmlspecialchars($rs[$f])."</td>";
			else if ($f == "Duration") $row[]="<td>".htmlspecialchars($rs[$f])."</td>";
			else if ($f == "Score")    $row[]="<td>".htmlspecialchars($rs[$f])."</td>";
			else                       $row[]="<td>".toWingDing($rs[$f])."</td>";
		}
		$data['body'][]="<tr>".implode($row)."</tr>";
	};
	//$data['body'][]=table::makeTable($tablearr);
	$data['body'][]="</tbody></table>";
	
}
function _make_html_ext_table($view,$item,$urlPrefix,&$data) {
	$dbh=getdbh();

	//view
	$fields="Name,towerD,towerH,Duration,Score";
	$stmt = $dbh->query("SELECT $fields FROM $view");
	if ($stmt === false) {
		var_dump($dbh->errorInfo());
		return;
	}
	$fields = explode(',', $fields);
	$tablearr[]=explode(',',"Name,Location Accuracy,Height Accuracy,Duration,Score");
	while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
		$row=null;
		foreach ($fields as $f) {
			$row[]=htmlspecialchars($rs[$f]);
		}
		$tablearr[]=$row;
	};
	$data['head'][] = '<meta http-equiv="refresh" content="'.$GLOBALS['leaderBoardRefresh'].'">';
	$data['body'][]=table::makeTable($tablearr);
}
