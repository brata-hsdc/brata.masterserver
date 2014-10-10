<script type="text/javascript">
  function validateForm(f) {
    if (f.text.value == "") {
      alert("Please enter message text");
      f.text.focus();
      return false;
    }
    if (f.waypointId.value == -1) {
        alert("Please select a waypoint name");
        f.waypointId.focus();
        return false;
      } 
   
    f.submit();
  }
</script>