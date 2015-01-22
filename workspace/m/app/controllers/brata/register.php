<?php
// brata reports team start challenge at station
//
require(APP_PATH.'inc/rest_functions.php');
require(APP_PATH.'inc/json_functions.php');
function _register() 
{
	trace("start",__FILE__,__LINE__,__METHOD__);
	
	$json = json_getObjectFromRequest("POST");
	//if ($json === NULL) return;
	json_checkMembers("team_id,message", $json);
        $teamPIN = $json['team_id'];
	if ($teamPIN === null) {
		trace("missing PIN",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(400,"missing team PIN");  // doesn't return
	}
	
	$team = Team::getFromPin($teamPIN);
	if ($team === false) {
		trace("_can't find team PIN=".$teamPIN,__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(404,"missing can't find team PIN=".$teamPIN);  // doesn't return
	}
	
	// we are assuming that the QR code won't include the station tag.
	$station = Station::getRegistrationStation();
	if ($station === false) {
		trace("can't find registration station",__FILE__,__LINE__,__METHOD__);
		rest_sendBadRequestResponse(500, "can't find registration station");
	}

        $points = 3;
	if (Event::createEvent(Event::TYPE_REGISTER,$team, $station,$points) === false) {
	  trace("createEvent Fails",__FILE__,__LINE__,__METHOD__);
	  rest_sendBadRequestResponse(500, "could not create event object");	
	}
/***********************
        // TODO deconflict the hack and Dan's long term plan 
        //$stationType = StationType::getFromTypeCode($station->get('tag'));
        $stationType = StationType::getFromTypeCode("reg01");
        $teamNumber = (int)$teamPIN;
        // TODO this should be a DB look  up
        $schools = array(1 => "Titusville HS", "", "Edgewood Jr/Sr HS", "", "Holy Trinity", "", "West Shore Jr/Sr HS", "", "Melbourne HS", "", "Palm Bay Magnet HS", "", "Bayside HS", "");
        if ($teamNumber > sizeof($schools)+1 or $teamNumber < 1){
	  trace("createEvent Fails",__FILE__,__LINE__,__METHOD__);
          rest_sendBadRequestResponse(404, "can't find team PIN");	
        }
        $welcome = sprintf("Welcome %s to the Design Challenge! Your app has successfully communicated with the Master Server! Congratulations!", $schools[$teamNumber]);
        if ($teamNumber%2 == 0){
          // TODO call encryption algorithm on welcome for now use canned
          $schools = array(1 => "", "Wgweeil!tc_hoY_moteuh_reT__iaMtpaupss_tvheiarls_l_Sese_urHcvSce_erts!os__fCtuohlnelg_yrD_aectsouimlgmanut_niCiohcnaaslt!le~ed~n_~",
            "", "W/np_tCeS_pcholrC_oenc_hhm_goHaamMrmSlsuaae_l_nst_tesituEonuceld_gcaragtect_teh!eeSiwe_sdeoo_Ys_rnoDofwvsdeuuie!_srltr~Ji_lh!~rgay__~",
            "", "Weie!tl_hcY_ootmuhere___HaMopalpsy_t_heTarrs_i_Snseiurtcvyce_erts!os__fCtuohlnelg_yrD_aectsouimlgmanut_niCiohcnaaslt!le~ed~n_~gw~",
            "", "WJi_lh!ergay__l/np_tCcS_pchoorC_oenm_hhm_geHaamMr_SlsuaaW_l_nstetesitusonucelt_gcara_tect_tSh!eeSihe_sdeoo_Ys_rnrDofwvseeuuie!_srltr~",
            "", "Weie!tl_hcY_ootmuhere___MaMepalpsb_toheuarrs_n_Sese_urHcvSce_erts!os__fCtuohlnelg_yrD_aectsouimlgmanut_niCiohcnaaslt!le~ed~n_~gw~",
            "", "Wggay__ennp_tCle_pchoctC_oeno_hhm_gmHaamMreSlsuaa__l_nstPtesituaonucell_gcaramtect_t_h!eeSiBe_sdeoa_Ys_rnyDofwvs_euuie!Msrltr~ai_lh!~",
            "", "We_e!wl_icYtoohmu_ert__hBaeap_ypMs_aihsdatese__rHs_SuS_cetcroev_setsrhf!eu__lCDloeyns_gicrgoanmt_muCulhnaaitlcilaoetnnesgd!");
           $welcome = sprintf("%s", $schools[$teamNumber]);
        }
        if ($teamNumber % 2 == 0){
          // use the encrypted version
          // TODO $welcome = encode($welcome);
        }
	*****/
    $stationType = StationType::getFromTypeCode($station->get('tag'));
    trace("registration complete",__FILE__,__LINE__,__METHOD__);
    $team->updateScore($stationType, $points);
	json_sendObject(array('message' => $team->expandMessage($stationType->get('instructions'), null ) ) );
}

