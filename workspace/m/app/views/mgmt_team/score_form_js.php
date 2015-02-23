<script type="text/javascript">
function checkScore(score,field) {
	  if (score.value <0 || score.value > 3 ) {
		    alert(field+" Score must be between 0 and 3");
		    score.focus();
		    return false;
		}
		return true;	
}
function checkDuration(duration,field) {
	  if (duration.value == "" || duration.value < 0 ) {
		    alert(field+" duation must >= 0");
		    duration.focus();
		    return false;
		}
		return true;	
}
function checkTower(tower,field) {
	  if (tower.value == "" || tower.value < 0 ) {
		    alert(field+"  must be >= 0");
		    tower.focus();
		    return false;
		}
		return true;		
}
  function validateForm(f) {   
    if (!checkScore(f.regScore,"REG Score")) return false;
    if (!checkScore(f.ctsScore,"CTS Score")) return false;
    if (!checkScore(f.fslScore0,"FSL Score(waypoint 1)")) return false;
    if (!checkScore(f.fslScore1,"FSL Score(waypoint 2)")) return false;
    if (!checkScore(f.fslScore2,"FSL Score(waypoint 3)")) return false;
    if (!checkScore(f.fslScore3,"FSL Score(Lab)")) return false;    
    if (!checkScore(f.hmbScore,"HMB Score")) return false; 
    if (!checkScore(f.cpaScore,"CPA Score")) return false;
    
    if (!checkTower(f.towerH,"Tower Height")) return false;    
    if (!checkTower(f.towerD,"Tower Distance")) return false;
     
    if (!checkDuration(f.ctsDuration,"CTS Duration")) return false;
    if (!checkDuration(f.fslDuration,"FSL Duration")) return false;  
    if (!checkDuration(f.hmbDuration,"HMB Duration")) return false; 
    if (!checkDuration(f.cpaDuration,"CPA Duration")) return false;
    if (!checkDuration(f.cpaDuration,"EXT Duration")) return false;
    
    f.submit();
  }
</script>