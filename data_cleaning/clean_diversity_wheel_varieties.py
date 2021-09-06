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



def seperate_two_cropnames_in_cell(df, columnname, list_of_crops): 
    """seperates several cropnames from the diversity wheel mentioned in a single cell as first and 2nd mentioned 

    Parameters
    ----------
    df : DataFrame
        
    columnname : columname
        columnname which contains cropsnames to be separated
    list_of_crops:
        list of crops (substrings) to be seperated
    returns DataFrame with first and second metioned crop added to original df. 
    """ 
    #make a helper dataset indexed as original frame, cropnames are cols
    cropoccurence=pd.DataFrame(index=df.index, columns=list_of_crops)
    cropoccurence['to_be_separated']=df[columnname]
    for cropsub in list_of_crops:
        #get a column with the index of the substring for that specific crop
        cropoccurence[cropsub]=cropoccurence['to_be_separated'].apply(lambda s: str.index(s, cropsub) if cropsub in s else np.nan)
    print(cropoccurence.columns)
    # return the colname of the first mentioned crop (lowest str index in cell)
    cropoccurence['firstcrop']= cropoccurence.loc[:, list_of_crops].idxmin(axis=1)
    # return the colname of the second mentioned crop (highest str index in cell)
    cropoccurence['secondcrop']= cropoccurence.loc[:, list_of_crops].idxmax(axis=1)
    #set second crop to missing if 1stcrop equals secondcrop
    cropoccurence['secondcrop']=np.where(cropoccurence['secondcrop']==cropoccurence['firstcrop'], np.nan,cropoccurence['secondcrop'])
    # #concat dataframes 
    combined=pd.concat([df, cropoccurence[['firstcrop', 'secondcrop']]], axis=1)
    return combined

    

    



#####FILENAMES & PATHS
input_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PPB\Diversity_wheel_excercise_for_varieties")

