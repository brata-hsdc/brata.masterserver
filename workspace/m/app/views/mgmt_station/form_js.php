<script type="text/javascript">
  function validateForm(f) {
    if (f.typeId.value == -1) {
      alert("Please enter a station type");
      f.typeId.focus();
      return false;
    }
   
    if (f.tag.value == "") {
        alert("Please enter a station name");
        f.description.focus();
        return false;
      }  
    f.submit();
  }
</script>