import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import glob
from datetime import datetime


# hardcode a dict of relevent level1 ids.

idcols_map = {}
idcols_map['Guatemala'] = ['What is the village  and the FFS name in Santa Eulalia?',
                           'What is the village and the FFS name in Todos Santos Cuchumatán?',
                           'What is the village and the FFS name in Concepción Huista?',
                           'What is the village and the FFS name in Chiantla?',
                           'What is the village and the FFS name in Petatán?',
                           'FFS Name']
idcols_map['Laos'] = ['What is the village?.1',
                      'What is the village?.2',
                      'What is the village?.3',
                      'What is the village?.4',
                      'What is the village?.5',
                      'What is the village?.6',
                      'What is the village?.7',
                      'FFS Name']

idcols_map['Nepal'] = ['What is the village and the FFS name in Jorayal Rural municipality?',
                       'What is the village and the FFS name in Ganyapdhura Rural municipality?',
                       'What is the village and the FFS name in Kailali Rural municipality?',
                       'What is the village and the FFS name in Jashpur Rural municipality?',
                       'What is the village and the FFS name in Gauriganga municipality?',
                       'What is the village and the FFS name in Lalijadi Rural municipality?',
                       'FFS Name',
                       'What is the FFS name?']


idcols_map['Peru'] = ['What is the FFS name?.1',
                      'FFS Name']
idcols_map['Zambia'] = ['vil_mab_s',
                        'vil_nad_s',
                        'Village_and_FFS_name_003',
                        'Village_and_FFS_name_004',
                        'vil_chi_ru',
                        'Village_and_FFS_name_005',
                        'vil_mp_ru',
                        'vil_ru_ru',
                        'vil_chi_ka',
                        'Villlage_and_FFS_name',
                        'vil_mam_c',
                        'Villlage_and_FFS_name_001',
                        'vil_mu_c',
                        'Village_and_FFS_name',
                        'Village_and_FFS_name_001',
                        'Village_and_FFS_name_002',
                        'What_is_the_village_and_FFS_name', 'ffs_oth']

idcols_map['Uganda'] = ['ffs_name_oth', 'ffs_name', 'ffs_oth',
                        'vil_ob_as',
                        'vil_oc_ks',
                        'vil_oj_ks',
                        'vil_ol_ks',
                        'vil_n_pac',
                        'vil_n_pad',
                        'vil_n_pay',
                        'vil_o_p',
                        'vil_o_lal',
                        'vil_o_lakp',
                        'vil_o_lakt',
                        'vil_o_od',
                        'vil_ak',
                        'vil_akay',
                        'vil_ako',
                        'vil_akt',
                        'vil_ogo_ok',
                        'vil_ogo_oc',
                        'vil_ogo_od',
                        'vil_ogongora_do',
                        'vil_ogongora_on',
                        'vil_orungo_adu',
                        'vil_orungo_ame',
                        'vil_orungo_moru',
                        'vil_orungo_omo',
                        'vil_p_cw',
                        'vil_p_bo',
                        'vil_p_fuda',
                        'vil_ofua_ofua', 'FFS_Name_001']

idcols_map['Zimbabwe'] = ['ffs_oth', 'ffs_17t', 'ffs_13t', 'ffs_8m', 'ffs_3m', 'ffs_9m', 'ffs_11m', 'ffs_15u', 'ffs_16u', 'ffs_6u', 'ffs_17u',
                          'ffs_18u', 'ffs_3u', 'ffs_5u', 'ffs_9u', 'ffs_8u', 'ffs_3c', 'ffs_4c', 'ffs_5c', 'ffs_10r', 'ffs_12r', 'ffs_16r', 'ffs_17r', 'ffs_11r', 'FFS_Name_001']


