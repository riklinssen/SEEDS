
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import glob
from datetime import datetime
import re
from itertools import compress

#cleaning diversity wheel excercise forms.


##Utils
def remove_multiple_strings(cur_string, replace_list):
  for cur_word in replace_list:
    cur_string = cur_string.replace(cur_word, '')
  return cur_string



def get_latest_entry_by_FFS_ID_sort_by_timestamp(df, timestamp_column='_submission_time'):
    """extracts latest entry (usually by _submission_id), generaltes col with most recent entry

    Parameters
    ----------
    df : input dataframe
        
    timestamp_column : list
        dataframe column with timestamp

    Returns
    -------
    dataframe
        dataframe sorted by ID_FFS_ID and timestamp, adds column with boolean for latest entry
    """
    if np.issubdtype(df[timestamp_column].dtype, np.datetime64) == False:
        df[timestamp_column] = pd.to_datetime(
            df[timestamp_column], infer_datetime_format=True)
    df['timerank'] = df.groupby(['ID_FFS_ID'], sort=True)[
        timestamp_column].transform('rank', ascending=False)
    df.sort_values(by=['ID_FFS_ID', timestamp_column],
                   ascending=[True, False], inplace=True)
    df['latest_entry'] = np.where(df['timerank'] == 1, True, False)
    df.drop(['timerank'], axis=1, inplace=True)
    return df


#####FILENAMES & PATHS
input_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PPB\Diversity_wheel_excercise_for_crops")

clean_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PPB\Diversity wheel exercise for crops")

#create clean data path if it doesnt exist.
if not os.path.exists(clean_data_path):
    os.mkdir(clean_data_path)
    print("Directory ", clean_data_path,  " Created ")

quadrants = ['many_large', 'many_small', 'few_large', 'few_small', 'disappear']

crop_divwheel_cols_by_quadrants = dict.fromkeys(quadrants)
crop_divwheel_cols_by_quadrants['many_large'] = {
    'List the crops grown by MANY farmers on LARGE plots?': 'many_large', 'Name_the_crops_grown_rmers_on_LARGE_plots':  'many_large'}
crop_divwheel_cols_by_quadrants['many_small'] = {
    'List the crops grown by MANY farmers on SMALL plots?': 'many_small', 'Name_the_crops_grown_rmers_on_SMALL_plots': 'many_small'}
# for zimbabwe there are no observation for few_large for the standard set of crops (only others)
crop_divwheel_cols_by_quadrants['few_large'] = {
    'List the crops grown by FEW farmers on LARGE plots?': 'few_large', 'Name_the_crops_grown_rmers_on_LARGE_plots_001': 'few_large'}
# for zimbabwe Name_the_crops_grown_rmers_on_SMALL_plots_001 is a substring of Name_the_crops_grown_rmers_on_SMALL_plots so this gets replaced in the initial run
crop_divwheel_cols_by_quadrants['few_small'] = {'List the crops grown by FEW farmers on SMALL plots?': 'few_small',
                                                'Name_the_crops_grown_rmers_on_SMALL_plots_001': 'few_small', 'many_small_001': 'few_small'}
crop_divwheel_cols_by_quadrants['disappear'] = {
    'List the crops that have disappeared from your community': 'disappear', 'Name_the_crops_that_have_disap': 'disappear'}

##for zimbabwe 001 stuff is again a substring of many_small? Da fuq?



#initialize a dict for the diversity wheel all file 
diversity_wheel_all={}

