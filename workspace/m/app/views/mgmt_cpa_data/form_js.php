<script type="text/javascript">
  function validateForm(f) {
    if (f.label.value == -1) {
      alert("Please enter a label from this value set");
	  f.which.focus();
	  return false;
	}

    if (f.fence.value == "") {
      alert("Please enter a fence value");
      f.vence.focus();
      return false;
    }
    if (f.building.value == "") {
        alert("Please enter the building value");
        f.building.focus();
        return false;
     }
    if (f.sum.value == "") {
        alert("Please enter the sum value");
        f.sum.focus();
        return false;
      }
 
    f.submit();
  }
</script>
