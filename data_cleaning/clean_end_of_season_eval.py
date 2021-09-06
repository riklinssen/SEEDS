import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import glob
from datetime import datetime


# hardcoded dicts and boilerplate to get FFS ids. 


idcols_map = {}
idcols_map['Guatemala'] = ['What is the village  and the FFS name in Santa Eulalia?',
                           'What is the village and the FFS name in Todos Santos Cuchumatán?',
                           'What is the village and the FFS name in Concepción Huista?',
                           'What is the village and the FFS name in Chiantla?',
                           'What is the village and the FFS name in Petatán?',
                           'FFS Name', 
                           'What is the FFS name']
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
                        'What_is_the_village_and_FFS_name', 
                        'ffs_oth', 
                        'What is the FFS name?', 'What is the village and FFS name?', 'Village and FFS name', 'Village and FFS name.1', 'Village and FFS name.2', 'Village and FFS name.3', 'Village and FFS name.4', 'Village and FFS name.5', 'Village and FFS name.6', 'Village and FFS name.7', 'Villlage and FFS name', 'Villlage and FFS name.1', 'Village and FFS name.8', 'Village and FFS name.9', 'Village and FFS name.10', 'Village and FFS name.11', 'Village and FFS name.12', 'Village and FFS name.13']

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
                        'vil_ofua_ofua', 'FFS_Name_001', 'What is the FFS name?', 'What is the FFS name?', 'FFS name and village', 'FFS name and village.1', 'FFS name and village.2', 'FFS name and village.3', 'FFS name and village.4', 'FFS name and village.5', 'FFS name and village.6', 'FFS name and village.7', 'FFS name and village.8', 'FFS name and village.9', 'FFS name and village.10', 'FFS name and village.11', 'FFS name and village.12', 'FFS name and village.13', 'FFS name and village.14', 'FFS name and village.15', 'FFS name and village.16', 'FFS name and village.17', 'FFS name and village.18', 'FFS name and village.19', 'FFS name and village.20', 'FFS name and village.21', 'FFS name and village.22', 'FFS name and village.23', 'FFS name and village.24', 'FFS name and village.25', 'FFS name and village.26', 'FFS name and village.27', 'FFS name and village.28']
                        


idcols_map['Zimbabwe'] = ['ffs_oth', 'ffs_17t', 'ffs_13t', 'ffs_8m', 'ffs_3m', 'ffs_9m', 'ffs_11m', 'ffs_15u', 'ffs_16u', 'ffs_6u', 'ffs_17u',
                          'ffs_18u', 'ffs_3u', 'ffs_5u', 'ffs_9u', 'ffs_8u', 'ffs_3c', 'ffs_4c', 'ffs_5c', 'ffs_10r', 'ffs_12r', 'ffs_16r', 'ffs_17r', 'ffs_11r', 'FFS_Name_001', 'What is the FFS name?', 'You indicated you are in ward 17: What is the FFs name?', 'You indicated you are in ward 13: What is the FFs name?', 'You indicated you are in ward 8: What is the FFS name?', 'You indicated you are in ward 3: What is the FFs name?', 'You indicated you are in ward 9: What is the FFs name?', 'You indicated you are in ward 11: What is the FFs name?', 'You indicated you are in ward 15 : What is the FFs name?', 'You indicated you are in ward 16 : What is the FFs name?', 'You indicated you are in ward 6 : What is the FFs name?', 'You indicated you are in ward 17 : What is the FFs name?', 'You indicated you are in ward 18 : What is the FFs name?', 'You indicated you are in ward 3 : What is the FFs name?', 'You indicated you are in ward 5: What is the FFs name?', 'You indicated you are in ward 9: What is the FFs name?.1', 'You indicated you are in ward 8: What is the FFs name?', 'You indicated you are in ward 3: What is the FFs name?.1', 'You indicated you are in ward 4: What is the FFs name?', 'You indicated you are in ward 5: What is the FFs name?.1', 'You indicated you are in ward 10: What is the FFs name?', 'You indicated you are in ward 12: What is the FFs name?', 'You indicated you are in ward 16: What is the FFs name?', 'You indicated you are in ward 17: What is the FFs name?.1', 'You indicated you are in ward 11: What is the FFs name?.1']
