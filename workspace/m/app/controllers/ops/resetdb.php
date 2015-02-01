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
			."`teamAtStation` int unsigned default '0', "	
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
	."`count`	    int unsigned NOT NULL default 0, "			
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
	`stationId` int unsigned NOT NULL,
	`velocity` int unsigned NOT NULL,
    `velocity_tolerance` int unsigned NOT NULL,
    `window_time` int unsigned NOT NULL,
    `window_time_tolerance` int unsigned NOT NULL,
    `pulse_width` int unsigned NOT NULL,
    `pulse_width_tolerance` int unsigned NOT NULL,
    `fence` int unsigned NOT NULL,
    `building` int unsigned NOT NULL, "
    ."CONSTRAINT `fk_cpa_stationid` FOREIGN KEY (`stationId`) REFERENCES `t_station` (`OID`) ON DELETE CASCADE, "	
  	. " PRIMARY KEY  (`OID`)"
	." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
	);
	if ($status === false) throw new ErrorInfo($dbh,"t_cpa_data");
}

function create_t_ext_data($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_ext_data` (
  	`OID` int unsigned NOT NULL auto_increment,
  	`CID` int unsigned NOT NULL default '0',
	`waypoint1_lat` decimal(8,6) NOT NULL,
	`waypoint1_lng` decimal(8,6) NOT NULL,
	`waypoint2_lat` decimal(8,6) NOT NULL,
	`waypoint2_lng` decimal(8,6) NOT NULL,
	`waypoint3_lat` decimal(8,6) NOT NULL,
	`waypoint3_lng` decimal(8,6) NOT NULL,
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
       "Hello! You have been successfully registered and may start the competition.",
       "If you see this message there was an internal error 1",
       "If you see this message there was an internal error 2",
       "If you see this message there was an internal error 3"
    );
    
    if ($stationType===false) echo "Create StationType REG failed";
    else createStations(1,"reg",$stationType->get('OID'));
    	

    $stationType = StationType::makeStationType(StationType::STATION_TYPE_CTS,"Crack The Safe"            ,true, 60,
      "Welcome, Team! Your first assignment is to break into Professor Aardvark's safe where you will find the first clue to his Secret Laboratory. Measure the interior angles and pick the three correct angles for the safe combination. Good luck! [clue=[clue]]",
      "Success! Go quickly to the next team queue.",
       "You have failed the challenge. Go quickly to the next team queue.",
       "No luck, better try again!"
    );
    $numStations = ($dataOption == 1) ? 1 : 6;
    if ($stationType===false) echo "Create StationType CTS failed";
    else createStations($numStations,"cts",$stationType->get('OID'));
    
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_FSL,"Find Secret Lab"           ,false, 60,
       "Find and scan the marker at [waypoint-lat=[lat]] [waypoint-lon=[lng]].",
       "Success! Find and scan the next marker at [waypoint-lat=[lat]] [waypoint-lon=[lng]].",
       "Too bad, you failed. Find and scan the next marker at waypoint-lat=[lat] waypoint-lon=[lng].",
       "Wrong marker, try again!"
    		
    		//Success! Go quickly to the next team queue.
    		//Wrong Secret Laboratory marker, try again!
    		//Too bad, you failed. Go quickly to the next team queue.
    );
    
    if ($stationType===false) echo "Create StationType FSL failed";
    else createStations(1,"fsl",$stationType->get('OID'));
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_HMB,"Defuse Hypermutation Bomb" ,true, 60,
     	"The HMB has been triggered! Send the Energy Pulsator cycle time quickly!",
     	"Success! Go quickly to the next team queue.",
     	"Oops. Enough said. Go quickly to the next team queue.",
     	"Nope, better try again!"
    );
     
    $numStations = ($dataOption == 1) ? 1 : 6;
    if ($stationType===false) echo "Create StationType HMB failed";
    else createStations($numStations,"hmb",$stationType->get('OID'));
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_CPA,"Catch Provessor Aardvark"   ,true, 60,
       //"PA is trying to escape. Quickly measure [fence=[fence]] [building=[building]] and scan Start QR Code.",
     		"Watch now as the professor attempts to escape. Get him!",
     		"Success! Go quickly to the team finish area.",
     		"Professor Aardvark has escaped. Oh well. Go quickly to the team finish area.",
     		"Miss! Try again!"
    );
     
    $numStations = ($dataOption == 1) ? 1 : 6;
    if ($stationType===false) echo "Create StationType CPA failed";
    else createStations($numStations,"cpa",$stationType->get('OID'));
    
    $stationType = StationType::makeStationType(StationType::STATION_TYPE_EXT,"Extra"                     ,false, 60,
     "You have 20 (TBR) minutes to provide the tower location and height. Good luck."
     ." waypoint1-lat=[waypoint1-lat] waypoint1-lng=[waypoint1-lng]"
     ."	waypoint2-lat=[waypoint2-lat] waypoint2-lng=[waypoint2=lng]"
     ." waypoint3-lat=[waypoint3-lat] waypoint3-lng=[waypoint3-lng]",
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
    
   // for ($i=1;$i < 21; $i++) {
   // 	$user = new User();
   // 	$user->set('username','user'.$i);
   // 	$user->setPassword('pass'.$i);
   // 	$user->set('email','email'.$i."@harris.com");
   // 	$user->set('fullname','User #'.$i);
   // 	if ($user->create()===false) echo "Create user $i failed";
   // }
    
    if ($GLOBALS['SYSCONFIG_STUDENT'] == 1) {
    	$mascots = explode(",","Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded");
    	$schools = explode(",", "Titusville HS,Edgewood Jr/Sr HS,Holy Trinity,West Shore Jr/Sr HS,Melbourne HS,Palm Bay Magnet HS,Bayside HS");
    } else {
    	$mascots = explode(",", "Tigers,Bulldogs");
    	$schools = explode(",","Bayside High,Valley High");
    }
    
    for ($i=0; $i<count($schools); $i++)
    {
    	$school = new School();
    	$school->set("name",$schools[$i]);
    	$school->set("mascot",$mascots[$i]);
    	if ($school->create() === false) echo "Create School $i failed";
    }
    
    if ($GLOBALS['SYSCONFIG_STUDENT'] == 1) {
    	$names = explode(",","team1,team2,team3,team4,team5,team6,team7,team8,team9,team10,team11,team12,team13,team14");
    	$pins = explode(",","00001,00002,00003,00004,00005,00006,00007,00008,00009,00010,00011,00012,00013,00014");
    	 
    } else {
    	$names = explode(",", "Tigers,Bulldogs");
    	$pins  = explode(",","00001,00002");
    }
    
    for ($i=0; $i<count($names);$i++)
    {
      $team = new Team();
      $team->set("name",$names[$i]);
      if ($GLOBALS['SYSCONFIG_STUDENT'] == 1)
      	$team->set("schoolId", (int)(($i+1)/2) + (int)(($i+1)%2));  // hack we know the order the schools were added
      else    
      	$team->set("schoolId",$i+1);  // hack we know the order the schools were added
      $team->set("pin", $pins[$i]); 
      if ($team->create() === false) echo "Create team $i failed";
    }
    for ($i=1; $i<= (($dataOption==1)?1:5); $i++)
    {
      $cts = new CTSData();
      $station = Station::getFromTag("cts0".$i);
      if ($station === false) break;
      $cts->set('stationId',$station->get('OID')); // hack assume get works
      if ($GLOBALS['SYSCONFIG_STUDENT'] == 1 and $i == 1){
        $cts->set('_1st',39);
        $cts->set('_2nd',57);
        $cts->set('_3rd',13);
        $cts->set('_4th',23);
        $cts->set('_5th',48);
      }
      else {
        $cts->set('_1st',10+$i);
        $cts->set('_2nd',20+$i);
        $cts->set('_3rd',30+$i);
        $cts->set('_4th',40+$i);
        $cts->set('_5th',50+$i);
      }
      $cts->set('tolerance',5.0);
      if ($cts->create() === false) echo "Create CTS $i failed";
    }
    for ($i=1; $i<= (($dataOption==1)?1:5); $i++)
    {
      $cpa = new CPAData();
      $station = Station::getFromTag("cpa0".$i);
      if ($station === false) break;
      $cpa->set('stationId',$station->get('OID')); // hack assume get works
      $cpa->set('velocity',8000);
      $cpa->set('velocity_tolerance',1000);
      $cpa->set('window_time',10000);
      $cpa->set('window_time_tolerance',100);
      $cpa->set('pulse_width',100);
      $cpa->set('pulse_width_tolerance',50);
      $cpa->set('fence',1);
      $cpa->set('building',1);
      if ($cpa->create() === false) echo "Create CTA $i failed";
    }
    for ($i=1; $i<= (($dataOption==1)?1:1); $i++)
    {
      $hmb = new HMBData();
      $hmb->set('_1st',11);
      $hmb->set('_2nd',13);
      $hmb->set('_3rd',17);
      if ($hmb->create() === false) echo "Create HMB $i failed";
    }
    if ($GLOBALS['SYSCONFIG_STUDENT'] == 1)
    {
      $fsl = new FSLData();
      $fsl->set('tag','T-WP');
      $fsl->set('lat1',28.592573);
      $fsl->set('lng1',-80.806185);
      $fsl->set('lat2',28.592480);
      $fsl->set('lng2',-80.806162);
      $fsl->set('lat3',28.592504);
      $fsl->set('lng3',-80.806321);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL T-WP failed";
      $fsl = new FSLData();
      $fsl->set('tag','EW-WP');
      $fsl->set('lat1',28.362813);
      $fsl->set('lng1',-80.696523);
      $fsl->set('lat2',28.362808);
      $fsl->set('lng2',-80.696677);
      $fsl->set('lat3',28.362735);
      $fsl->set('lng3',-80.696516);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL EW-WP failed";
      $fsl = new FSLData();
      $fsl->set('tag','HT-WP');
      $fsl->set('lat1',28.201413);
      $fsl->set('lng1',-80.667392);
      $fsl->set('lat2',28.201522);
      $fsl->set('lng2',-80.667223);
      $fsl->set('lat3',28.201390);
      $fsl->set('lng3',-80.667241);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL HT-WP failed";
      $fsl = new FSLData();
      $fsl->set('tag','WS-WP');
      $fsl->set('lat1',28.108592);
      $fsl->set('lng1',-80.627157);
      $fsl->set('lat2',28.108555);
      $fsl->set('lng2',-80.627252);
      $fsl->set('lat3',28.108511);
      $fsl->set('lng3',-80.627118);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL WS-WP failed";
      $fsl = new FSLData();
      $fsl->set('tag','M-WP');
      $fsl->set('lat1',28.090005);
      $fsl->set('lng1',-80.619992);
      $fsl->set('lat2',28.089905);
      $fsl->set('lng2',-80.619916);
      $fsl->set('lat3',28.089966);
      $fsl->set('lng3',-80.619857);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL M-WP failed";
      $fsl = new FSLData();
      $fsl->set('tag','PB-WP');
      $fsl->set('lat1',28.048604);
      $fsl->set('lng1',-80.619697);
      $fsl->set('lat2',28.048483);
      $fsl->set('lng2',-80.619651);
      $fsl->set('lat3',28.048532);
      $fsl->set('lng3',-80.619796);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL PB-WP failed";
      $fsl = new FSLData();
      $fsl->set('tag','BS-WP');
      $fsl->set('lat1',27.951701);
      $fsl->set('lng1',-80.675085);
      $fsl->set('lat2',27.951616);
      $fsl->set('lng2',-80.675061);
      $fsl->set('lat3',27.951640);
      $fsl->set('lng3',-80.674953);
      $fsl->set('rad1',1);
      $fsl->set('rad2',2);
      $fsl->set('rad3',3);
      if ($fsl->create() === false) echo "Create FSL BS-WP failed";
    }
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