files = [c for c in os.listdir(input_data_path) if c.endswith('csv')]
for file in files:
    df = pd.read_csv(input_data_path/file)
    #continue loop if df is empty
    if df.empty:
        print(file, "is empty, no data here, yet")
        continue
    #make country indicator (from df)
    cntrycol_idx = df.columns.get_loc("country")
    country = df.iat[0, cntrycol_idx]
    #find latest entry
    get_latest_entry_by_FFS_ID_sort_by_timestamp(df)
    #admin_1 & admin_1_type cleanup,
    #remove info between brackets
    df['admin_1']=df['admin_1'].str.replace(r"\(.*\)","", regex=True)

    if country =='Guatemala': 
        df['admin_1_type'] = 'Municipality'
    else: 
        df['admin_1_type'] = 'District'
    #make sure columnnames are consistent rename cols by quadrant
    for quadrant in quadrants:
        for old, new in crop_divwheel_cols_by_quadrants[quadrant].items():
            df.columns = df.columns.str.replace(old, new, regex=False)
        #make a quadrant identifier that is constant (it does not hold a list of crops)
        df[quadrant] = str(quadrant)
    #melt the df
    #create a list of idvars
    #idvars=['ID_FFS_ID'] + quadrants
    #create a list of value vars, these should startwith quadrant names have a slash in the name and exclude all other stuff
    value_vars = [colname for colname in df.columns for startstr in quadrants if colname.startswith(
        startstr) and '/' in colname and 'oth' not in colname]
    idvars = ['ID_FFS_ID', 'admin_1', 'admin_1_type', '_submission_time',
              'subform', 'timing',	'latest_entry', 'country']
    melted_df = pd.melt(df, id_vars=idvars, value_vars=value_vars,
                        var_name='quandrant_crop', value_name='isthere')
    #select only the crops mentioned
    isthere = melted_df.loc[melted_df['isthere'] == 1]
    #seperate quadrant and cropname, split by forward slash
    quadrant_cropname = (isthere['quandrant_crop'].str.split('/', expand=True)
        .rename({0: 'quadrant', 1: 'cropname'}, axis=1))
    diversity_wheel = (pd.concat([isthere, quadrant_cropname], axis=1)
                       .drop(['quandrant_crop', 'isthere'], axis=1)
                       .set_index('ID_FFS_ID')
                       .sort_index()
                       .sort_values(by=['_submission_time'],ascending=False))
        
    diversity_wheel.to_csv(
        clean_data_path/str(country + ' Diversity wheel exercise for crops.csv'))
    #append to all diversity wheel dicts. 
    diversity_wheel_all[country]=diversity_wheel
    
    
    


#concatenate a set for all diveristy wheels
all_diversity_wheels=pd.concat(diversity_wheel_all, ignore_index=True)

all_diversity_wheels.to_csv(
        clean_data_path/str('ALL' + ' Diversity wheel exercise for crops.csv'))



# ########################################SNIPPETS & OTHER CRAP BELOW#########TO CLEANUP


# # #other colnames for crop diversity wheel excercise in uganda, zambia and zimbabwe. Uganda and amd zambia first, this seems to be consistent.
# # crop_divwheel_colnames_dict={'List the crops grown by MANY farmers on LARGE plots?': 'many_large',
# # 'List the crops grown by MANY farmers on SMALL plots?': 'many_small',
# # 'List the crops grown by FEW farmers on LARGE plots?':'few_large',
# # 'List the crops grown by FEW farmers on SMALL plots?':'few_small',
# # 'List the crops that have disappeared from your community': 'disappear',
# # 'If other, specify.1': 'many_large_oth', ##making other specify1 etc more meaningful
# # 'If other, specify.2':'many_small_oth',
# # 'If other, specify.3': 'few_large_other',
# # 'If other, specify.4': 'few_small_other',
# # 'If other, specify.5': 'disappear_oth',
# # 'Name_the_crops_grown_rmers_on_LARGE_plots':  'many_large', #this is for zimbabwe which is even more different, what a shitshow.
# # #many large other specify is not filled so no text variable. Indicator var for zimbabwe is Name_the_crops_grown_rmers_on_LARGE_plots/others__specif
# # #'Name_the_crops_grown_rmers_on_LARGE_plots_001': 'many_large_oth'
# # 'Name_the_crops_grown_rmers_on_SMALL_plots': 'many_small',
# # 'If_other_specify_001': 'many_small_oth',
# # 'Name_the_crops_grown_rmers_on_LARGE_plots_001': 'few_large',
# # 'If_other_specify_002': 'few_large_other',
# # 'Name_the_crops_grown_rmers_on_SMALL_plots_001':'few_small',
# # 'If_other_specify_003': 'few_small_other',
# # 'Name_the_crops_that_have_disap': 'disappear',
# # 'If_other_specify_004': 'disappear_oth'}
# #sort out what to do with this later
# #'DWC_male': 'Number of MALE members present during this session.1',
# #'DWC_female': 'Number of FEMALE members present during this this session.1',



