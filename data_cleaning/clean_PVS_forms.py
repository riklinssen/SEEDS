
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import glob
from datetime import datetime
import re



def remove_multiple_strings(cur_string, replace_list):
  for cur_word in replace_list:
    cur_string = cur_string.replace(cur_word, '')
  return cur_string




# hardcode a dict of relevent FFS ids.

idcols_map = {}
idcols_map['Guatemala'] = ['What is the village  and the FFS name in Santa Eulalia?',
                           'What is the village and the FFS name in Todos Santos Cuchumatán?',
                           'What is the village and the FFS name in Concepción Huista?',
                           'What is the village and the FFS name in Chiantla?',
                           'What is the village and the FFS name in Petatán?',
                           'FFS Name', 
                           'What is the FFS name?']
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
                        'What_is_the_village_and_FFS_name', 'ffs_oth', 
                        'What is the FFS name?', 
                        'What is the village and FFS name?', 'Village and FFS name',
                        'Village and FFS name.1',
                        'Village and FFS name.2',
                        'Village and FFS name.3',
                        'Village and FFS name.4',
                        'Village and FFS name.5',
                        'Village and FFS name.6',
                        'Village and FFS name.7',]

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
                        'vil_ofua_ofua', 'FFS_Name_001'
                        'What is the FFS name?', 'What is the FFS name?.1', 'FFS name and village', 'FFS name and village.1', 'FFS name and village.2', 'FFS name and village.3', 'FFS name and village.4', 'FFS name and village.5', 'FFS name and village.6', 'FFS name and village.7', 'FFS name and village.8', 'FFS name and village.9', 'FFS name and village.10', 'FFS name and village.11', 'FFS name and village.12', 'FFS name and village.13', 'FFS name and village.14', 'FFS name and village.15', 'FFS name and village.16', 'FFS name and village.17', 'FFS name and village.18', 'FFS name and village.19', 'FFS name and village.20', 'FFS name and village.21', 'FFS name and village.22', 'FFS name and village.23', 'FFS name and village.24', 'FFS name and village.25', 'FFS name and village.26', 'FFS name and village.27', 'FFS name and village.28', ]

idcols_map['Zimbabwe'] = ['ffs_oth','ffs_17t', 'ffs_13t', 'ffs_8m', 'ffs_3m', 'ffs_9m', 'ffs_11m', 'ffs_15u', 'ffs_16u', 'ffs_6u', 'ffs_17u',
                          'ffs_18u', 'ffs_3u', 'ffs_5u', 'ffs_9u', 'ffs_8u', 'ffs_3c', 'ffs_4c', 'ffs_5c', 'ffs_10r', 'ffs_12r', 'ffs_16r', 'ffs_17r', 'ffs_11r', 'FFS_Name_001', 'What is the FFS name?',
                          'You indicated you are in ward 10: What is the FFs name?',
                          'You indicated you are in ward 11: What is the FFs name?',
                          'You indicated you are in ward 11: What is the FFs name?.1',
                          'You indicated you are in ward 12: What is the FFs name?',
                          'You indicated you are in ward 13: What is the FFs name?',
                          'You indicated you are in ward 15 : What is the FFs name?',
                          'You indicated you are in ward 16 : What is the FFs name?',
                          'You indicated you are in ward 16: What is the FFs name?',
                          'You indicated you are in ward 17 : What is the FFs name?',
                          'You indicated you are in ward 17: What is the FFs name?',
                          'You indicated you are in ward 17: What is the FFs name?.1',
                          'You indicated you are in ward 18 : What is the FFs name?',
                          'You indicated you are in ward 3 : What is the FFs name?',
                          'You indicated you are in ward 3: What is the FFs name?',
                          'You indicated you are in ward 3: What is the FFs name?.1',
                          'You indicated you are in ward 4: What is the FFs name?',
                          'You indicated you are in ward 5: What is the FFs name?',
                          'You indicated you are in ward 5: What is the FFs name?.1',
                          'You indicated you are in ward 6 : What is the FFs name?',
                          'You indicated you are in ward 8: What is the FFS name?',
                          'You indicated you are in ward 8: What is the FFs name?',
                          'You indicated you are in ward 9: What is the FFs name?',
                          'You indicated you are in ward 9: What is the FFs name?.1']


# load in csv's
input_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PVS")
clean_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PVS")
#seems like AESA and pre and post harvest have different ID cols. 
allfiles = [c for c in os.listdir(input_data_path) if c.endswith('csv')]
aesa=[f for f in allfiles if 'AESA' in f]
notaesa=[f for f in allfiles if f not in aesa]

