<?php
function _mgmt_login() {
  $username=trim($_POST['username']);
  $password=trim($_POST['password']);

  $user=User::getUser($username,$password);
  if ($user === false) {
    loginClearMgmt();
    redirect('mgmt_main/login/'.$username,'Login Failed!');
  }

  //Login Succeeded
  loginSetMgmt($user);
  redirect('mgmt_main');
}