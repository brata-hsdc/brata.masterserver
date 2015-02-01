<script type="text/javascript">
  function validateForm(f) {

    if (f.a_tag.value == "") {
      alert("Please enter a_tag");
      f.a_tag.focus();
      return false;
    }
    if (f.a_lat.value == "") {
        alert("Please enter the a_lat value");
        f.a_lat.focus();
        return false;
     }
    if (f.a_lng.value == "") {
        alert("Please enter the a_lng value");
        f.a_lng.focus();
        return false;
      }
    if (f.b_tag.value == "") {
        alert("Please enter b_tag");
        f.b_tag.focus();
        return false;
      }
      if (f.b_lat.value == "") {
          alert("Please enter the b_lat value");
          f.b_lat.focus();
          return false;
       }   
      if (f.b_lng.value == "") {
          alert("Please enter the b_lng value");
          f.b_lng.focus();
          return false;
        }
      if (f.c_tag.value == "") {
          alert("Please enter c_tag");
          f.c_tag.focus();
          return false;
        }
      if (f.c_lat.value == "") {
          alert("Please enter the c_lat value");
          f.c_lat.focus();
          return false;
       }   
      if (f.c_lng.value == "") {
          alert("Please enter the c_lng value");
          f.c_lng.focus();
          return false;
        } 
      if (f.l_tag.value == "") {
          alert("Please enter the l_tag value");
          f.l_tag.focus();
          return false;
       }
      if (f.l_lat.value == "") {
          alert("Please enter the l_lat value");
          f.l_lat.focus();
          return false;
       }   
      if (f.l_lng.value == "") {
          alert("Please enter the l_lng value");
          f.l_lng.focus();
          return false;
        } 
      if (f.a_rad.value == "") {
          alert("Please enter the a_rad value");
          f.a_rad.focus();
          return false
        }
      if (f.b_rad.value == "") {
          alert("Please enter the b_rad value");
          f.b_rad.focus();
          return false;
        }       
      if (f.c_rad.value == "") {
          alert("Please enter the c_rad value");
          f.c_rad.focus();
          return false;
        }
        
    f.submit();
  }
</script>