# hardcode FFSprofile cols.
profilecols = ['ID_FFS_ID', 'admin_1',
               'Distance to major road (in kms)',
               'GPS coordinates of the FFS',
               '_GPS coordinates of the FFS_latitude',
               '_GPS coordinates of the FFS_longitude',
               '_GPS coordinates of the FFS_altitude',
               '_GPS coordinates of the FFS_precision',
               'Agro-ecological zone',
               'Year the FFS was established',
               'Number of MALE members in FFS',
               'How many of the men are considered YOUTHS',
               'Number of FEMALE members in FFS',
               'How many of the women are considered YOUTHS',
               'Swipe  to Next Screen',
               'Average Land access (in hectares)',
               'Percentage (%) of households in the community that have access to DRAUGHT POWER',
               'Percentage (%) of households in the community that have access to IRRIGATION',
               'Percentage (%) of household in the community that have access to MANURE',
               'Percentage (%) of household in the community that have access to EXTERNAL LABOUR',
               'Percentage (%) of household in the community that have access to CHEMICAL FERTILIZER',
               'Percentage (%) of household in the community that have access to CHEMICAL PESTICIDE',
               'Percentage (%) of household in the community that have access to MICROCREDIT',
               '_id', '_uuid', '_submission_time']
# uganda is different.
profilecols_map = {"FFS_Name_001"	:	"FFS Name",
                   "Distance_to_major_road_in_kms"	:	"Distance to major road (in kms)",
                   "GPS_coordinates_of_the_FFS"	:	"GPS coordinates of the FFS",
                   "_GPS_coordinates_of_the_FFS_latitude"	:	"_GPS coordinates of the FFS_latitude",
                   "_GPS_coordinates_of_the_FFS_longitude"	:	"_GPS coordinates of the FFS_longitude",
                   "_GPS_coordinates_of_the_FFS_altitude"	:	"_GPS coordinates of the FFS_altitude",
                   "_GPS_coordinates_of_the_FFS_precision"	:	"_GPS coordinates of the FFS_precision",
                   "Agro_ecological_zone"	:	"Agro-ecological zone",
                   "Year_the_FFS_was_established"	:	"Year the FFS was established",
                   "Number_of_MALE_member_in_FFS"	:	"Number of MALE members in FFS",
                   "Number_of_YouthMALE"	:	"How many of the men are considered YOUTHS",
                   "Number_of_FEMALE_member_in_FFS"	:	"Number of FEMALE members in FFS",
                   "Number_of_YOUTHFEMALE"	:	"How many of the women are considered YOUTHS",
                   "Swipe_to_Next_Screen"	:	"Swipe  to Next Screen",
                   "Average_Land_access"	:	"Average Land access (in hectares)",
                   "What_percentage_of_ess_to_DRAUGHT_POWER"	:	"Percentage (%) of households in the community that have access to DRAUGHT POWER",
                   "Percentage_of_households_in_"	:	"Percentage (%) of households in the community that have access to IRRIGATION",
                   "What_percentage_of_ave_access_to_MANURE"	:	"Percentage (%) of household in the community that have access to MANURE",
                   "What_percentage_of_ave_access_to_LABOUR"	:	"Percentage (%) of household in the community that have access to EXTERNAL LABOUR",
                   "What_percentage_of_CHEMICAL_FERTILIZER"	:	"Percentage (%) of household in the community that have access to CHEMICAL FERTILIZER",
                   "What_percentage_of_o_CHEMICAL_PESTICIDE"	:	"Percentage (%) of household in the community that have access to CHEMICAL PESTICIDE",
                   "What_percentage_of_ccess_to_MICROCREDIT"	:	"Percentage (%) of household in the community that have access to MICROCREDIT"}


