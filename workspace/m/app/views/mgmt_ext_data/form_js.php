<script type="text/javascript">
  function validateForm(f) {

    if (f.a_lat.value == "") {
      alert("Please enter a_lat");
      f.a_lat.focus();
      return false;
    }
    if (f.a_lng.value == "") {
      alert("Please enter a_lng");
      f.a_lng.focus();
      return false;
    }        
    if (f.b_lat.value == "") {
      alert("Please enter b_lat");
      f.b_lat.focus();
      return false;
    }
    if (f.b_lng.value == "") {
      alert("Please enter b_lng");
      f.b_lng.focus();
      return false;
    }
    if (f.c_lat.value == "") {
      alert("Please enter c_lat");
      f.c_lat.focus();
      return false;
    }
    if (f.c_lng.value == "") {
      alert("Please enter c_lng");
      f.c_lng.focus();
      return false;
    }
    if (f.t_lat.value == "") {
        alert("Please enter t_lat");
        f.t_lat.focus();
        return false;
    }
    if (f.t_lng.value == "") {
      alert("Please enter t_lng");
      f.t_lng.focus();
      return false;
    }
    if (f.height.value == "") {
        alert("Please enter height");
        f.height.focus();
        return false;
     }
    f.submit();
  }
</script>