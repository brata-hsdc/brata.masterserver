<?php
function _clear_scores() {
	$team = new Team();
	$allTeams = $team->retrieve_many("OID>?",array(0));
	foreach ( $allTeams as $team)
	{
		$team->clearScore();
	}
	Event::clearEvents();
	redirect('mgmt_main','Scores cleared');
}