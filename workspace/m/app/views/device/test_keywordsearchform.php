<form method="post" action="<?=$actionUrl?>">
<div>
<table style="width: auto">
	<thead>
		<tr>
			<th>Search</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>words<br />
			<input style="width: 120px" type="text" name="keywords"
				value="<?php echo $keywords?>" /> <input class="button"
				style="width: 45px; margin-left: 5px" type="submit" name="submit"
				value="Search" /></td>
		</tr>
	</tbody>
</table>
</div>
</form>
