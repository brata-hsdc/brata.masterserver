<script type="text/javascript">
  function validateForm(f) {
    if (f.name.lat == "") {
      alert("Please enter waypoint lat");
      f.lat.focus();
      return false;
    }
    if (f.name.lng == "") {
        alert("Please enter waypoint lng");
        f.lng.focus();
        return false;
      }
    if (f.name.description == "") {
        alert("Please enter waypoint description");
        f.description.focus();
        return false;
      }   
    f.submit();
  }
</script>