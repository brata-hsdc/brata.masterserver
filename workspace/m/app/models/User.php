<?php
class User extends ModelEx {

  // each section of the mgmt web site gets one bit to control access
  const MGMT_USER   	     =  0x0001;    // user can access mgmt_user
  const MGMT_XXX             =  0x0002;    // user can access open
  const MGMT_STATIONTYPE     =  0x0004;    // user can access mgmt_station type
  const MGMT_STATION         =  0x0008;    // user can access mgmt_station
  const MGMT_MESSAGE         =  0x0010;    // user can access mgmt_message
  const MGMT_WAYPOINT        =  0x0020;    // user can access mgmt_waypoint
  const MGMT_RPI             =  0x0040;    // user can access mgmt_rpi
  const MGMT_SCHOOL          =  0x0080;    // user can access mgmt_school
  const MGMT_STUDENT         =  0x0100;    // user can access mgmt_student
  const MGMT_TEAM            =  0x0200;    // user can access mgmt_team
  const MGMT_WEBSITE         =  0x0400;    // user can access mgmt_website
  const TEST_EVENT           =  0x0800;    // user can access test_event
  const MGMT_CTS_DATA        =  0x1000;    // user can access CTS data
  const MGMT_HMB_DATA        =  0x2000;    // user can access HMB data
  const MGMT_CPA_DATA        =  0x4000;    // user can access CPA data
  const MGMT_EXT_DATA        =  0x8000;    // user can access EXT data
  
  // map permissions into rolls
  const ROLL_ADMIN           = 0xFFFF; 	// access all mgmt;
  const ROLL_ADMIN_ASSISTANT = 0xFFFE;  // access mgmt_reviewstories & mgmt_taxtinfo;
  const ROLL_NONE            = 0x0000;  // no access

  static private function isSelected($value, $selectValue) {
    return $value == $selectValue ? " selected " : "";
  }
  static function getAllAsHtmlOptions($selectValue) {
    return
		 "<option " . User::isSelected(User::ROLL_ADMIN, $selectValue)           . "value=" . User::ROLL_ADMIN . "> Admin"
		 ."<option " . User::isSelected(User::ROLL_ADMIN_ASSISTANT, $selectValue) . "value=" . User::ROLL_ADMIN_ASSISTANT    . "> Admin Assistant";
  }
  static function getPermissionsAsRollText($value) {
    switch ($value)
    {
      case User::ROLL_ADMIN          : return "admin";
      case User::ROLL_ADMIN_ASSISTANT: return "assistant";
      case User::ROLL_NONE           : return "none";
      default: return "Error - unknown Roll";
    }
  }

  function isPermissionSet($permission) {
    return (($this->rs['permissions'] & $permission) != 0) ? true : false;
  }

  function __construct($oid=0,$cid=0) {
    parent::__construct('OID','CID','t_user'); //primary key = oid; tablename = users
    $this->rs['OID'] = $oid;
    $this->rs['CID'] = $cid;
    $this->rs['permissions'] = User::ROLL_NONE;
    $this->rs['username'] = '';
    $this->rs['passwordHash'] = '';
    $this->rs['email'] = "";
    $this->rs['fullname'] = '';
    $this->rs['created_dt'] = '';
    if ($oid && $cid)
    $this->retrieve($oid,$cid);
  }
  function create() {
    $this->rs['created_dt'] = unixToMySQL(time());
    return parent::create();
  }

  public function setRoll($roll) {
    $this->rs['permissions']=$roll;
  }

  public function setPassword($password) {
    $this->rs['passwordHash']=User::encodePassword($password);
  }
  public function sendMail($subject,$message) {
    return $GLOBALS['SETTINGS_SENDMAIL']==1?mail($this->rs['email'],$subject,$message):1;
  }
  public static function encodePassword($password) {
    return sha1($password);
  }
  public static function getUser($username,$password) {
    $password=User::encodePassword($password);
    $user = new User();
    return $user->retrieve_one('username=? and passwordHash=?',array($username,$password));
  }

  public static function getUserByEmail($email) {
    $user = new User();
    return $user->retrieve_one('email=?',$email);
  }
}