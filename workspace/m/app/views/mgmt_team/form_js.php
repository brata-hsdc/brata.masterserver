<script type="text/javascript">
  function validateForm(f) {
    if (f.name.value == "") {
      alert("Please enter a team name");
      f.name.focus();
      return false;
    }
    if (f.schoolId.value.value == -1) {
        alert("Please enter a school name");
        f.name.focus();
        return false;
      }   
    f.submit();
  }
</script>