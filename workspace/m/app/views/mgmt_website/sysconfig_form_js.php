<script type="text/javascript">
  function validateForm(f) {

	  if (f.webfolder.value == "") {
      alert("Please enter web folder");
      f.webfolder.focus();
      return false;
    }

    if (f.webdomain.value == "") {
        alert("Please enter webdomain");
        f.webdomain.focus();
        return false;
    }

    if (f.paypal_return.value == "") {
        f.paypal_return.value = f.webdomain.value;
    }

       
    if (f.dbhost.value == "") {
        alert("Please enter dbhost");
        f.dbhost.focus();
        return false;
    }
    if (f.dbname.value == "") {
        alert("Please enter dbname");
        f.dbname.focus();
        return false;
    } 
    if (f.dbuser.value == "") {
        alert("Please enter dbuser");
        f.dbuser.focus();
        return false;
    }
    if (f.dbpass.value == "") {
        alert("Please enter dbpass");
        f.dbpass.focus();
        return false;
    }    
    f.submit();
  }
</script>