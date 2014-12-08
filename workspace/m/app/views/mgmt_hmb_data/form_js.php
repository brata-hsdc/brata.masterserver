<script type="text/javascript">
function validateForm(f) 
{
  if (f._1st.value == "") {
    alert("Please enter 1st value");
	f._1st.focus();
	return false;
  }
  if (f._2nd.value == "") {
    alert("Please enter 2nd value");
    f._2nd.focus();
    return false;
  }
  if (f._3rd.value == "") {
    alert("Please enter 3rd value");
	f._3rd.focus();
	return false;
  }	             
    
  f.submit();
}
</script>