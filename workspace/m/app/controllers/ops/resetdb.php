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
 ."`fslScore0` int unsigned NOT NULL default 0, "
 ."`fslScore1` int unsigned NOT NULL default 0, "
 ."`fslScore2` int unsigned NOT NULL default 0, "
 ."`fslScore3` int unsigned NOT NULL default 0, "
 ."`hmbScore` int unsigned NOT NULL default 0, "
 ."`cpaScore` int unsigned NOT NULL default 0, "
      
 ."`totalDuration` int unsigned NOT NULL default 0, "
 ."`regDuration` int unsigned NOT NULL default 0, "
 ."`ctsDuration` int unsigned NOT NULL default 0, "
 ."`fslDuration` int unsigned NOT NULL default 0, "
 ."`hmbDuration` int unsigned NOT NULL default 0, "
 ."`cpaDuration` int unsigned NOT NULL default 0, "
 ."`extDuration` int unsigned NOT NULL default 0, "
 ."`towerD`      FLOAT NOT NULL default 0.0,"
 ."`towerH`      FLOAT NOT NULL default 0.0,"		
 ."`count`     int unsigned NOT NULL default 0, "   
 ."`started`     int unsigned NOT NULL default 0, "
 ."`json` TEXT NOT NULL, "
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
   `data` TEXT NOT NULL,
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
   ."`a_tag` varchar(255) NOT NULL, "
   ."`a_lat` decimal(12,8) NOT NULL, "
   ."`a_lng` decimal(12,8) NOT NULL, "
   ."`b_tag` varchar(255) NOT NULL, "
   ."`b_lat` decimal(12,8) NOT NULL, "
   ."`b_lng` decimal(12,8) NOT NULL, "
   ."`c_tag` varchar(255) NOT NULL, "
   ."`c_lat` decimal(12,8) NOT NULL, "
   ."`c_lng` decimal(12,8) NOT NULL, " 
   ."`l_tag` varchar(255) NOT NULL, "
   ."`l_lat` decimal(12,8) NOT NULL, "
   ."`l_lng` decimal(12,8) NOT NULL, " 
   ."`a_rad` float NOT NULL, "
   ."`b_rad` float NOT NULL, "
   ."`c_rad` float NOT NULL, "   
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
 `_1st_on`  int unsigned NOT NULL, 
 `_1st_off` int unsigned NOT NULL,
    `_2nd_on`  int unsigned NOT NULL,
 `_2nd_off` int unsigned NOT NULL,
    `_3rd_on`  int unsigned NOT NULL,  
    `_3rd_off` int unsigned NOT NULL,
    `cycle`    int unsigned NOT NULL,
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
 `label` varchar(255) NOT NULL,
 `fence` int unsigned NOT NULL,
    `building` int unsigned NOT NULL,
    `sum` int unsigned NOT NULL," 
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
 `a_lat` decimal(8,6) NOT NULL,
 `a_lng` decimal(8,6) NOT NULL,
 `b_lat` decimal(8,6) NOT NULL,
 `b_lng` decimal(8,6) NOT NULL,
 `c_lat` decimal(8,6) NOT NULL,
 `c_lng` decimal(8,6) NOT NULL,
 `t_lat` decimal(8,6) NOT NULL,
 `t_lng` decimal(8,6) NOT NULL,
 `height` int unsigned NOT NULL,
   PRIMARY KEY  (`OID`)"
 ." ) ENGINE=InnoDB DEFAULT CHARSET=latin1"
 );
 if ($status === false) throw new ErrorInfo($dbh,"t_ext_data");
}

function create_v_leaderboard_main($dbh) {
 $status = $dbh->exec("create view v_leaderboard_main as " 
 ."select name Name  , totalDuration Duration , totalScore Score, "
 ."regScore Reg,ctsScore CTS ,fslScore0 FSL0,fslScore1 FSL1,fslScore2 FSL2,fslScore3 FSL3,hmbScore HMB,cpaScore CPA"
 ." from t_team order by Duration asc, Score desc"
 );
 
 if ($status === false) throw new ErrorInfo($dbh,"v_leaderboard_main");
}

