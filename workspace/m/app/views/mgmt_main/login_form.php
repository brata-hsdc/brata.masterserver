<form class=form-inline method="post" action="<?php echo myUrl('ops/mgmt_login')?>">
<input type="hidden" name="LoginForm" value="1" />
<label>User name</label>
<input placeholder="user name" name="username" value="<?php echo $username?>" />
<label>Password</label>
<input placeholder="password" type="password" name="password" value="" />
<button type="submit" class="btn">Login</button>
</form>