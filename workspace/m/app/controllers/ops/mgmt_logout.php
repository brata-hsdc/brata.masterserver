<?php
function _mgmt_logout() {
  loginClearMgmt();
  redirect('mgmt_main','You have logged out!');
}