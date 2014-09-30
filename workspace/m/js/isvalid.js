function isZip(s) 
{
     // Check for correct zip code
     reg = /(^\d{5}$)|(^\d{5}-\d{4})$/;
     return reg.test(s);
}
function isEmail(s)
{
	var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	return reg.test(s);
}
function isPhoneNumber(s) {
    reg = /^\d{3}-\d{3}-\d{4}$/;
    return reg.test(s);
}
function isMMDDYYYY(s) {
	reg = /\d{2}-\d{2}-\d{4}/;
	return reg.test(s);
}