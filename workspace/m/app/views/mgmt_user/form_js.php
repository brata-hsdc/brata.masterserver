<script type="text/javascript">
  function validateForm(f) {
    if (f.username.value == "") {
      alert("Please enter a user");
      f.username.focus();
      return false;
    }
    /*
    if (f.password.value == "") {
        alert("Please enter a password");
        f.password.focus();
        return false;
    }
    if (f.confirm.value == "" || f.password.value != f.confirm.value) {
        alert("Please confirm password");
        f.confirm.focus();
        return false;
    }
    */
    if (f.password.value != f.confirm.value) {
        alert("Confirm password mismatch");
        f.confirm.focus();
        return false;
    }   
    if (f.fullname.value == "") {
        alert("Please enter full name");
        f.confirm.focus();
        return false;
    }    
    if (f.permissions.selectedIndex <=0) {
        alert("Please select a roll");
        f.permissions.focus();
        return false;
    }
    f.submit();
  }
</script>