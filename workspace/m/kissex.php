<?php
//  iSms Extensions
//
class ModelEx extends KISS_Model  {

	protected $ckname;


	function __construct($pkname='', $ckname='',$tablename='',$dbhfnname='getdbh',$quote_style='MYSQL',$compress_array=true) {
		parent::__construct($pkname , $tablename , $dbhfnname , $quote_style , $compress_array);

		$this->ckname=$ckname; // Name of concurrency id for optimistic lock

	}

	//Inserts record into database with a new auto-incremented primary key
	//If the primary key is empty, then the PK column should have been set to auto increment
	function create() {
		$this->rs[$this->ckname] = 1;  // start the concurrency counter at 1
		return parent::create();
	}

	function retrieve($pkvalue,$ckvalue=0) {
		
		if ($ckvalue == -1) return parent::retrieve($pkvalue);
	
		$dbh=$this->getdbh();
		$sql = 'SELECT * FROM '.$this->enquote($this->tablename).' WHERE '.$this->enquote($this->pkname).'=? and ' .$this->enquote($this->ckname).'=?';		
		$stmt = $dbh->prepare($sql);
		$stmt->bindValue(1,(int)$pkvalue);
		$stmt->bindValue(2,(int)$ckvalue);
		$stmt->execute();
		$rs = $stmt->fetch(PDO::FETCH_ASSOC);
		if ($rs)
			foreach ($rs as $key => $val)
				if (isset($this->rs[$key]))
					$this->rs[$key] = is_scalar($this->rs[$key]) ? $val : unserialize($this->COMPRESS_ARRAY ? gzinflate($val) : $val);
		return $this;
	}
	
	
	function update() {
		$dbh=$this->getdbh();
		$s='';
		$this->rs[$this->ckname]++;				// next sequence
		foreach ($this->rs as $k => $v)
			$s .= ','.$this->enquote($k).'=?';
		$s = substr($s,1);
		$sql = 'UPDATE '.$this->enquote($this->tablename).' SET '.$s .' WHERE '
		.$this->enquote($this->pkname).'=? and '
		.$this->enquote($this->ckname).'=?';
		$stmt = $dbh->prepare($sql);
		$i=0;
		foreach ($this->rs as $k => $v)
			$stmt->bindValue(++$i,is_scalar($v) ? $v : ($this->COMPRESS_ARRAY ? gzdeflate(serialize($v)) : serialize($v)) );
		$stmt->bindValue(++$i,$this->rs[$this->pkname]);
		$stmt->bindValue(++$i,$this->rs[$this->ckname]-1);
		return $stmt->execute();
	}

	function delete() {
		$dbh=$this->getdbh();
		$sql = 'DELETE FROM '.$this->enquote($this->tablename).' WHERE '
		.$this->enquote($this->pkname).'=? and '
		.$this->enquote($this->ckname).'=?';
		$stmt = $dbh->prepare($sql);
		$stmt->bindValue(1,$this->rs[$this->pkname]);
		$stmt->bindValue(2,$this->rs[$this->ckname]);
		return $stmt->execute();
	}
	
	//returns true if primary key and concurrency id is a positive integer
	//if checkdb is set to true, this function will return true if there exists such a record in the database

	function exists($checkdb=false) {
		if ((int)$this->rs[$this->pkname] < 1)
			return false;
		if ((int)$this->rs[$this->ckname] < 1)
			return false;
		if (!$checkdb)
			return true;
			
		$dbh=$this->getdbh();
		$sql = 'SELECT 1 FROM '.$this->enquote($this->tablename).' WHERE '
		.$this->enquote($this->pkname)."='".$this->rs[$this->pkname]."' and "
		.$this->enquote($this->ckname)."='".$this->rs[$this->ckname]."'";
		$result = $dbh->query($sql)->fetchAll();
		return count($result);
	}
	# HACK for Master Server
	# 
	function retrieveRandom() {
		
		$dbh=$this->getdbh();		
		$stmt = $dbh->query('SELECT max(oid) FROM '.$this->enquote($this->tablename));
		$oid=$stmt->fetchColumn();
	    $oid=rand(0,$oid);
	    return $this->retrieve($oid,-1);
	}
	#for master server loaddb
	function truncateTable() {
		$dbh=$this->getdbh();
		$stmt = $dbh->query('TRUNCATE TABLE '.$this->enquote($this->tablename));
		
	}
}