# ##someting wrong with zimbabwe.
# zim = pd.read_csv(
#     r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PPB\Diversity_wheel_excercise_for_crops\Diversity_wheel_exercise_for_crops_Zimbabwe_RAW.csv")
# ###SNIPPETS & CRAP BELOW
# #see if this works in analyses.

# test = diversity_wheel.groupby(
#     'quadrant')['cropname'].value_counts(normalize=True)
# idvars = ['ID_FFS_ID'] + quadrants

# startswith = list(set(crop_divwheel_colnames_map.values()))
# alldivcols = [
#     colname for colname in df.columns for startstr in startswith if colname.startswith(startstr)]


# test_div = df.loc[:, alldivcols]
# test_div['ID_FFS_ID'] = df['ID_FFS_ID']
# #make an indicator for location in wheel
# #test_div['crop_divwheel_many_large']='crop_divwheel_many_large'
# selection = test_div.loc[:, [c for c in test_div.columns if 'crop_divwheel_many_large' in c or 'ID_FFS_ID' in c]].drop(
#     'crop_divwheel_many_large', axis=1)

# #try to replace the 0/1 with the string after the slash.

# variables = [
#     c for c in selection.columns if 'crop_divwheel_many_large' in c and '/' in c]
# replacestr = [c.split('/')[1] for c in variables if '/' in c]
# toreplace = dict(zip(variables, replacestr))
# for var in toreplace.keys():
#     selection[var] = np.where(selection[var] == 1, toreplace[var], np.nan)
# selection.head()
# test_melt = pd.melt(selection, id_vars=[
#                     'ID_FFS_ID'], var_name='crop_divwheel_many_large', value_vars=toreplace.keys())

# test_div_2 = df.loc[:, ['crop_divwheel_many_large/rice',
#                         'crop_divwheel_many_large/wheat',
#                         'crop_divwheel_many_large/maize',
#                         'crop_divwheel_many_large/groundnut',
#                         'crop_divwheel_many_large/pearl_millet',
#                         'crop_divwheel_many_large/sorghum',
#                         'crop_divwheel_many_large/potato',
#                         'crop_divwheel_many_large/bambara_nut',
#                         'crop_divwheel_many_large/radish',
#                         'crop_divwheel_many_large/lentil',
#                         'crop_divwheel_many_large/common_bean',
#                         'crop_divwheel_many_large/soybean', 'ID_FFS_ID']]
# test_div_2['wheelloc'] = 'many_large'
# test_melt = pd.melt(test_div_2, id_vars=['ID_FFS_ID', 'wheelloc'], value_vars=['crop_divwheel_many_large/rice',
#                                                                                'crop_divwheel_many_large/wheat',
#                                                                                'crop_divwheel_many_large/maize',
#                                                                                'crop_divwheel_many_large/groundnut',
#                                                                                'crop_divwheel_many_large/pearl_millet',
#                                                                                'crop_divwheel_many_large/sorghum',
#                                                                                'crop_divwheel_many_large/potato',
#                                                                                'crop_divwheel_many_large/bambara_nut',
#                                                                                'crop_divwheel_many_large/radish',
#                                                                                'crop_divwheel_many_large/lentil',
#                                                                                'crop_divwheel_many_large/common_bean',
#                                                                                'crop_divwheel_many_large/soybean'], var_name='crop', value_name='isthere')

# result = test_melt.loc[test_melt['isthere'] == 1]
# melted_df = pd.melt()
# quadrant_cropname = result['crop'].str.split(
#     '/', expand=True).rename({0: 'quadrant', 1: 'cropname'}, axis=1)
# pd.concat([result, quadrant_cropname], axis=1)
# result['cropname'] = result['crop'].apply(lambda x: x.split('/')[1])
# result[['quadrant', 'crop']] = result['crop'].str.split(pat='/', expand=True)

# #try and
# #generate a list of unique values (startswith) to iterate over
# #startswith = list(set(crop_divwheel_colnames_map.values()))
# #select columnnames
# #alldivcols=[ colname for colname in df.columns for startstr in startswith if colname.startswith(startstr)]
# #export to csv