# in guatemala I get values instead of FFS names
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


#make a list of cols to determine admin level 1 in each file. 
#sometimes village and FFS was asked in a single questions, admin_1 is the lowest geographical/adminstrative level we can determine. 
admin_1_map={}
admin_1_map['Guatemala']=['What is the municipality?', 'What is the municipality?.1']
admin_1_map['Laos']=['What is the district?', 'What is the district?.1', 'What is the district?.2', 'What is the district?.3', 'What is the district?.4', 'What is the district?.5', 'What is the district?.6']
admin_1_map['Peru']=['not in data yet distrito'] # Peru is not included in the end of season eval, yet (19 Aug 2021) -->     
# code snippet below used for peru. 
#if country == 'Peru':
        #df['admin_1'] = df.loc[:, [d for d in df.columns if 'distrito' in d]
        #                           ].stack().groupby(level=0).first().reindex(df.index)

admin_1_map['Uganda']=['What is the district?', 'What is the district?.1, district_oth',	'district','distr_oth']
admin_1_map['Zambia']=['distr_oth', 'district', 'district_s','district_lu', 'district_c', 'What is the district?.1', 'What is the district?', 'What is the district in Southern province?', 'What is the district in Lusaka province?', 'What is the district in Central province?']
admin_1_map['Zimbabwe']=['What is the district?', 'What is the district?.1']
admin_1_map['Nepal']=['What is the district?','What is the district?.1']
#add a mapper to see what level 1 actually means (e.g. municipality, dictrict province etc. ) 
admin_1_type={}
admin_1_type['Guatemala']='Municipality'
admin_1_type['Laos']='District'
admin_1_type['Peru']='Distrito'
admin_1_type['Uganda']='District'
admin_1_type['Zambia']='District'
admin_1_type['Zimbabwe']='District'
admin_1_type['Nepal']='District'


def get_latest_entry_by_FFS_ID_sort_by_timestamp(df,timestamp_column='_submission_time'):
    """extracts latest entry (usually by _submission_id), generaltes col with most recent entry

    Parameters
    ----------
    df : input dataframe
        
    timestamp_column : list
        dataframe column with

    Returns
    -------
    dataframe
        dataframe sorted by ID_FFS_ID and timestamp, adds column with boolean for latest entry
    """    
    if np.issubdtype(df[timestamp_column].dtype, np.datetime64)==False: 
        df[timestamp_column]=pd.to_datetime(df[timestamp_column], infer_datetime_format=True)
    df['timerank']=df.groupby(['ID_FFS_ID'],sort=True)[timestamp_column].transform('rank', ascending=False)
    df.sort_values(by=['ID_FFS_ID', timestamp_column], ascending=[True, False], inplace=True)
    df['latest_entry']=np.where(df['timerank']==1,True, False)
    df.drop(['timerank'], axis=1, inplace=True)
    return df


##FILENAMES & PAHTS 
input_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\End_of_season")

clean_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\End_of_season")

#create clean data path if it doesnt exist. 
if not os.path.exists(clean_data_path):
    os.mkdir(clean_data_path)
    print("Directory " , clean_data_path,  " Created ")
