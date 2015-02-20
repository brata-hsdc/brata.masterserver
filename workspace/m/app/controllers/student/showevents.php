<?php
function _showevents($n=0) {
  $n=(int)$n;
  $data['body'][]='<h2>Show Events</h2><br />';
  _make_html_table($n,$data);
  View::do_dump(VIEW_PATH.'layouts/studentlayout.php',$data);
}

function _make_html_table($n,&$data) {
  $dbh=getdbh();

  //pagination
  $stmt = $dbh->query('SELECT count(OID) total FROM t_event');
  $total=$stmt->fetchColumn();
  $limit=$GLOBALS['pagination']['per_page'];
  $data['body'][]='<p>Showing records '.($n+1).' to '. min($total,($n+$limit)).' of '.$total.'</p>';
  $data['body'][]=pagination::makePagination($n,$total,myUrl('mgmt_user/manage'),$GLOBALS['pagination']);

  //table
  $stmt = $dbh->query("SELECT created_dt,teamId,stationId,points,data FROM t_event LIMIT $n,$limit");
  $tablearr[]=explode(',','created_dt,teamId,stationId,points,data');
  while ($rs = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $row=null;
    foreach ($tablearr[0] as $f) {
    	$row=htmlspecialchars($rs[$f]);
    }
    $tablearr[]=$row;
  };
  $data['body'][]=table::makeTable($tablearr);
  $data['head'][]='<script type="text/javascript" src="'.myUrl('js/jsconfirm.js').'"></script>';
}