guat_ffs_map = {'What is the village  and the FFS name in Santa Eulalia?': {	'1'	:	"Moclil Grande",
                                                                             '2'	:	"Yichjoyom",
                                                                             '3'	:	"Tziquina Grande",
                                                                             '4'	:	"Nuqwuitz",
                                                                             '5'	:	"Payconop",
                                                                             '6'	:	"Txolpataq",
                                                                             '7'	:	"Temux Chiquito",
                                                                             '8'	:	"Muqanjolom"},
                'What is the village and the FFS name in Todos Santos Cuchumatán?': {'1'	:	"Chemal I"	,
                                                                                     '2'	:	"Chemal II",
                                                                                     '3'	:	"Los  Ramirez"	,
                                                                                     '4'	:	"Tuicoy",
                                                                                     '5'	:	"Chichim",
                                                                                     '6'	:	"Buena vista"	,
                                                                                     '7'	:	"Piedra Blanca"	,
                                                                                     '8'	:	"Chicoy 1",
                                                                                     '9'	:	"Tican",
                                                                                     '10'	:	"Chenihuitz"	,
                                                                                     '11'	:	"Chicoy 2",
                                                                                     '12'	:	"Chanchimil",
                                                                                     '13'	:	"Tzunul",
                                                                                     '14'	:	"Tres Cruces",
                                                                                     '15'	:	"Los Lucas",
                                                                                     '16'	: "Chemal I Altiplano Mam"},
                'What is the village and the FFS name in Concepción Huista?': {	'1' 	:	"Ajul",
                                                                                '2'	:	"Secheu",
                                                                                '3'	:	"Ap",
                                                                                '4'	:	"Yatolop",
                                                                                '5'	:	"Tzujan",
                                                                                '6'	:	"Checan",
                                                                                '7':  "Com",
                                                                                '8': "Yichoch"},
                'What is the village and the FFS name in Chiantla?'	: {	'1'	:	"Quilinco",
                                                                        '2'	:	"San José Las Flores",
                                                                        '3'	:	"El Pino",
                                                                        '4'	:	"Cantón Regadillos",
                                                                        '5'	:	"Maravillas",
                                                                        '6'	:	"Sibila",
                                                                        "san_antonio_las_nubes"	:	"San Antonio Las Nubes"	,
                                                                        '7': 	"San Antonio Las Nubes",
                                                                        '8'	: "Santo Tomas",
                                                                        '9': "Unkown FFS name in Chiantila no 9"},
                'What is the village and the FFS name in Petatán?': {'1'	:	"Trapichitos",
                                                                     "cabic"	:	"Cabic",
                                                                     '2': 	"Cabic",
                                                                     "3":	"El Sabino"}}


##FILENAMES & PAHTS 
input_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PPB")
clean_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PPB")
files = [c for c in os.listdir(input_data_path) if c.endswith('csv')]
# load in csv's


