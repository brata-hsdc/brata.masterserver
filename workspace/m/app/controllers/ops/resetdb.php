<?php
// team finder ideas
//select E.teamId,TT.pin,S.OID stationId, max(typeCode) stationType from t_event E left join t_station S on E.stationId = S.OID left join t_stationtype T on S.typeId=T.OID left join t_team TT  on E.teamId=TT.OID where E.type = 2 group by teamId;
//select E.teamId,TT.pin,S.OID stationId, max(typeCode) stationType from t_event E left join t_station S on E.stationId = S.OID left join t_stationtype T on S.typeId=T.OID left join t_team TT  on E.teamId=TT.OID where E.type = 2 group by teamId;


class ErrorInfo extends Exception
{
  function __construct($dbh,$msg=null) {
    parent::__construct(ErrorInfo::makeMessage($dbh,$msg));
  }
  static function makeMessage($dbh,$msg) {
    $msg = ($msg == null) ? "Error - " : $msg . " Error - ";
    $e = $dbh->errorInfo();
    return $msg . $e[0] . " ". $e[1] . " " .$e[2];
  }
}
function createStations($stationCount,$tag,$typeId) {

	for ($j=0; $j<$stationCount;$j++) {
		$station = new Station();
		$tmp = sprintf("%s%02d",$tag,$j+1);
		$station->set("tag", $tmp);
		$station->set("typeId", $typeId);
		if ($station->create() === false) echo "Create Station $tag failed";
	}	
}
function create_t_stationtype($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_stationtype` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`typeCode` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`hasrPI` bool NOT NULL default false,				
  	`delay` int unsigned NOT NULL default '60',			
 	`instructions` varchar(255) NOT NULL,
	`success_msg` varchar(255) NOT NULL,
	`failed_msg` varchar(255) NOT NULL,
	`retry_msg` varchar(255) NOT NULL,
  	PRIMARY KEY  (`OID`),
	CONSTRAINT `typeCode_unique` UNIQUE KEY (`typeCode`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_stationtype");
}

function create_t_station($dbh) {
	$status = $dbh->exec(
			"CREATE TABLE `t_station` ( "
			."`OID` int unsigned NOT NULL auto_increment, "
			."`CID` int unsigned NOT NULL default '0', "
			."`typeId` int unsigned NOT NULL, "
			."`tag` varchar(255), "
			."PRIMARY KEY  (`OID`), "
			."CONSTRAINT `rpi_tag_unique` UNIQUE KEY (`tag`), "
			."CONSTRAINT `fk_typeId` FOREIGN KEY (`typeId`) REFERENCES `t_stationtype` (`OID`) ON DELETE CASCADE"
			.") ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_station");
}

function create_t_rpi($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_rpi` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`stationId` int unsigned NOT NULL, 
  	`URL` varchar(255) NOT NULL, 
	`lastContact` DATETIME NOT NULL,
	`debug` varchar(255) NOT NULL, 
  	PRIMARY KEY  (`OID`),
	CONSTRAINT FOREIGN KEY (`stationId`) REFERENCES `t_station` (`OID`) ON DELETE CASCADE		
	) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_rpi");
}


