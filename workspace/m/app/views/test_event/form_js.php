<script type="text/javascript">
  function validateForm(f) {
	  /*
    if (f.name.value == "") {
      alert("Please enter a station name");
      f.name.focus();
      return false;
    }
    if (f.gpsLocation.value == "") {
        alert("Please enter the gps Location");
        f.gpsLocation.focus();
        return false;
      }*/
    if (f.description.value == "") {
        alert("Please enter a description long.");
        f.description.focus();
        return false;
      }   
    f.submit();
  }
</script>