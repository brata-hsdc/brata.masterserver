<script type="text/javascript">
  function validateForm(f) {

    if (f.todo.value == "") {
      alert("Please enter todo");
      f.todo.focus();
      return false;
    }
        
    f.submit();
  }
</script>