# SEEDS - Pillar 3 

Code to extract transform and load Pillar 3 data  <add link> --> add link to report here. 

# Technologies
Project is created with: 
- Python 3.8.0 
- api keys & secrets loaded using dotenv. and .env (not published)

# Data
Source data for this project from Kobo forms. 

# Structure
```
├───Documentation           <- data documentation, database scheme, overview of various forms. 
│   
├───Data download           <-Code to automate data download
|   ├download_forms.py              <-Creates exports on Kobo and downloads forms to \RAW on Box.
|   └get_csv.py                     <- helper file to create exports, run download_froms.py when env. is active in data download folder.
├───Data download           <-Code to automate data cleaning. input files are in \RAW on box, output files are in \clean on box. 
|   |                        Structure of cleaning and output files:"split(in various countries)-apply (transormations)-combine ) into one set containing all countries and forms (in e.g. FFS-profile all
|   ├clean_general_documentation.py <-Cleans general documentation forms, including FFS profiles, weekly monitoring, diagnostic stage forms. Creates unique ID_FFS_ID
|   ├clean_diversiy_wheel_crops.py      <-Cleans diversity wheel for crops, results in long-form datasets, ID_FFS_ID*crop*quadrant
|   ├clean_diversiy_wheel_variety.py    <-Cleans diversity wheel for varieties, results in long-form datasets, row=ID_FFS_ID*crop*quadrant*variety 
|   ├clean_diversiy_wheel_var_traits.py <-Cleans diversity wheel for varieties, results in long-form datasets, row=ID_FFS_ID*crop*quadrant*variety*traits 
|   ├clean_pvs_forms                    <-Cleans participatory variety selection forms, including all AESA forms. Results in Wide form datasets row=ID_FFS_ID
|   └clean_end_of_season.py             <-Cleans end of season documentation including dissemination activities. Results in wide form datasets row=ID_FFS_ID      
|   
├───requirements.txt        <-requirements (pip install requirements.txt)
│   
│      
│      
│      
│   
└───                     

----Data stored on Box

\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\
├───data                 
    │   
    ├───RAW                 <-Raw data extracted by get_data.py
    │   ├───PPB             <-PPB  forms (all countries)
    │   ├───PVE             <-PVE (variety enhancement) forms (all countries)
    │   └───PVS             <-PVS (variety selection) forms (all countries)        
    ├───clean               <-Cleaned datasets

```








