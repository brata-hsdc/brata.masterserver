<script type="text/javascript">
  function validateForm(f) {
   
    if (f.delay.value == "") {
        alert("Please enter a delay value (numeric)");
        f.delay.focus();
        return false;
      } 
    if (f.instructions.value == "") {
        alert("Please enter instructions for this station type");
        f.instructions.focus();
        return false;
      }
    if (f.success_msg.value == "") {
        alert("Please enter the 'success' message");
        f.success_msg.focus();
        return false;
      }
    if (f.failed_msg.value == "") {
        alert("Please enter the 'failed' message");
        f.failed_msg.focus();
        return false;
      }
    if (f.retry_msg.value == "") {
        alert("Please enter the 'retry' message");
        f.retry_msg.focus();
        return false;
      }
    f.submit();
  }
</script>