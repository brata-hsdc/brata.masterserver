
<form method="post" action=<?="$actionUrl" ?> >
  <table>
    <tr><th colspan="2">Reset Database</th></tr>
    <tr>
      <td>Test Data Option</td>
      <td>
      <select name='dataOption' >
         <option value=0 > No Test Data</option>
         <option value=1 > With Test Data (short)</option>
         <option value=1 > With Test Data (long)</option>
      </select>
      </td>
    </tr>

    <tr>
      <td colspan="2" style="text-align:right">
        <input type="button" value="Cancel" onclick="location.href='<?=$cancelUrl ?>' " />
        <input type="Submit" value="Reset Database" /> 
      </td>
    </tr>
    
  </table>
</form>
