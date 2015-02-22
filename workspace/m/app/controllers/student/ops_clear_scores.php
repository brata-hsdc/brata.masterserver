<?php
function _ops_clear_scores() {
	$team = new Team();
	$allTeams = $team->retrieve_many("OID>?",array(0));
	foreach ( $allTeams as $team)
	{
		$team->clearScore();
	}
	Event::clearEvents();
	redirect('student','Scores cleared');
}