clean_data_path = Path(
    r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PPB\Diversity wheel exercise for varieties")

cropdiversitywheel_all=pd.read_csv(Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PPB\Diversity wheel exercise for crops\ALL Diversity wheel exercise for crops.csv"))

#initalize crops_by_country_dict to have a dict with unique crops for each country.
# # retreive a list of crops by country from copdiversitywheel dataset
        # Throw all crops in a dict where country is the key.  
crops_by_country_d={K: None for K in cropdiversitywheel_all['country'].unique()}
for cntry in crops_by_country_d.keys():
    crops_by_country_d[cntry]=list(cropdiversitywheel_all.groupby('country')
    .get_group(cntry)['cropname'].unique())
        


#create clean data path if it doesnt exist.
if not os.path.exists(clean_data_path):
    os.mkdir(clean_data_path)
    print("Directory ", clean_data_path,  " Created ")

quadrants = ['many_large', 'many_small', 'few_large', 'few_small', 'disappear']


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
    if country not in crops_by_country_d.keys():
            print('Country:', country,' does not have a diversity wheel excercise, cannot retrieve list of unique crops')
            continue
    #find latest entry
    get_latest_entry_by_FFS_ID_sort_by_timestamp(df)
    #admin_1 & admin_1_type cleanup,
    #remove info between brackets
    df['admin_1']=df['admin_1'].str.replace(r"\(.*\)","", regex=True)

    if country =='Guatemala': 
        df['admin_1_type'] = 'Municipality'
    else: 
        df['admin_1_type'] = 'District'
    #separate the crops mentioned
    if country=='Guatemala' or country== 'Laos': 
        list_of_crops=[c for c in crops_by_country_d[country]]              
        df=seperate_two_cropnames_in_cell(df=df, columnname=['Select the crops (maximum two) for which you want to list the varieties'], list_of_crops=list_of_crops)
    # for other countries this is differently structured. Crop is contained in column name, seperate column for each crop and wheel location e.g. DWV_maize_ML (many-large). 
    #retrieve first and second crop mentioned, 

    #then take the whole range of columns  of DWV_rice etc, melt the df according to quadrant. 

    #then remove all cropnames from the col/variables names to get the variety name in each location in the wheel
        df.to_csv(
            clean_data_path/str(country + ' Diversity wheel exercise for varieties.csv'))    



#Guatemala & Laos
# Select the crops (maximum two) for which you want to list the varieties people select 2 crops
# then What are the most UNDESIRABLE traits for the crop selected? (list maximun 8 traits)/Storage (dormancy, sprouting).1 --> refers to 2nd crop selected. 


## Uganda, Zambia, Zimbabwe
#DWV_crops has multiple crops in one cell maize groundnut
#then traits have the cropname in the colname e.g. DWV_rice_ML	DWV_rice_MS	DWV_rice_FL	DWV_rice_FS	DWV_rice_vardisa	DWV_rice_vardisa_rea	DWV_rice_vardisa_rea/do_not_have_se


# Note no data for nepal for the diversity wheel, yet. 

dft=pd.read_csv(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\clean\PPB\Diversity wheel exercise for varieties\Uganda Diversity wheel exercise for varieties.csv")
country='Uganda'
dft=seperate_two_cropnames_in_cell(dft, 'DWV_crops', crops_by_country_d[country])

dft.firstcrop
dft.secondcrop
#using a tuple in endswith ensures that the list is filled with all occurences (any/or)
value_vars = [c for c in dft.columns if c.endswith(('ML', 'MS', 'FL', 'FS', 'vardisa'))]
idvars = ['ID_FFS_ID', 'admin_1', 'admin_1_type', '_submission_time',
              'subform', 'timing',	'latest_entry', 'country', 'firstcrop']
value_vars=[c for c in dft.columns if c.endswith(('ML', 'MS', 'FL', 'FS', 'vardisa'))]
#melt the df (cols to rows) then use dropna to drop all combinations not mentioned. 

melted_df_firstcrop = pd.melt(dft, id_vars=idvars, value_vars=value_vars,
                        var_name='quadrant_crop_var', value_name='varietystr').dropna(subset=['varietystr'])
#make quadrant indicator
melted_df_firstcrop['quadrant']=melted_df_firstcrop['quadrant_crop_var'].apply(quadrant_indicator)
# try to split and expand the variety strings (won't work all the time but  at least filter out  comma's & 'and')
pattern = '|'.join(['and', ',']) 
melted_df_firstcrop['varietystr']=melted_df_firstcrop['varietystr'].str.replace(pattern, '\n', regex=True)
#expand the variets in columns
exp_varieties=melted_df_firstcrop['varietystr'].str.split('\n', expand=True)
#rename cols
exp_varieties.columns=['variety_'+ str(c) for c in exp_varieties.columns]
for c in exp_varieties.columns: 
    melted_df_firstcrop[c]=exp_varieties[c]
divwheel_firstcrop=pd.melt(melted_df_firstcrop, id_vars=['ID_FFS_ID', 'admin_1', 'admin_1_type', '_submission_time','subform', 'timing',	'latest_entry', 'country', 'firstcrop', 'quadrant'], value_vars=[c for c in exp_varieties.columns], value_name='varietyname').dropna(subset=['varietyname']).sort_values(by=['ID_FFS_ID', '_submission_time', 'quadrant'], ascending=False).drop(['variable'], axis=1).rename(columns={'firstcrop': 'cropname'})



# add some other indicators that might be relevant. 
#  number of varietys in quadrant




varietynames['quadrant']=varietynames['quadrant_crop_var'].apply(quadrant_indicator)

#make a quadrant indicator. 

idvars = ['ID_FFS_ID', 'admin_1', 'admin_1_type', '_submission_time',
              'subform', 'timing',	'latest_entry', 'country']
value_vars=[c for c in dft.columns if c.endswith(('ML', 'MS', 'FL', 'FS', 'vardisa'))]

def melt_varietywheel_on_crop(df,idvars, cropnamecol, value_vars):
    if any([c for c in idvars not in df.columns]): 
        print(c, 'not in df')
    else:
    fullidvars=None
    fullidvars=idvars+[cropnamecol]
         
    melted_df=pd.melt(dft, id_vars=fullidvars, value_vars=value_vars,var_name='quadrant_crop_var', value_name='varietystr').dropna(subset=['varietystr'])
    return melted_df

test=melt_varietywheel_on_crop(dft, cropnamecol='firstcrop', idvars=idvars, value_vars=value_vars)


def quadrant_indicator(x):
    if x.endswith('ML'): 
        return 'many_large'
    if x.endswith('MS'):
        return 'many_small' 
    if x.endswith('FL'):
        return'few_large' 
    if x.endswith('FS'):
        return'few_small'
    if x.endswith('vardisa'):
        return'disappear'
    else:
        return np.nan
    

    else:
        quadrant=np.nan


'DWV_rice_ML'.endswith('ML')

#add the expanded varietis
df['A'] = df['A'].str.replace(pattern, 'CORP')
 
 str.replace('and', ', ') 

#                     
#melt df
dft.melt()
cropoccurence=pd.DataFrame(index=dft.index, columns=crops_by_country_d[country])
cropoccurence['cropsselected']=dft['Select the crops (maximum two) for which you want to list the varieties']
for cropsub in crops_by_country_d[country]:
    cropoccurence[cropsub]=cropoccurence['cropsselected'].apply(lambda s: str.index(s, cropsub) if cropsub in s else np.nan)

cropoccurence['firstcrop']= cropoccurence[crops_by_country_d[country]].idxmin(axis=1)
cropoccurence['secondcrop']= cropoccurence[crops_by_country_d[country]].idxmax(axis=1)
cropoccurence['secondcrop']=np.where(cropoccurence['secondcrop']==cropoccurence['firstcrop'], np.nan,cropoccurence['secondcrop'])



df[['sequence', 'sub_sequence']].apply(lambda s: str.index(*s), axis=1)
pd.Series({w: long_string.count(w) for w in word_list})