# check idcols
# initialize some dicts to concat all specific subforms later.
ffs_profiles = {}
# weekly monitoring also country or even FFS specific sort this out later.
weekly_monitoring_forms = {}
# do make response overviews.
responseoverviews = {}
diag_overviews = {}
for datafile in files:
    data = pd.read_csv(input_data_path/datafile)
    country = datafile.split('__')[0]
    # continue for Unknown countries.
    if country == 'Unknown':
        continue
    idcols = idcols_map[country]
    # in guatamala numbers are parsed instead of ffs names.
    if country == 'Guatemala':
        colstomap = [c for c in guat_ffs_map.keys() if c in data.columns]
        print(colstomap)
        for c in colstomap:
            data[c] = data[c].replace(guat_ffs_map[c])
          
    # take first nonmissing value in all village and id cols.
    data['ID_FFS_ID'] = data.loc[:, idcols_map[country]
                                 ].stack().groupby(level=0).first().reindex(data.index)
    # in Uganda & Zambia the FFS profile columns have different names  replace
    if country in ['Uganda', 'Zambia', 'Zimbabwe']:
        data.rename(columns={'Data_Collection_Forms': 'Documentation Forms', "Date_of_the_FFS_meeting": "Date of the FFS meeting",
                    "Choose_the_correct_to_continue": "Choose the correct form to continue documentation"}, inplace=True)
        # export FFS profiles.
        # different colnames in Uganda and Zambia
        data.rename(columns=profilecols_map, inplace=True)

    # documentation forms sometimes parses nrs instead of strings.
    data['Documentation Forms'].replace({
        1:	'FFS PROFILE',
        2	: 'WEEKLY MONITORING',
        3	: 'DIAGNOSTIC STAGE FORMS'}, inplace=True)
    # drop cases where documentation forms is missing.
    data.dropna(subset=['Documentation Forms'], inplace=True)
    #submission time to datetime
    data['_submission_time']=pd.to_datetime(data['_submission_time'], infer_datetime_format=True)

    print(country)
    print("len of df", len(data))
    print("nr of missing IDS", data['ID_FFS_ID'].isnull().sum())
    #in zimbabwe there are 89 records that do not have identifying information on the FFS to which this info pertains (Diagnostic stage forms) drop these. 
    if country=='Zimbabwe': 
        data.dropna(subset=['ID_FFS_ID'], inplace=True)

    # add location data.
    # in some countries there is data in old location format.
    if country == 'Guatemala':
        # get admin level 1 (in guatemala municipality)
        data['admin_1'] = data['What is the municipality?']
        data['admin_1'] = data['admin_1'] + '(municipality)'
    # in loas admin_1=district
    if country in ['Laos', 'Nepal']:
        data['admin_1'] = data.loc[:, [d for d in data.columns if 'district' in d]
                                   ].stack().groupby(level=0).first().reindex(data.index)
        data['admin_1'] = data['admin_1'] + '(district)'
    if country == 'Peru':
        data['admin_1'] = data.loc[:, [d for d in data.columns if 'distrito' in d]
                                   ].stack().groupby(level=0).first().reindex(data.index)
        data['admin_1'] = data['admin_1'] + '(district)'
    if country == 'Uganda':
        data['admin_1'] = data.loc[:, ['district_oth',	'district',
                                       'distr_oth']].stack().groupby(level=0).first().reindex(data.index) + '(district)'
    if country == 'Zambia':
        data['admin_1'] = data.loc[:, ['distr_oth', 'district', 'district_s',
                                       'district_lu', 'district_c']].stack().groupby(level=0).first().reindex(data.index) + '(district)'
    if country == 'Zimbabwe':
            data['ward'] = data.loc[:, ['M_ward','U_ward','C_ward','R_ward']].stack().groupby(level=0).first().reindex(data.index)               
            data['admin_1']=data['district'] + ' '+ data['ward'] + '(district)'
            data.drop('ward', axis=1, inplace=True)
    ##str split admin_1, path=()
    # make an overview of responses
    responseoverview=data['Documentation Forms'].value_counts(dropna=False).to_frame()
    responseoverview['latest_datachange']=data.groupby('Documentation Forms')['_submission_time'].max()
    responseoverviews[country] =responseoverview
    
    # export FFS_profiles.

    ffs_profile = data.loc[data['Documentation Forms'] == 'FFS PROFILE']
    ffs_profile = ffs_profile[profilecols]
    ffs_profile['country'] = country
    ffs_profile['timing'] = 'FFS establishment stage'

    cleanfilename = 'FFS_profile_' + country + '.csv'
    ffs_profile['filename'] = cleanfilename
    ffs_profile.to_csv(clean_data_path/cleanfilename)
    #excel output
    cleanxlsfilename='FFS_profile_' + country + '.xlsx'
    #ffs_profile.to_excel(clean_data_path/cleanxlsfilename)

    ffs_profiles[country] = ffs_profile

    # export weekly monitoring & drop empty cols
    weekly_monitoring = data.loc[data['Documentation Forms']
                                 == 'WEEKLY MONITORING']
    weekly_monitoring.drop(
        columns=[c for c in idcols if c in weekly_monitoring], inplace=True)
    if not weekly_monitoring.empty:
        weekly_monitoring = weekly_monitoring.dropna(how='all', axis=1)
        weekly_monitoring['country'] = country
        weekly_monitoring['timing'] = 'Every FFS session (optional)'

        # set datetime + indices.
        weekly_monitoring['Date'] = pd.to_datetime(
            weekly_monitoring['Date of the FFS meeting'], dayfirst=True)
        weekly_monitoring.sort_values(by=['ID_FFS_ID', 'Date'], inplace=True)
        weekly_monitoring.set_index(['ID_FFS_ID', 'Date'], inplace=True)
        weekly_filepath = Path(clean_data_path/'Weekly monitoring' /
                               str('Weekly_monitoring' + '_' + country + '.csv'))
        weekly_monitoring.to_csv(clean_data_path/weekly_filepath)

    
        

        # add to overall weekly monitoring dict.
        #weekly_monitoring_forms[country] = weekly_monitoring
        
    # diagnostic stage forms
    diagnostic_stage_form = data.loc[data['Documentation Forms']
                                     == 'DIAGNOSTIC STAGE FORMS']
    if not diagnostic_stage_form.empty:
        diagnostic_stage_form.dropna(how='all', axis=1, inplace=True)
        diagnostic_stage_form['subform'] = diagnostic_stage_form['Choose the correct form to continue documentation'].replace(
            {'timel_line_ana': 'Timeline analysis', "seed_system_analysis": 'Seed system analysis', 'diversity_wheel_exercise_for_c': 'Diversity wheel exercise for crops', 'diversity_wheel_exercise_for_v': 'Diversity wheel exercise for varieties'})
        diagnostic_stage_form.dropna(subset=['subform'], inplace=True)
        # add timing
        diagnostic_stage_form['timing'] = diagnostic_stage_form['subform'].map(
            {'Timeline analysis': 'Before the season', 'Diversity wheel exercise for crops': 'Before the season', 'Diversity wheel exercise for varieties': 'Before the season', 'Seed system analysis': 'Anytime'})
        diagnostic_stage_form['country'] = country
        # add to response overviews (diag_overviews)
        diag_overview = diagnostic_stage_form['subform'].value_counts(
            dropna=False).to_frame()
        diag_overview['latest_datachange']=diagnostic_stage_form.groupby('subform')['_submission_time'].max()
        diag_overviews[country] =diag_overview
    


        # export subforms seperately in folders for timeline analyses etc.
        for form in diagnostic_stage_form['subform'].unique():
            print(form)
            subformname = form.replace(' ', '_')
            filename = Path(clean_data_path/str(form) /
                            str(subformname + '_' + country + '.csv'))
            #save diversity wheel excercises in raw folder/ input_data_path, this needs an extra cleaning step then clean and save in clean folder afterwards. 
            
            if form=='Diversity wheel exercise for crops': 
                divwheelfilename=Path(input_data_path/"Diversity_wheel_excercise_for_crops"/str(subformname + '_' + country + '_RAW.csv'))
                divwheel=diagnostic_stage_form.loc[diagnostic_stage_form['subform'] == 'Diversity wheel exercise for crops'].dropna(
                how='all', axis=1)
                divwheel.to_csv(divwheelfilename)
            if form=='Diversity wheel exercise for varieties':
                divwheelvarfilename=Path(input_data_path/"Diversity_wheel_excercise_for_varieties"/str(subformname + '_' + country + '_RAW.csv'))
                divwheelvar=diagnostic_stage_form.loc[diagnostic_stage_form['subform'] == 'Diversity wheel exercise for varieties'].dropna(
                how='all', axis=1)
                divwheelvar.to_csv(divwheelvarfilename)
          
            else:
                diagnostic_stage_form.loc[diagnostic_stage_form['subform'] == form].dropna(
                how='all', axis=1).to_csv(clean_data_path/filename)
            
                

        # subforms always to be analysed at cntry level. (too many country specific crop*trait combi's + all others)


# concat ffs_profiles
FFS_profile_allcountrys = pd.concat(ffs_profiles.values(), ignore_index=True)
FFS_profile_allcountrys.to_csv(clean_data_path/"FFS_profile_all.csv")

# concat & export responseoverviews
documentation_forms_response = pd.concat(responseoverviews).reset_index(
).rename(columns={'level_0': 'country', 'level_1': 'formname'})
diagnostic_stage_forms_response = pd.concat(diag_overviews).reset_index(
).rename(columns={'level_0': 'country', 'level_1': 'formname'})
# export response overview PPB
pd.concat([documentation_forms_response, diagnostic_stage_forms_response]).set_index(['country']).assign(
    latest_download=pd.Timestamp.today()).to_csv(clean_data_path/"PPB_response_overview.csv")
