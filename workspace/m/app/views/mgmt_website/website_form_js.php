<script type="text/javascript">
  function validateForm(f) {

    if (!isEmail(f.supportemail.value)) {
        alert("invalid email address ");
        f.supportemail.focus();
        return false;
    }    

    if (!isPhoneNumber(f.supportnumber.value)) {
        alert("Support Number invalid ddd-ddd-dddd ");
        f.supportnumber.focus();        
        return false;
    }
    if (!isPhoneNumber(f.taxfaxnumber.value)) {
        alert("Tax Fax number invalid ddd-ddd-dddd ");
        f.taxfaxnumber.focus(); 
        return false;
    }     
    f.submit();
  }
</script>