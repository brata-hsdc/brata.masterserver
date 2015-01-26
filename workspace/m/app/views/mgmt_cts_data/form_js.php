<script type="text/javascript">
  function validateForm(f) {
	  
	 if (f.stationId.value == -1) {
	   alert("Please enter tag");
	   f.stationId.focus();
	   return false;
	}

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
    if (f._4th.value == "") {
        alert("Please enter 4th");
        f._4th.focus();
        return false;
      }
    if (f._5th.value == "") {
        alert("Please enter 5th");
        f._5th.focus()
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