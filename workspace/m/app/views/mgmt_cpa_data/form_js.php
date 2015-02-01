<script type="text/javascript">
  function validateForm(f) {
    if (f.stationId.value == -1) {
      alert("Please enter tag");
	  f.stationId.focus();
	  return false;
	}

    if (f.velocity.value == "") {
      alert("Please enter a velocity");
      f.velocity.focus();
      return false;
    }
    if (f.velocity_tolerance.value == "") {
        alert("Please enter the velocity tolerance");
        f.velocity_tolerance.focus();
        return false;
     }
    if (f.window_time.value == "") {
        alert("Please enter a window time");
        f.window_time.focus();
        return false;
      }
      if (f.window_time_tolerance.value == "") {
          alert("Please enter the window time tolerance");
          f.window_time_tolerance.focus();
          return false;
       }   
      if (f.pulse_width.value == "") {
          alert("Please enter a pulse  width");
          f.pulse_width.focus();
          return false;
        }
        if (f.pulse_width_tolerance.value == "") {
            alert("Please enter the pulse width tolerance");
            f.pulse_width_tolerance.focus();
            return false;
         }
        if (f.fence.value == "") {
            alert("Please enter the fence id");
            f.fence.focus();
            return false;
         }
        if (f.building.value == "") {
            alert("Please enter the building id");
            f.building.focus();
            return false;
         }
        
    f.submit();
  }
</script>
