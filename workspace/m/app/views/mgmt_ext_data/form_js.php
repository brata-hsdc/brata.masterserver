<script type="text/javascript">
  function validateForm(f) {

    if (f.waypoint1_lat.value == "") {
      alert("Please enter waypoint1_lat");
      f.waypoint1_lat.focus();
      return false;
    }
    if (f.waypoint1_lng.value == "") {
      alert("Please enter waypoint1_lng");
      f.waypoint1_lng.focus();
      return false;
    }        
    if (f.waypoint2_lat.value == "") {
      alert("Please enter waypoint2_lat");
      f.waypoint2_lat.focus();
      return false;
    }
    if (f.waypoint2_lng.value == "") {
      alert("Please enter waypoint2_lng");
      f.waypoint2_lng.focus();
      return false;
    }
    if (f.waypoint3_lat.value == "") {
      alert("Please enter waypoint3_lat");
      f.waypoint3_lat.focus();
      return false;
    }
    if (f.waypoint3_lng.value == "") {
      alert("Please enter waypoint3_lng");
      f.waypoint3_lng.focus();
      return false;
    }
    f.submit();
  }
</script>