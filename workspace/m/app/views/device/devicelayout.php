<?php 
header("Content-Type: text/plain");
header("Expires: " . gmdate('D, d M Y H:i:s \G\M\T') );
header("Cache-Control: no-cache");
header("Pragma: no-cache");

if ( !isset($statusLine) )
{
 echo '500 Internal error no status line\n\n';
}
else
{
	echo $statusLine . "\n";
	echo (isset($headers) && is_array($headers)) ? implode("\n",$headers) : '';
	echo "\n\n";
	echo (isset($payload) && is_array($payload)) ? implode("\n",$payload) : '';
}