<?php 
function _showlog($n=300) {
  trace("showlog",__FILE__,__LINE__,__FUNCTION__);
  $filename = $GLOBALS['LOGFILE'];
  echo "<h1>Last $n lines of log</h1>";
  echo "<p>NOTE: maybe less if log has less data</p>";
  echo "<pre>";
  if (is_readable($filename)) echo passthru("tail -n$n $filename");
  else                        echo "no log file yet";
  echo "</pre>";
  echo "<p>use the back button on your browser</p>";
}