othercols={}
# load in csv's
#dicts for concating all countries subforms dfs
dissemination_all={}
functioning_all={}
files = [c for c in os.listdir(input_data_path) if c.endswith('csv')]
for file in files: 
    df=pd.read_csv(input_data_path/file)
    #exclude empty dfs
    if df.empty:
        print(file, "is empty, no data here, yet")
        continue
    
    #make country indicator (from df)
    cntrycol_idx=df.columns.get_loc("country")
    country=df.iat[0,cntrycol_idx]
    #generate unique ids. 
    idcols=[c for c in idcols_map[country] if c in  df.columns] 
    #make FFS id: stack idcols and take first nonmissing value in stacked idcols, then reindex towards existing df. 
    # in guatamala numbers are parsed instead of ffs names.
    if country == 'Guatemala':
        colstomap = [c for c in guat_ffs_map.keys() if c in df.columns]
        for c in colstomap:
            df[c] = df[c].replace(guat_ffs_map[c])
          
    df['ID_FFS_ID'] = df.loc[:, idcols].stack().groupby(level=0).first().reindex(df.index)
    
    # add location info. using admin_1_map
    #same trick as ID_FFS_ID 
    #make temp list of idcols
    admin1cols=[c for c in admin_1_map[country] if c in df.columns]
    
    df['admin_1']=df.loc[:, admin1cols].stack().groupby(level=0).first().reindex(df.index)
    #make an admin_1_type designation to see what admin level this is actually about 
    df['admin_1_type']=admin_1_type[country]
    #move ID cols to front of df
    df = df[ ['ID_FFS_ID', '_submission_time','admin_1', 'admin_1_type'] + [ col for col in df.columns if col not in ['ID_FFS_ID', 'admin_1', 'admin_1_type', '_submission_time'] ] ].drop ('Unnamed: 0', axis=1)

     
 
    #split subforms functioning and dissemination sort and export
    #create df where all countries are combined
    #functioning FFS 
    functioning_filename =None
    dissemination_filename=None
    #sometimes the subform indicator = PVS- Select stage of documentation
    print(country)
    if 'PVS- Select stage of documentation' in df.columns: 
        df.drop('PVS- Select stage of documentation', axis=1)
    if 'Select stage of documentation' in df.columns: 
        df.drop('Select stage of documentation', axis=1)

    
    functioning=df.loc[df['Select the form'].isin(['Functioninig of the FFS','Dissemination of selected FFS varieties'])].dropna(how='all', axis=1)
    if functioning.empty:
        print(country, 'FFS functioning subset is empty')
    else: 
        #sort and flag latest entry
        get_latest_entry_by_FFS_ID_sort_by_timestamp(functioning)
        functioning_filename=country+ '-End of Season Eval-FFS_functioning_dissemination.csv'
        functioning.to_csv(clean_data_path/functioning_filename)
        #add an indicator with the filename for easy retreval later
        functioning['sourcefile']=functioning_filename
        #add to full set, exclude idcols (this will only be confusing in the concatenation)
        functioning_all[country]=functioning

#concat all forms
#inner join to keep equivalent cols only drop level 1 rangeindex (is confusing)
functioning_all_df=(
    pd.concat(functioning_all, axis=0)
    .reset_index(drop=[True])
    .drop(['What is the province?.1', 
'What is the district?.1', 
'What is the district?.3', 
'What is the district?.4', 
'PVS- Select stage of documentation', 
'Do you want to enter a new FFS?', 
'What is the district?', 
'What is the subcounty in Soroti district?', 
'what is the parish in Asuret subcounty?', 
'What is the parish in Katine subcounty?', 
'What is the subcounty in Nebbi district?', 
'what is the parish in Erussi subcounty?', 
'What is the subcounty in Omoro district?', 
'what is the parish in Lalogi subcounty?', 
'What is the parish in Odek subcounty?', 
'What is the subcounty in Amuria district?', 
'What is the parish in  Akeriau subcounty?', 
'Select stage of documentation', 
'If other, please specify', 
'What is the subcounty?', 
'What is the parish?', 
'What is the village?', 
'_validation_status',                                             
'username', 
'What is the province?', 
'What is the camp?.1', 
'What is the district in Central province?',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
'What is the camp in Shibyunji?', 
'What is the ward in Mudzi?', 
'What is the ward in Chiredzi?', 
'__version__', 
'What is the ward?',
'FFS name and village', 
'FFS name and village.1', 
'FFS name and village.2',                                                                                                                       
'FFS name and village.3', 
'FFS name and village.5', 
'FFS name and village.6', 
'FFS name and village.8', 
'FFS name and village.11', 
'FFS name and village.12',                                                                                
'FFS name and village.13', 
'FFS name and village.14', 
'FFS name and village.15', 
'Village and FFS name.9', 
'Village and FFS name.10',                                                                                                                                         
'You indicated you are in ward 9: What is the FFs name?', 
'You indicated you are in ward 11: What is the FFs name?', 
'You indicated you are in ward 5: What is the FFs name?.1'], axis=1).to_csv(clean_data_path/'ALL-End of Season Eval-FFS_functioning.csv', index=False)
)                                         


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

