<script type="text/javascript">
  function validateForm(f) {

    if (f.tag.value == "") {
      alert("Please enter a tag");
      f.tag.focus();
      return false;
    }
    if (f.lat1.value == "") {
        alert("Please enter the lat1 value");
        f.lat1.focus();
        return false;
     }
    if (f.lng1.value == "") {
        alert("Please enter the lng1 value");
        f.lng1.focus();
        return false;
      }
      if (f.lat2.value == "") {
          alert("Please enter the lat2 value");
          f.lat2.focus();
          return false;
       }   
      if (f.lng2.value == "") {
          alert("Please enter the lng2 value");
          f.lng2.focus();
          return false;
        }
      if (f.lat3.value == "") {
          alert("Please enter the lat3 value");
          f.lat2.focus();
          return false;
       }   
      if (f.lng3.value == "") {
          alert("Please enter the lng3 value");
          f.lng2.focus();
          return false;
        } 
      if (f.rad1.value == "") {
          alert("Please enter the rad1 value");
          f.rad1.focus();
          return false
        }
      if (f.rad2.value == "") {
          alert("Please enter the rad2 value");
          f.rad2.focus();
          return false;
        }       
      if (f.rad3.value == "") {
          alert("Please enter the rad3 value");
          f.rad3.focus();
          return false;
        }
        
    f.submit();
  }
</script>