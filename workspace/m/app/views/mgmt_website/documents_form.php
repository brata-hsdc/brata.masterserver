<form enctype="multipart/form-data" action="<?=myUrl('mgmt_website/ops_documents_update')?>" method="POST">
  <table>
    <tr>
      <td>Document Slot:
      </td>
      <td>
        <select name="document_slot">
          <option value='terms'>Terms Of Use</option>
          <option value='privacy'>Privacy Statement</option>
        </select>
      </td>
    </tr>
    <tr>
      <td>PDF File</td> 
      <td><input name="document" type="file" /></td>
   </tr>
   <tr>
     <td colspan=2 >
        <input type="button" value="Cancel" onclick="location.href='<?=$cancel ?>' " />
        <input type="submit" value="Upload PDF" />
     </td>
   </tr>
  </table>
</form>