countries=[]
forms=[]
observations=[]
missingids=[]
datafiles=[]
downloaded_ats=[]
latest_uploads=[]
for datafile in allfiles:
    data = pd.read_csv(input_data_path/datafile)
    country=datafile.split('-')[0].strip()
    #filter out empty dfs. 
    nrobs=len(data['country'])
    if nrobs>0:        
        isempty=False
    if nrobs==0:
        isempty=True
        toreplacelist=[country, '- SDHS ',  'project', '.csv', '-PVS', '- SDHS', 'Project', 'SD=HS'  ]
        form=remove_multiple_strings(datafile, toreplacelist)
        countries.append(country)
        forms.append(form)
        observations.append(0)
        missingids.append(np.nan)
        datafiles.append(datafile)
        downloaded_ats.append(pd.Timestamp.today())
        latest_uploads.append(np.nan)

    if isempty: 
        continue

    if not isempty:
      #add form indicator  
     #in some datasets the form name col is named differently. 
        data.rename(columns={'PVS- Select stage of data collection':'PVS- Select stage of documentation', 'Select stage of data collection': 'PVS- Select stage of documentation', 'PVS_forms':'PVS- Select stage of documentation'}, inplace=True)
        #drop in case there is no response on the form indicator.
        data.dropna(subset=['PVS- Select stage of documentation'], inplace=True)
        #in uganda i receive codes instead of string vals. 
        data['PVS- Select stage of documentation'].replace({'aesa_stg3_1': 'AESA (EARLY VEGETATIVE_EMERGENCE STAGE)',
                                                            'AESA (EARLY VEGETATIVE/EMERGENCE STAGE)': 'AESA (EARLY VEGETATIVE_EMERGENCE STAGE)',
                                                            'aesa_stg3_2': 'AESA (LATE VEGETATIVE STAGE)',
                                                            'aesa_stg3_3': 'AESA (FLOWERING STAGE)',
                                                            'aesa_stg3_4':	'AESA (MATURITY STAGE)', 
                                                            'AESA for FLOWERING STAGE': 'AESA (FLOWERING STAGE)',
                                                            'PRE-SEASON DOCUMENTATION': 'PRE_SEASON DOCUMENTATION', 
                                                            'POST-HARVEST EVALUATION': 'POST_HARVEST EVALUATION'}, inplace=True)
         

        #add unique FFS id
        # AESA forms have the same idcols as previously used for the PPB forms so we can use idcols_map.
        ####AESA forms
         #generate unique ids. 
        try: 
            data['ID_FFS_ID'] = data.loc[:, idcols_map[country]].stack().groupby(level=0).first().reindex(data.index)
        except KeyError:
            #the list of idcols might be longer so it throws an error now once there are missing col indices references.
            idcols=[c for c in idcols_map[country] if c in  data.columns] 
            data['ID_FFS_ID'] = data.loc[:, idcols].stack().groupby(level=0).first().reindex(data.index)
        if datafile in aesa:
            # Create target Directory if don't exist

            dirName=Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PVS\AESA")
            if not os.path.exists(dirName):
                os.mkdir(dirName)
                print("Directory " , dirName ,  " Created ")
            
           
            #make form indicator
            form=data['PVS- Select stage of documentation'].unique()[0]                        
            #extract formname (re to extract all between brackets)
            formname= str('PVS_AESA_'+ country +'_' + re.search(r'\((.*?)\)',form).group(1) + '.csv').replace(" ", "_")
            #clean 
            
            data.to_csv(Path(dirName/formname))
        if datafile not in aesa: 
            dirName=Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PVS")
            if not os.path.exists(dirName):
                os.mkdir(dirName)
                print("Directory " , dirName ,  " Created ")
            form=data['PVS- Select stage of documentation'].unique()[0]                        
            #extract formname (re to extract all between brackets)
            formname= str('PVS_'+ country +'_' + form + '.csv').replace(" ", "_")
            data.to_csv(Path(dirName/formname))

        data['submission_time_dt']=pd.to_datetime(data['_submission_time'], infer_datetime_format=True)
        nrmissingids=data['ID_FFS_ID'].isnull().sum()
        countries.append(country)
        forms.append(form)
        observations.append(len(data))
        missingids.append(nrmissingids)
        datafiles.append(datafile)
        downloaded_ats.append(data['downloaded_at'].max())
        latest_uploads.append(data['submission_time_dt'].max())

response_overview=pd.DataFrame(zip(countries, forms, observations, missingids, datafiles, downloaded_ats, latest_uploads), columns=['country', 'form', 'observations', 'missing_FFS_ids', 'file', 'latest_data_download', 'latest_submission'])

#export response overview.         
response_overview.to_csv(Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PVS\pvs_response_overview.csv"))
    
