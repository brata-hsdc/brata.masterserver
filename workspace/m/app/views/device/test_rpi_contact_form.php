<form method="post" action="<?=$actionUrl?>">
<div>
<table style="width: auto">
	<thead>
		<tr>
		<th colspan="2">Test rPI Contact Form</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Method</td>
			<td>
	          <select  name="method">
		      <option>GET</option>
			  <option>POST</option>
  			  <option>OPTIONS</option>
			  <option>PUT</option>
			  <option>DELETE</option>
			  <option>HEAD</option>
			  </select>
			</td>
		</tr>
	    <tr>
		  <td>rPI URL</td>
		  <td>
			<input style="width: 120px" type="text" name="rPIUrl"
				value="" /> <input class="button"
				style="width: 45px; margin-left: 5px" type="submit" name="submit"
				value="Contact" />
		  </td>
		</tr>
			    <tr>
		  <td>rPI Data</td>
		  <td>
			<textarea style="width: 120px" name="data"></textarea>
			<input class="button"
				style="width: 45px; margin-left: 5px" type="submit" name="submit"
				value="Contact" />
		  </td>
		</tr>
	</tbody>
</table>
</div>
</form>
