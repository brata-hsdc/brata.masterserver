<script type="text/javascript">
  function validateForm(f) {

    if (f._1st.value == "") {
      alert("Please enter 1st");
      f._1st.focus();
      return false;
    }
    if (f._2nd.value == "") {
        alert("Please enter 2nd");
        f._2nd.focus();
        return false;
      }    
    if (f._3rd.value == "") {
        alert("Please enter 3rd");
        f._3rd.focus();
        return false;
      }
    if (f.tolerance.value == "") {
        alert("Please enter tolerance");
        f.tolerance.focus();
        return false;
      }          
    f.submit();
  }
</script>