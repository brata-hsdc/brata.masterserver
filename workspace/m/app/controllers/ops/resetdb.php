<?php
// team finder
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
	`typeCode` int(10) NOT NULL,
	`name` varchar(255) NOT NULL,
	`hasrPI` bool NOT NULL default false,				
  	`delay` int(10) unsigned NOT NULL default '60',			
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
			."`OID` int(10) unsigned NOT NULL auto_increment, "
			."`CID` int(10) unsigned NOT NULL default '0', "
			."`typeId` int(10) unsigned NOT NULL, "
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
	`stationId` int(10) unsigned NOT NULL, 
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
  	`name` varchar(255) NOT NULL,
 	`mascot` varchar(255) NOT NULL,
  	`logo` int(10) unsigned NULL,
  	PRIMARY KEY  (`OID`),
	CONSTRAINT `school_name_unique` UNIQUE KEY (`name`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_school");
}

function create_t_team($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_team` ( "
  	."`OID` int(10) unsigned NOT NULL auto_increment, "
  	."`CID` int(10) unsigned NOT NULL default '0', "
  	."`name` varchar(255) NOT NULL, "
    ."`pin`  varchar(5) NOT NULL, "
 	."`schoolId` int(10) unsigned NOT NULL, "
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
  	`permissions` int(10) unsigned NOT NULL default '0',
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
    `created_dt` DATETIME NOT NULL,
  	`teamId` int(10) unsigned NOT NULL,
  	`stationId` int(10) unsigned NOT NULL default '0',
 	`eventType` int(10) NOT NULL,
	`points` int(10) NOT NULL,			
  	`data` varchar(255) NOT NULL,
  	PRIMARY KEY  (`OID`),"
	." CONSTRAINT `fk_teamId` FOREIGN KEY (`teamId`) REFERENCES `t_team` (`OID`),"
    ." CONSTRAINT `fk_stationId` FOREIGN KEY (`stationId`) REFERENCES `t_station` (`OID`)"
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_event");
}

function create_t_cts_data($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_cts_data` (
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
	`tag` varchar(255) NOT NULL,
    `_1st` FLOAT NOT NULL,
	`_2nd` FLOAT NOT NULL,
	`_3rd` FLOAT NOT NULL,
	`_4th` FLOAT NOT NULL,
	`_5th` FLOAT NOT NULL,
    `tolerance` FLOAT NOT NULL,
	CONSTRAINT `cts_tag_unique` UNIQUE KEY (`tag`),
  	PRIMARY KEY  (`OID`)"
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_cts_data");	
}

function create_t_fsl_data($dbh) {
	$status = $dbh->exec(
			"CREATE TABLE `t_fsl_data` ( "
			."`OID` int(10) unsigned NOT NULL auto_increment, "
			."`CID` int(10) unsigned NOT NULL default '0', "
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
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
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
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

function create_v_scores($dbh) {
	$status = $dbh->exec("create view v_scores as "
			."select T.name team, E.stationId Station, ST.name name ,sum(E.points) score from t_event E "
			."left join t_team T on E.teamid=T.OID " 
			."left join t_station S on E.stationid=S.OID "
			."left join t_stationtype ST on E.stationid=ST.OID "
			."group by E.teamid,E.stationId order by E.teamid"
	);

	if ($status === false) throw new ErrorInfo($dbh,"v_scores");
}

function create_v_leaderboard($dbh) {
	$status = $dbh->exec("create view v_leaderboard as "	
	."select T.name team ,sum(E.points) score from t_event E "
	."left join t_team T on E.teamid=T.OID group by E.teamid order by score desc"
	);
	
	if ($status === false) throw new ErrorInfo($dbh,"v_leaderboard");
}


function create_v_duration($dbh) {
	$status = $dbh->exec("create view v_duration as "
			 ."select t1.teamid,t1.stationid,timediff(stop,start) "
             ."from "
             ."(SELECT teamid,stationid,min(created_dt) AS 'start' FROM t_event GROUP BY teamid,stationid) t1 "
             ."left join "
             ."(SELECT teamid,stationid,max(created_dt) AS 'stop' FROM t_event GROUP BY teamid,stationid) t2 "
             ."on "
             ." t1.teamid = t2.teamid and t1.stationid = t2.stationid"
	         );

	if ($status === false) throw new ErrorInfo($dbh,"v_duration");
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

    $list = explode(",","v_stationfinder,v_duration,v_leaderboard,v_scores");
    foreach ($list as $view) dropView($dbh, $view);


    $list = explode(",", "t_event,t_user,t_rpi,t_station,t_stationtype,t_team,t_school");
    foreach ($list as $table) dropTable($dbh, $table);

    create_t_user          ($dbh);
    create_t_stationtype   ($dbh);
    create_t_station       ($dbh);
    create_t_school        ($dbh);
    create_t_team          ($dbh);
    create_t_event         ($dbh);
    create_t_rpi           ($dbh);
    
//    create_v_duration($dbh);
    ///create_v_scores($dbh);
    ///create_v_leaderboard($dbh);
    ///create_v_stationfinder($dbh);
    //
    //  rPI challenge data
    //
    $list = explode(",", "t_cts_data,t_fsl_data,t_hmb_data,t_cpa_data,t_ext_data");
    foreach ($list as $table) dropTable($dbh, $table);
    
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
        
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_REG, "Register", false, 0,
       "Welcome [team] to the Design Challenge! Your app has successfully communicated with the Master Server! Congratulations!",
       "If you see this message there was an internal error 1",
       "If you see this message there was an internal error 2",
       "If you see this message there was an internal error 3"
    );
    
    if ($stationType===false) echo "Create StationType REG failed";
    else createStations(1,"reg",$stationType->get('OID'));
    	

    $stationType = StationType::makeStationType(StationType::STATION_TYPE_CTS,"Crack The Safe"            ,true, 0,
      "Welcome, [team] Your first assignment is to break into Professor Aardvark's safe where you will find the first clue to his Secret Laboratory. Measure the interior angles and pick the three correct angles for the safe combination. Good luck! [clue=rrsG]",
      "Success! Go quickly to the next team queue.",
       "You have failed the challenge. Go quickly to the next team queue.",
       "No luck, better try again!"
    );
    if ($stationType===false) echo "Create StationType CTS failed";
    else createStations(6,"cts",$stationType->get('OID'));
    
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_FSL,"Find Secret Lab"           ,false, 0,
       "Find and scan the first marker at [waypoint-lat=+dd.dddddd] [waypoint-lon=+dd.dddddd].",
       "Success! Find and scan the 2nd marker at [waypoint-lat=+dd.dddddd] [waypoint-lon=+dd.dddddd].",
       "Too bad, you failed. Find and scan the second marker at [waypoint-lat=+dd.dddddd] [waypoint-lon=+dd.dddddd].",
       "Wrong first marker, try again!"
    		
    		//Success! Go quickly to the next team queue.
    		//Wrong Secret Laboratory marker, try again!
    		//Too bad, you failed. Go quickly to the next team queue.
    );
    if ($stationType===false) echo "Create StationType FSL failed";
    else createStations(1,"fsl",$stationType->get('OID'));
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_HMB,"Defuse Hypermutation Bomb" ,false, 0,
     	"The HMB has been triggered! Send the Energy Pulsator cycle time quickly!",
     	"Success! Go quickly to the next team queue.",
     	"Oops. Enough said. Go quickly to the next team queue.",
     	"Nope, better try again!"
    );
    if ($stationType===false) echo "Create StationType HMB failed";
    else createStations(6,"hmb",$stationType->get('OID'));
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_CPA,"Catch Provessor Aardvark"   ,true, 0,
       "PA is trying to escape. Quickly measure [fence=d] [building=d] and scan Start QR Code.",
     		
     		//"Watch now as the professor attempts to escape. Get him!"
     		"Success! Go quickly to the team finish area.",
     		"Professor Aardvark has escaped. Oh well. Go quickly to the team finish area.",
     		"Miss! Try again!"
    );
    if ($stationType===false) echo "Create StationType CPA failed";
    else createStations(6,"cpa",$stationType->get('OID'));
    
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_EXT,"Extra"                     ,false, 0,
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

    $events = array(
    	array('pin'=>"00001", 'tag'=>"cts01", 'retries'=>1 ),
        array('pin'=>"00002", 'tag'=>"cts02", 'retries'=>1 )
    );
    foreach ( $events as $event )
    {
    	x($event);
    	
    }
    // TODO why is this or some other message not still sent back to indicate the DB load is done?
   //redirect('mgmt_main','Database Initialized test data!');
    
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
