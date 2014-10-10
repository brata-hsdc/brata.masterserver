<script type="text/javascript">
  function validateForm(f) {
    if (f.shortName.value == "") {
      alert("Please enter a short name");
      f.shortName.focus();
      return false;
    }
    if (f.longName.value == "") {
        alert("Please enter a long Name name");
        f.longNnme.focus();
        return false;
      }   
    if (f.delay.value == "") {
        alert("Please enter a delay value (numberic)");
        f.longNnme.focus();
        return false;
      } 
    if (f.instructions.value == "") {
        alert("Please enter instructions for this station type");
        f.instructions.focus();
        return false;
      }
    f.submit();
  }
</script>