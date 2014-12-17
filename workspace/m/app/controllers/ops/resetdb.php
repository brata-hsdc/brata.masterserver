<?php
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

function create_t_stationtype($dbh) {
	$status = $dbh->exec(
	"CREATE TABLE `t_stationtype` (
  	`OID` int(10) unsigned NOT NULL auto_increment,
  	`CID` int(10) unsigned NOT NULL default '0',
  	`longName` varchar(255) NOT NULL,
	`shortName` varchar(255) NOT NULL,			
  	`delay` int(10) unsigned NOT NULL default '60',			
 	`instructions` varchar(255) NOT NULL,
	`correct_msg` varchar(255) NOT NULL,
	`incorrect_msg` varchar(255) NOT NULL,
  	PRIMARY KEY  (`OID`)
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
			."CONSTRAINT `rpi_key_unique` UNIQUE KEY (`tag`), "
			."CONSTRAINT `fk_typeId` FOREIGN KEY (`typeId`) REFERENCES `t_stationtype` (`OID`) "
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
  	PRIMARY KEY  (`OID`)
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
	."CONSTRAINT `team-name_unique` UNIQUE KEY (`name`), "			
	." CONSTRAINT `fk_schoolId` FOREIGN KEY (`schoolId`) REFERENCES `t_school` (`OID`)"
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
 	`type` int(10) NOT NULL,
	`points` int(10) NOT NULL,			
  	`description` varchar(255) NOT NULL,
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
	if ($status === false) throw new ErrorInfo($dbh,"t_cts_data");
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

function create_v_scores($dbh) {
	$status = $dbh->exec("create view v_scores as "
			."select T.name team, E.stationId Station, ST.shortName name ,sum(E.points) score from t_event E "
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

    $list = explode(",","v_duration,v_leaderboard,v_scores");
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
    create_v_scores($dbh);
    create_v_leaderboard($dbh);
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

    $stationType = new StationType();
    $stationType->set('longName',"Register");
    $stationType->set('shortName',"REG");
    $stationType->set('delay',0);
    $stationType->set('instructions',"Welcome [team-name]");
    $stationType->set('correct_msg',"not used");
    $stationType->set('incorrect_msg',"not used");
    if ($stationType->create()===false) echo "Create StationType 'Register' failed";
    $station = new Station();
    $station->set("tag", "REG");
    $station->set("typeId", $stationType->get("OID"));
    if ($station->create() === false) echo "Create Station 'REG' failed";
    
    
    $stationNames = explode(",","Crack The Safe,CTS,Find Secret Lab,FSL,Defuse Hypermutation Bomb,HMB,Catch Provessor Aardvark,CPA,Extra,EXT");
    for ($i=0;$i<count($stationNames);$i+=2)
    {
    	$stationType = new StationType();
    	$stationType->set('longName',$stationNames[$i]);
    	$stationType->set('shortName',$stationNames[$i+1]);
    	$stationType->set('delay',60);
    	$stationType->set('instructions',"todo instructions ".$i/2);
    	$stationType->set('correct_msg',"Correct ".$i/2);
    	$stationType->set('incorrect_msg',"Please try again ".$i/2);
    	if ($stationType->create()===false) echo "Create StationType $i failed";
    }
    
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
 
    $stationNames = explode(",", "CTS,FSL");
    for ($i=0; $i<count($stationNames); $i++)
    {
      $stationType = StationType::getFromShortname($stationNames[$i]);
      $station = new Station();
      $station->set("tag", $stationNames[$i]."00");
      $station->set("typeId", $stationType->get("OID"));
      if ($station->create() === false) echo "Create Station $i failed";
    }
    
    $names   = explode(",", "Tigers,Bulldogs");
    $schools = explode(",","Bayside High,Valley High");
    for ($i=0; $i<count($schools); $i++)
    {
    	$school = new School();
    	$school->set("name",$schools[$i]);
    	$school->set("mascot",$names[$i]);
    	if ($school->create() === false) echo "Create School $i failed";
    }
    for ($i=0; $i<count($names);$i++)
    {
      $team = new Team();
      $team->set("name",$names[$i]);
      $team->set("schoolId",$i+1);
      $team->set("pin", Team::generatePIN());
      if ($team->create() === false) echo "Create Team $i failed";
    }
/**
    $numStations = 2;
    for ($s=1; $s<=$numStations; $s++)
    {
      for ($t=1; $t<=count($names);$t++)
      {
    	  $event = new Event();
    	  $time = time();
    	  $event->set('created_dt',unixToMySQL($time));
    	  $event->set('teamId',$t);
    	  $event->set('stationId',$s);
    	  $event->set('type',Event::TYPE_START);
    	  $event->set('points',0);
    	  $event->set('description',"START");
    	  if ($event->create() === false) echo "Create start event $s,$t failed";

    	  if ($t == 2)
    	  {
    	    $event->set("OID",0); $event->set("CID",0); $time += 5;
    	    $event->set('created_dt',unixToMySQL($time));
    	    $event->set('type',Event::TYPE_SUBMIT);
    	    $event->set('points',-1);
    	    $event->set('description',"Incorrect");
    	    if ($event->create() === false) echo "Create submit/incorrect  event $s,$t failed";
    	  }
    	     	  
    	  $event->set("OID",0); $event->set("CID",0); $time += 5;
    	  $event->set('created_dt',unixToMySQL($time));
    	  $event->set('type',Event::TYPE_SUBMIT);
    	  $event->set('points',20);
    	  $event->set('description',"Correct Solution");    	  
    	  if ($event->create() === false) echo "Create  submit/correct Solution event $s,$t failed";
	  
    	  $event->set("OID",0); $event->set("CID",0); $time += 5;
    	  $event->set('type',Event::TYPE_END,$time);
    	  $event->set('description',"eND");
    	  if ($event->create() === false) echo "Create Leave event $s,$t failed";
      }
    }
   **/     
    redirect('mgmt_main','Database Initialized test data!');
    
  }
  catch(ErrorInfo $e)
  {
    echo $e->getMessage();
  }

}