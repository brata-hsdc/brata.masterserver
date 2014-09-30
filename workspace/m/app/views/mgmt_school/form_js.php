<script type="text/javascript">
  function validateForm(f) {
    if (f.name.value == "") {
      alert("Please enter a school name");
      f.name.focus();
      return false;
    }
    if (f.mascot.value == "") {
        alert("Please enter the mascot name");
        f.mascot.focus();
        return false;
      }
   
    f.submit();
  }
</script>