function create_t_school($dbh) {
	$status = $dbh->exec(
			"CREATE TABLE `t_school` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
  	`name` varchar(255) NOT NULL,
 	`mascot` varchar(255) NOT NULL,
  	`logo` int unsigned NULL,
  	PRIMARY KEY  (`OID`),
	CONSTRAINT `school_name_unique` UNIQUE KEY (`name`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_school");
}

function create_t_team($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_team` ( "
  	."`OID` int unsigned NOT NULL auto_increment, "
  	."`CID` int unsigned NOT NULL default '0', "
  	."`name` varchar(255) NOT NULL, "
    ."`pin`  varchar(5) NOT NULL, "
 	."`schoolId` int unsigned NOT NULL, "
			
	."`totalScore` int unsigned NOT NULL default 0, "
	."`regScore` int unsigned NOT NULL default 0, "		
	."`ctsScore` int unsigned NOT NULL default 0, "
	."`fslScore` int unsigned NOT NULL default 0, "
	."`hmbScore` int unsigned NOT NULL default 0, "
	."`cpaScore` int unsigned NOT NULL default 0, "
	."`extScore` int unsigned NOT NULL default 0, "
						
	."`totalDuration` int unsigned NOT NULL default 0, "
	."`regDuration` int unsigned NOT NULL default 0, "
	."`ctsDuration` int unsigned NOT NULL default 0, "
	."`fslDuration` int unsigned NOT NULL default 0, "
	."`hmbDuration` int unsigned NOT NULL default 0, "
	."`cpaDuration` int unsigned NOT NULL default 0, "
	."`extDuration` int unsigned NOT NULL default 0, "
	."`started`	    int unsigned NOT NULL default 0, "
	."`json` varchar(255) NOT NULL, "
  	."PRIMARY KEY  (`OID`), "
	."UNIQUE KEY (`pin`), "
	."CONSTRAINT `team_name_unique` UNIQUE KEY (`name`), "			
	." CONSTRAINT `fk_schoolId` FOREIGN KEY (`schoolId`) REFERENCES `t_school` (`OID`) ON DELETE CASCADE "
	.") ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_team");
}

function create_t_user($dbh)
{
  $status = $dbh->exec(
	"CREATE TABLE `t_user` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
  	`permissions` int unsigned NOT NULL default '0',
  	`username` varchar(255) NOT NULL,
  	`passwordHash` varchar(40) NOT NULL,
  	`email` varchar(255) NOT NULL,  	
  	`fullname` varchar(255) NOT NULL,	
  	`created_dt` DATETIME NOT NULL,
  	PRIMARY KEY  (`OID`),
 	CONSTRAINT `user_email_unique` UNIQUE KEY (`email`),
  	CONSTRAINT `user_username_unique` UNIQUE KEY (`username`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_user");

}

function create_t_event($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_event` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
    `created_dt` DATETIME NOT NULL,
  	`teamId` int unsigned NOT NULL,
  	`stationId` int unsigned NOT NULL default '0',
 	`eventType` int NOT NULL,
	`points` int NOT NULL,			
  	`data` varchar(255) NOT NULL,
  	PRIMARY KEY  (`OID`),"
	." CONSTRAINT `fk_teamId_event` FOREIGN KEY (`teamId`) REFERENCES `t_team` (`OID`),"
    ." CONSTRAINT `fk_stationId` FOREIGN KEY (`stationId`) REFERENCES `t_station` (`OID`)"
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_event");
}

function create_t_cts_data($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_cts_data` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`stationId` int unsigned NOT NULL,
    `_1st` FLOAT NOT NULL,
	`_2nd` FLOAT NOT NULL,
	`_3rd` FLOAT NOT NULL,
	`_4th` FLOAT NOT NULL,
	`_5th` FLOAT NOT NULL,
    `tolerance` FLOAT NOT NULL, "
	."CONSTRAINT `fk_cts_stationid` FOREIGN KEY (`stationId`) REFERENCES `t_station` (`OID`) ON DELETE CASCADE, "
  	."PRIMARY KEY  (`OID`) "
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_cts_data");	
}

function create_t_fsl_data($dbh) {
	$status = $dbh->exec(
			"CREATE TABLE `t_fsl_data` ( "
			."`OID` int unsigned NOT NULL auto_increment, "
			."`CID` int unsigned NOT NULL default '0', "
			."`tag` varchar(255) NOT NULL, "
			."`lat1` decimal(12,8) NOT NULL, "
			."`lng1` decimal(12,8) NOT NULL, "
			."`lat2` decimal(12,8) NOT NULL, "
			."`lng2` decimal(12,8) NOT NULL, "
			."`lat3` decimal(12,8) NOT NULL, "
			."`lng3` decimal(12,8) NOT NULL, "	
			."`rad1` int NOT NULL, "
			."`rad2` int NOT NULL, "
			."`rad3` int NOT NULL, "			
			."PRIMARY KEY  (`OID`) "
			.") ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_station");
}
function create_t_hmb_data($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_hmb_data` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`_1st` int unsigned NOT NULL,	
    `_2nd` int unsigned NOT NULL,
    `_3rd` int unsigned NOT NULL,		
  	PRIMARY KEY  (`OID`)"
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_hmb_data");
}

function create_t_cpa_data($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_cpa_data` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`velocity` int unsigned NOT NULL,
    `velocity_tolerance` int unsigned NOT NULL,
    `window_time` int unsigned NOT NULL,
    `window_time_tolerance` int unsigned NOT NULL,
    `pulse_width` int unsigned NOT NULL,
    `pulse_width_tolerance` int unsigned NOT NULL,
    `combo` int unsigned NOT NULL,
  	PRIMARY KEY  (`OID`)"
			." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_cpa_data");
}

function create_t_ext_data($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_ext_data` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`todo` varchar(255) NOT NULL,		
  	PRIMARY KEY  (`OID`)"
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_ext_data");
}

function create_v_stationfinder($dbh) {
   $status = $dbh->exec("create view v_stationfinder as "
   		."select S.tag,T.hasrPI,R.stationId,R.URL,S.typeId,T.name from t_rpi R "
   		."left join t_station S on S.OID=R.stationId "
   		."left join t_stationtype T on S.typeId=T.OID"
   		);
   
    if ($status === false) throw new ErrorInfo($dbh,"v_stationfinder");
}


function create_v_leaderboard_main($dbh) {
	$status = $dbh->exec("create view v_leaderboard_main as "	
	."select name Name  , totalDuration Duration , totalScore Score, "
	."regScore Reg,ctsScore CTS ,fslScore FSL,hmbScore HMB,cpaScore CPA"
	." from t_team order by Duration desc, Score asc"
	);
	
	if ($status === false) throw new ErrorInfo($dbh,"v_leaderboard_main");
}

function create_v_leaderboard_ext($dbh) {
	$status = $dbh->exec("create view v_leaderboard_ext as "
			."select name Name  , extDuration Duration , extScore Score from t_team order by Duration desc, Score asc"
	);

	if ($status === false) throw new ErrorInfo($dbh,"v_leaderboard_ext");
}

function dropView($dbh, $view) {
  if ($dbh->exec("DROP VIEW if exists ".$view) === false) {
    throw new ErrorInfo($dbh,"dropView " . $view);
  }
}

function dropTable($dbh, $table) {
  if ($dbh->exec("DROP table if exists ".$table) === false) {
    throw new ErrorInfo($dbh,"dropTable " . $table);
  }
}

function _resetdb() {
	
	if ( !isset($_POST['dataOption']) ) {
		echo "error";
		exit;
	}
	$dataOption = $_POST['dataOption'];

  try
  {
    $dbh=getdbh();

    $list = explode(",","v_stationfinder,v_leaderboard_main,v_leaderboard_ext");
    foreach ($list as $view) dropView($dbh, $view);

    
    //
    //  rPI challenge data
    //
    $list = explode(",", "t_cts_data,t_fsl_data,t_hmb_data,t_cpa_data,t_ext_data");
    foreach ($list as $table) dropTable($dbh, $table);

    $list = explode(",", "t_event,t_user,t_rpi,t_station,t_stationtype,t_team,t_school");
    foreach ($list as $table) dropTable($dbh, $table);

    create_t_user          ($dbh);
    create_t_stationtype   ($dbh);
    create_t_station       ($dbh);
    create_t_school        ($dbh);
    create_t_team          ($dbh);
    create_t_event         ($dbh);
    create_t_rpi           ($dbh);
    
    create_v_leaderboard_main($dbh);
    create_v_leaderboard_ext($dbh);
    ///create_v_stationfinder($dbh);
    //
    //  rPI challenge data
    //
    create_t_cts_data($dbh);
    create_t_fsl_data($dbh);
    create_t_hmb_data($dbh);
    create_t_cpa_data($dbh);
    create_t_ext_data($dbh);

    $admin = new User();
    $admin->set('username',"admin");
    $admin->setPassword('pass');
    $admin->set('email',"dcarreir@harris.com");
    $admin->set('fullname',"administrator");
    $admin->setRoll(USER::ROLL_ADMIN);
    $admin->create();
        
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_REG, "Register", false, 60,
       "Welcome [team] to the Design Challenge! Your app has successfully communicated with the Master Server! Congratulations!",
       "If you see this message there was an internal error 1",
       "If you see this message there was an internal error 2",
       "If you see this message there was an internal error 3"
    );
    
    if ($stationType===false) echo "Create StationType REG failed";
    else createStations(1,"reg",$stationType->get('OID'));
    	

    $stationType = StationType::makeStationType(StationType::STATION_TYPE_CTS,"Crack The Safe"            ,true, 60,
      "Welcome, [team] Your first assignment is to break into Professor Aardvark's safe where you will find the first clue to his Secret Laboratory. Measure the interior angles and pick the three correct angles for the safe combination. Good luck! clue=[clue]",
      "Success! Go quickly to the next team queue.",
       "You have failed the challenge. Go quickly to the next team queue.",
       "No luck, better try again!"
    );
    if ($stationType===false) echo "Create StationType CTS failed";
    else createStations(6,"cts",$stationType->get('OID'));
    
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_FSL,"Find Secret Lab"           ,false, 60,
       "Find and scan the marker at [lat] [lng].",
       "Success! Find and scan the next marker at [lat] [lng].",
       "Too bad, you failed. Find and scan the next marker at [lat] [lng].",
       "Wrong marker, try again!"
    		
    		//Success! Go quickly to the next team queue.
    		//Wrong Secret Laboratory marker, try again!
    		//Too bad, you failed. Go quickly to the next team queue.
    );
    if ($stationType===false) echo "Create StationType FSL failed";
    else createStations(1,"fsl",$stationType->get('OID'));
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_HMB,"Defuse Hypermutation Bomb" ,false, 60,
     	"The HMB has been triggered! Send the Energy Pulsator cycle time quickly!",
     	"Success! Go quickly to the next team queue.",
     	"Oops. Enough said. Go quickly to the next team queue.",
     	"Nope, better try again!"
    );
    if ($stationType===false) echo "Create StationType HMB failed";
    else createStations(6,"hmb",$stationType->get('OID'));
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_CPA,"Catch Provessor Aardvark"   ,true, 60,
       "PA is trying to escape. Quickly measure fence=[fence] building=[building] and scan Start QR Code.",
     		
     		//"Watch now as the professor attempts to escape. Get him!"
     		"Success! Go quickly to the team finish area.",
     		"Professor Aardvark has escaped. Oh well. Go quickly to the team finish area.",
     		"Miss! Try again!"
    );
    if ($stationType===false) echo "Create StationType CPA failed";
    else createStations(6,"cpa",$stationType->get('OID'));
    
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_EXT,"Extra"                     ,false, 60,
     "You have 20 (TBR) minutes to provide the tower location and height. Good luck. [waypoint1-lat=+dd.dddddd] [waypoint1-lon=+dd.dddddd] [waypoint2-lat=+dd.dddddd] [waypoint2-lon=+dd.dddddd] [waypoint3-lat=+dd.dddddd] [waypoint3-lon=+dd.dddddd]",
      "success",
      "failed",
      "retry"
    );
    if ($stationType===false) echo "Create StationType EXT failed";
    else createStations(1,"ext",$stationType->get('OID'));
    
    if ($dataOption == 0) {
        redirect('mgmt_main','Database Initialized without test data!');
        return;
    }
    
    // generate test data
    
    for ($i=1;$i < 21; $i++) {
    	$user = new User();
    	$user->set('username','user'.$i);
    	$user->setPassword('pass'.$i);
    	$user->set('email','email'.$i."@harris.com");
    	$user->set('fullname','User #'.$i);
    	if ($user->create()===false) echo "Create user $i failed";
    }
    
    $mascots = explode(",","Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded");
    $schools   = explode(",", "Titusville HS,Edgewood Jr/Sr HS,Holy Trinity,West Shore Jr/Sr HS,Melbourne HS,Palm Bay Magnet HS,Bayside HS");
    for ($i=0; $i<count($schools); $i++)
    {
    	$school = new School();
    	$school->set("name",$schools[$i]);
    	$school->set("mascot",$mascots[$i]);
    	if ($school->create() === false) echo "Create School $i failed";
    }
    $names = explode(",","00001,00002,00003,00004,00005,00006,00007,00008,00009,00010,00011,00012,00013,00014");
    $pins = explode(",","00001,00002,00003,00004,00005,00006,00007,00008,00009,00010,00011,00012,00013,00014");
    for ($i=0; $i<count($names);$i++)
    {
      $team = new Team();
      $team->set("name",$names[$i]);
      $team->set("schoolId", (int)(($i+1)/2) + (int)(($i+1)%2));  // hack we know the order the schools were added
      $team->set("pin", $pins[$i]); 
      if ($team->create() === false) echo "Create team $i failed";
    }
    for ($i=1; $i<= 5; $i++)
    {
      $cts = new CTSData();
      $station = Station::getFromTag("cts0".$i);
      $cts->set('stationId',$station->get('OID')); // hack assume get works
      $cts->set('_1st',1);
      $cts->set('_2nd',2);
      $cts->set('_3rd',2);
      $cts->set('_4th',2);
      $cts->set('_5th',2);
      $cts->set('tolerance',5.0);
      if ($cts->create() === false) echo "Create CTS $i failed";
    }
/*
    $events = array(
    	array('pin'=>"00001", 'tag'=>"cts01", 'retries'=>1 ),
        array('pin'=>"00002", 'tag'=>"cts02", 'retries'=>1 )
    );
    foreach ( $events as $event )
    {
    	x($event);
    	
    }
    */
   redirect('mgmt_main','Database Initialized test data!');
    
  }
  catch(ErrorInfo $e)
  {
    echo $e->getMessage();
  }

}
function x($e)
{
	$team = Team::getFromPin($e['pin']);
	$station = Station::getFromTag($e['tag']);
	$r = Event::createEvent(Event::TYPE_START, $team, $station, 0);
}
