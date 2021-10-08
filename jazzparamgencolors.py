#
# File: jazzparamgencolors.py
#
# Author: D. Adriaansen
#
# Date: 25 April 2012
#
# Purpose: Contains the logic for determining the colormap
#
# Notes:
#_________________________________________________________

# Function for setting the colormap
def set_cmap(layername):

  coldict = {'ltg_strikes_gray.colors':['Ltg_Strikes'],
             'ltg_distance.colors':['Ltg_Distance'],
             'dist_to_obs_km.colors':['DIST_TO_CBH','DIST_TO_ZR','DIST_TO_CC','DIST_TO_ZL','DIST_TO_ZR','DIST_TO_IP','DIST_TO_RN',\
                                      'DIST_TO_SN','DIST_TO_DZ','DIST_TO_TH','DIST_2_LGHT'],
             'cloud_base_height_m.colors':['CLD_BASE_HGT','CLOUD_BASE_HGT'],
             'cloud_cover_cat.colors':['CLOUD_COVER'],
             'cbh_conf.colors':['CBH_CONF'],
             'precip_conf.colors':['PRECIP_CONF'],
             'cape_j_kg.colors':['CAPE'],
             'cin_j_kg.colors':['CIN'],
             'geopot_height_gpm.colors':['HGT','geop_ht'],
             'pressure_pa.colors':['PRES'],
             'vvel_pa_s.colors':['VVEL','vert_wind'],
             'condensate_kg_kg.colors':['CLWMR','ICMR','SNMR','GRMR','RWMR','clw','rnw','ice','snow','graupel'],
             'mixing_ratio_kg_kg.colors':['MIXR','Q','ciwc','clwc','spec_hum','SPECH'],
             'temp_K.colors':['TMP','TEMP','VPTMP','DEW_PT_TEMP','WET_BULB_TEMP','LCL_TEMP','TK','IN_CLOUD_TEMP','air_temp'],
             'model_precip_kg_m2.colors':['ACPCP1hr','ACPCP1Hr','NCPCP1hr','NCPCP1Hr','ACPCP2hr','ACPCP2Hr','NCPCP2hr','NCPCP2Hr','ACPCP3hr',\
                                          'ACPCP3Hr','NCPCP3hr','NCPCP3Hr','ACPCP','NCPCP','MODEL_PRECIP','accum_ls_prcp','accum_conv_prcp'],
             'theta_e_K.colors':['THETA_E'],
             'rh_per.colors':['RH','IN_CLOUD_RH'],
             'condensate_g_kg.colors':['ICE_COND','LIQ_COND','SLW','SUP_COOL_WTR','PRECIP_COND','SLW_COMP','TOTAL_COND'],
             'tot_wtr_path_g_m2.colors':['TOT_WATER_PATH'],
             'k_index.colors':['K_INDEX'],
             'lifted_index.colors':['LIFTED_INDEX'],
             'total_totals.colors':['TOTAL_TOTALS'],
             'pirep_interest.colors':['PIREP_INTEREST','PIREP_INTRT'],
             'shum.colors':['PIREP_WEIGHT'],
             'lcref.colors':['cref','lcref'],
             'dbz_pct.colors':['VIP>=1','VIP==1','VIP==2','VIP==3','VIP==4','VIP==5','VIP==6','DBZ_75_PCTL','DBZ_25_PCTL','R75','VIPGE1'],
             'sat_albedo.colors':['VISIBLE','NORM_ALBEDO','visible','albedo','VIS_1','VIS_2'],
             'sat_temp2.colors':['IR','SW_IR','SWIR','C08_BT','C09_BT','C10_BT','C11_BT','C13_BT','C15_BT'],
             'sat_zenith.colors':['SAT_ZENITH'],
             'sun_zenith.colors':['SUN_ZENITH'],
             'rel_azimuth.colors':['REL_AZIMUTH'],
             'sw_refl.colors':['SW_REFL'],
             'sat_ch2m4.colors':['IR2-IR4','IR2_IR4'],
             'cip_ice_sld_sev_percent.colors':['ICE','ICE_PROB','SLD','SLD_COMP','ICE_COMP','ICE_SEV','ICE_SEV_COMP','ICE_PROB_COMP',\
                                               'PROB_NIGHT_ADJU','PROB_VIS_ADJUST','ICE_SLD','ICE_SEV','SEV_TEMP_DAMP','SEV_CTT_DAMP',\
                                               'SEV_REFLECT_DAMP','SEV_VIS_DAMP','SEV_NIGHT_ADJUS'],
             'cip_sevcat.colors':['ICE_SEV_CAT'],
             'cip_cnt.colors':['CNT','CLOUD_LAYER_NUM','NLAYERS'],
             'cip_interest_maps.colors':['TEMP_MAP','THUNDER_MAP','RH_MAP','CTT_MAP','VV_MAP','SLW_MAP','PIREP_MAP','BWN_TMAP','MMAP'],
             'cip_k_level.colors':['CTL','CBL','CBK','WNHGT','CBK-2D','LAYER_TOP_K','LAYER_BASE_K','CTK-2D','WARMNOSE','BOUNDARY_LYR','PIREP_COUNT'],
             'cloud_thickness_m.colors':['CLD'],
             'zp.colors':['ZP'],
             'allsno.colors':['ALLSNO','ONLYSNO'],
             'cloud_top_height_m.colors':['CLD_TOP_HGT','CLOUD_TOP_HGT'],
             'warmnose_height_m.colors':['WARMNOSE_HGT'],
             'fip_sev_scenarios.colors':['SCENARIO'],
             'algo_ctt_sat.colors':['CTT','CTT-2D','CTT_2D'],
             'CipAlgo_prob_scenarios.colors':['PROB_SCENARIO','POT_SCENARIO'],
             'CipAlgo_sev_scenarios.colors':['SEV_SCENARIO'],
             'CipAlgo_sld_scenarios.colors':['SLD_SCENARIO'],
             'CipAlgo_warnings.colors':['WARNINGS'],
             'fip_sev_scenarios.xml':['FIP_SEV_SCENARIO'],
             'fip_surf_precip.xml':['SURF_PRECIP'],
             'sat_ice_idx.colors':['SAT_ICE_IDX'],
             'micro_g_m3.colors':['DQ'],
             'sat_refl.colors':['C04_REFL','C05_REFL','C06_REFL'],
             'topo.colors':['TOPO','topog'],
             'general_categorical_eight.xml':['ACTP'],
             'goes_16_l2_cod.colors':['COD'],
             'goes_16_l2_cps.colors':['CPS'],
             'radarkdp.xml':['MKDP','MeanKDP','sdevKDP','KDP'],
             'radarrhohv.xml':['MRHOHV','RHOHV'],
             'radardbz.xml':['MREF','MeanDBZ','MeanDBZ_MIXPHA','MeanDBZ_PLATES','sdevDBZ','TDBZ','LCREF','REFL'],
             'radarzdr.xml':['MZDR','MeanZDR_PLATES','MeanZDR_MIZPHA','MeanZDR','sdevZDR','ZDR'],
             'radia_interest.colors':['MIXPHA','PLATES','FRZDRZ'],
             'decision.colors':['DECISION','decision'],
             'tiles.colors':['TILENUM']
  }

  # Initialize the cmapname
  cmapname = 'sat_temp2.colors'

  # Handle some special cases
  if layername[:4] == 'IMAP' or layername[-4:] == '_INT' or layername[-9:] == '_interest' or layername[-4:] == '_MAP' or layername[-4:] == '_ADJ':
    cmapname = 'cip_interest_maps.colors'
  else:
    # Loop over each item in the dictionary and return the colormap for the layername requested
    for k,v in coldict.items():
      if layername in v:
        cmapname = k

  # Return the colormap
  return(cmapname)             
