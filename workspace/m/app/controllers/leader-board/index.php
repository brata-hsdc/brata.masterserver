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
    
  View::do_dump(VIEW_PATH.'layouts/mgmtlayout.php',$data);
}

function _make_html_main_table($view,$item,$urlPrefix,&$data) {
	$dbh=getdbh();

	//view
	$fields="Name,Reg,CTS,FSL,HMB,CPA,Duration,Score";
	$stmt = $dbh->query("SELECT $fields FROM $view");
	if ($stmt === false) {
		var_dump($dbh->errorInfo());
		return;
	}
	$tablearr[]=explode(',',$fields);
	while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
		$row=null;
		foreach ($tablearr[0] as $f) {
			if      ($f == "Name")     $row[]=htmlspecialchars($rs[$f]);
			else if ($f == "Duration") $row[]=htmlspecialchars($rs[$f]);
			else if ($f == "Score")    $row[]=htmlspecialchars($rs[$f]);
			//todo what if score is not valid?
			else if ($f == "FSL")      { $T=$rs[$f]%4; $row[]="<img src='" . myUrl("img/$T.gif'") . ">"; } // TODO
			//else                       $row[]="<img src='" . myUrl("img/$rs[$f].gif'") . ">";//
			else                       $row[]=toWingDing($rs[$f]);
		}
		$tablearr[]=$row;
	};
	$data['body'][]=table::makeTable($tablearr);
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
