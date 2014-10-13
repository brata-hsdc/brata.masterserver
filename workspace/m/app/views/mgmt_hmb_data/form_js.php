<script type="text/javascript">
  function validateForm(f) {

    if (f._1st_on.value == "") {
      alert("Please enter 1st on value");
      f._1st_on.focus();
      return false;
    }
    if (f._1st_off.value == "") {
        alert("Please enter 1st off value");
        f._1st_off.focus();
        return false;
    }

    if (f._2nd_on.value == "") {
        alert("Please enter 2nd on value");
        f._2nd_on.focus();
        return false;
      }
      if (f._2nd_off.value == "") {
          alert("Please enter 2nd off value");
          f._2nd_off.focus();
          return false;
      } 
      if (f._3rd_on.value == "") {
          alert("Please enter 3rd on value");
          f._3rd_on.focus();
          return false;
        }
        if (f._3rd_off.value == "") {
            alert("Please enter 3rd off value");
            f._3rd_off.focus();
            return false;
        }         
    
    f.submit();
  }
</script>