<?php
function _test_show_request()
{
echo "SERVER DATA";
print_r($_SERVER);
if (count($_POST) ) {
	echo "POST DATA";
    print_r($_POST);
}
if (count($_GET)) {
	echo "GET DATA";
	print_r($_GET);
}
if (count ($_FILES))
{
   echo "FILES";
   print_r($_FILES);
}
$input = file_get_contents( 'php://input' );
if (strlen($input)) echo "body is $input";
}