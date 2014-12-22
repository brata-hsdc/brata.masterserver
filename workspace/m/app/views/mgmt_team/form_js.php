<script type="text/javascript">
  function validateForm(f) {
    if (f.name.value == "") {
      alert("Please enter a team name");
      f.name.focus();
      return false;
    }
    if (f.schoolId.value == -1) {
        alert("Please select a school");
        f.schoolId.focus();
        return false;
      }   
    f.submit();
  }
</script>