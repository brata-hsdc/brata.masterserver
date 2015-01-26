<?php
function _testPage() 
{
  echo "hi";
  $team = Team::getFromPin("00001");
  $jsonObject = array("one"=>1,"two"=>2);
  $station = new Station();
  $team->startChallenge($station, $jsonObject);
  $team = null;
  usleep(500);
  $team = Team::getFromPin("00001");
  var_dump($team->getChallengeData());
  echo "bye";
  die;
}