function create_v_ext_ranks($dbh) {
 $status = $dbh->exec("create view v_ext_ranks as select OID,name,towerH,towerD,extDuration, "
 ."find_in_set(towerH, (select group_concat( towerH order by towerH desc) from t_team)) as T, "
 ."find_in_set(towerD, (select group_concat( towerD order by towerH desc) from t_team)) as H, "
 ."find_in_set(extDuration, (select group_concat( extDuration order by extDuration desc) from t_team)) as E "
 ."from t_team where extDuration > 0"
 );

 if ($status === false) throw new ErrorInfo($dbh,"v_leaderboard_ext");
}

function create_v_leaderboard_ext($dbh) {
	$status = $dbh->exec("create view v_leaderboard_ext as select OID,name as Name,towerD,towerH,extDuration as Duration,3*T+3*H+E as Score from v_ext_ranks");
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

    $list = explode(",","v_leaderboard_main,v_ext_ranks,v_leaderboard_ext");
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
    create_v_ext_ranks($dbh);
    create_v_leaderboard_ext($dbh);
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
       "Hello! You have been successfully registered and may start the competition. Good luck!",
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
       "Find and scan the [ordinal] at [waypoint-lat=[lat]] [waypoint-lon=[lng]].",
       "Success! Find and scan the [ordinal] marker at [waypoint-lat=[lat]] [waypoint-lon=[lng]].",
       "Too bad, you failed. Find and scan the [ordinal] marker at [waypoint-lat=[lat]] [waypoint-lon=[lng]].",
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
    
     $stationType = StationType::makeStationType(StationType::STATION_TYPE_CPA,"Catch Provessor Aardvark"   ,true, 2000,
       "PA is trying to escape. Quickly measure the [fence=label] [building=[label]] and scan Start QR Code.",
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
     ." [waypoint1-lat=[a_lat]] [waypoint1-lon=[a_lng]]"
     ." [waypoint2-lat=[b_lat]] [waypoint2-lon=[b_lng]]"
     ." [waypoint3-lat=[c_lat]] [waypoint3-lon=[c_lng]]",
      "Message received, return to base",
      "M didn't understand your message",
      "If you see this message there was an internal error 5"
    );
    if ($stationType===false) echo "Create StationType EXT failed";
    else createStations(1,"ext",$stationType->get('OID'));
    
    if ($dataOption == 0) {
        redirect('mgmt_main','Database Initialized without test data!');
        return;
    }
    
    // generate test data
    
   // for ($i=1;$i < 21; $i++) {
   //  $user = new User();
   //  $user->set('username','user'.$i);
   //  $user->setPassword('pass'.$i);
   //  $user->set('email','email'.$i."@harris.com");
   //  $user->set('fullname','User #'.$i);
   //  if ($user->create()===false) echo "Create user $i failed";
   // }
    
    // keep an equal number of each of these items.
    $mascots = explode(",", "Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded,Unencoded,Encoded");
    $schools = explode(",", "Titusville HS,Edgewood Jr/Sr HS,Holy Trinity,West Shore Jr/Sr HS,Melbourne HS,Palm Bay Magnet HS,Bayside HS");
    // keep twice as many name&pins we will populate 2 teams / school
    $names   = explode(",", "team1,team2,team3,team4,team5,team6,team7,team8,team9,team10,team11,team12,team13,team14");
    $pins    = explode(",", "00001,00002,00003,00004,00005,00006,00007,00008,00009,00010,00011,00012,00013,00014");
    
    // always make the schools
    $numSchools = count($schools);
    for ($i=0; $i<$numSchools; $i++)
    {
     $school = new School();
     $school->set("name",$schools[$i]);
     $school->set("mascot",$mascots[$i]);
     if ($school->create() === false) echo "Create School $i failed";
     $schools[$i] = $school->get('OID');  // replace school name with OID for next part
    }
    
    // TODO always make the teams with random ids
    $numTeams = ($dataOption == 1) ? 2 : count($names);
    for ($i=0; $i<$numTeams;$i++)
    {
      $team = new Team();
      $team->set("name",$names[$i]);
      $team->set("schoolId", $schools[$i/2]); /*use OID from previous step two teams / school */
      $team->set("pin", $pins[$i]); 
      
      // to test ext we need special test data
      $team->set('extDuration',$i*100);
      $team->set('towerH',$i);
      $team->set('towerD',$i);
      
      if ($team->create() === false) echo "Create team $i failed";

    }
    for ($i=1; $i<= (($dataOption==1)?1:5); $i++)
    {
      $cts = new CTSData();
      $station = Station::getFromTag("cts0".$i);
      if ($station === false) break;
      $cts->set('stationId',$station->get('OID')); // hack assume get works
      if (isStudentServer() && $i == 1){
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
     if ($i== 1) {
     	$cpa->set('label', $i);
     	$cpa->set('fence', 240);
     	$cpa->set('building',127);
     	$cpa->set('sum',367);
     } else {
     	$cpa->set('label', $i);
     	$cpa->set('fence', 240+$i);
     	$cpa->set('building',127-$i);
     	$cpa->set('sum',367);     	
     }
     if ($cpa->create() === false) echo "Create CTA $i failed";
   }
   $hmb = new HMBData();
   $hmb->set('_1st_on'  , 1);
   $hmb->set('_1st_off' , 1);
   $hmb->set('_2nd_on'  , 1);
   $hmb->set('_2nd_off' , 10);
   $hmb->set('_3rd_on'  , 1);
   $hmb->set('_3rd_off' , 22);
   $hmb->set('cycle'    , 506);
   if ($hmb->create() === false) echo "Create HMB $i failed";
   
   $fsl_data = array(
     array("1", +28.030924, -80.601834, "1", +28.032708, -80.600032, "1", +28.031670, -80.598559, "1", +28.031062, -80.600013, 665.8, 600.1, 574.6),
     array("1", +28.030924, -80.601834, "1", +28.032708, -80.600032, "1", +28.031670, -80.598559, "2", +28.030975, -80.600107, 629.9, 632.4, 618.6),
     array("1", +28.030924, -80.601834, "1", +28.032708, -80.600032, "1", +28.031670, -80.598559, "3", +28.030859, -80.600018, 662.5, 674.1, 608.6)
   );
   for ($i=0;$i<count($fsl_data);$i++)
   {
     $fsl = new FSLData();
     $fsl->set('a_tag',$fsl_data[$i][0]);
     $fsl->set('a_lat',$fsl_data[$i][1]);
     $fsl->set('a_lng',$fsl_data[$i][2]);
     $fsl->set('b_tag',$fsl_data[$i][3]);
     $fsl->set('b_lat',$fsl_data[$i][4]);
     $fsl->set('b_lng',$fsl_data[$i][5]);
     $fsl->set('c_tag',$fsl_data[$i][6]);
     $fsl->set('c_lat',$fsl_data[$i][7]);
     $fsl->set('c_lng',$fsl_data[$i][8]);
     $fsl->set('l_tag',$fsl_data[$i][9]);
     $fsl->set('l_lat',$fsl_data[$i][10]);
     $fsl->set('l_lng',$fsl_data[$i][11]);
     $fsl->set('a_rad',$fsl_data[$i][12]);
     $fsl->set('b_rad',$fsl_data[$i][13]);
     $fsl->set('c_rad',$fsl_data[$i][14]);
     if ($fsl->create() === false) echo "Create FSLData $i failed";
   }
     
   $ext = new EXTData();
   $ext->set('a_lat', +28.031848);
   $ext->set('a_lng', -80.600938);
   $ext->set('b_lat', +28.031695);
   $ext->set('b_lng', -80.600413);
   $ext->set('c_lat', +28.031579);
   $ext->set('c_lng', -80.600873);
   $ext->set('t_lat', +28.031698);
   $ext->set('t_lng', -80.600755);
   $ext->set('height', 102);
   if ($ext->create() === false) echo "Create EXTData $i failed";
   redirect('mgmt_main','Database Initialized test data!');
    
  }
  catch(ErrorInfo $e)
  {
    echo $e->getMessage();
    die;
  }

}

