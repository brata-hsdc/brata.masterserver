<script type="text/javascript">
  function validateForm(f) {
    if (f.typeId.value == -1) {
      alert("Please enter a station type");
      f.name.focus();
      return false;
    }

    if (f.description.value == "") {
        alert("Please enter a description long.");
        f.description.focus();
        return false;
      }   
    f.submit();
  }
</script>