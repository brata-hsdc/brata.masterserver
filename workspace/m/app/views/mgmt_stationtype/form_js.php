<script type="text/javascript">
  function validateForm(f) {
   
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
    if (f.correct_msg.value == "") {
        alert("Please enter the 'correct' message");
        f.correct_msg.focus();
        return false;
      }
    if (f.incorrect_msg.value == "") {
        alert("Please enter the 'incorrect' message");
        f.incorrect_msg.focus();
        return false;
      }
    if (f.failed_msg.value == "") {
        alert("Please enter the 'failed' message");
        f.failed_msg.focus();
        return false;
      }
    f.submit();
  }
</script>