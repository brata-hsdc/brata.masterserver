<script type="text/javascript">
  function validateForm(f) {
    if (f.name.value == "") {
      alert("Please enter message text");
      f.name.focus();
      return false;
    }
   
    f.submit();
  }
</script>