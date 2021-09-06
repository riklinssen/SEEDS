
###################download general documentation forms####################
####put these in datafolder: "C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PPB"

from koboextractor import KoboExtractor
import pandas as pd
import requests
import sys
import os
from pathlib import Path
#import get_csv as gcsv
from io import StringIO
import numpy as np
import get_csv as gcsv
import csv
import io
from contextlib import closing

###########API tokens, secrets
username =os.getenv("KOBO_USERNAME")
passwd = os.getenv("KOBO_PASSWD")
domain = "https://kobo.humanitarianresponse.info/"
token=os.getenv("KOBO_TOKEN")
        

uids=[]
cntrys=[]
descriptions=[]
names=[]
formtypes=[]
kobo = KoboExtractor(os.getenv("KOBO_TOKEN"), 'https://kobo.humanitarianresponse.info/api/v2/')


assets = kobo.list_assets()


for i in range(0, 100):
    #only deployed surveys
    if (assets['results'][i]['asset_type']=='survey') & (assets['results'][i]['has_deployment']==True): 
        description=assets['results'][i]['settings']['description']
        formtype=None
        #GENERAL DOCUMENTATION
        if 'General Documentation' in description: 
            formtype='General Documentation'             
        ##PVS forms
        if 'PVS' in description:
            formtype='Participatory Variety Selection (PVS)'
        ## end of season evluation
        if 'End of Season' in description: 
            formtype='End of season evaluation'
        #continue next interation in case formtype is still None
        if formtype==None: 
            continue
                   
        if formtype=='General Documentation':                  
            country=description.split('__')[0] 
        else: 
            country=description.split('-')[0].strip() 
        print(country, description, formtype)
        uid= assets['results'][i]['uid']
        
        uids.append(uid)            
        cntrys.append(country)
        descriptions.append(description)
        formtypes.append(formtype)
            

to_download=pd.DataFrame(zip(uids, cntrys, descriptions, formtypes), columns=['uids', 'cntrys', 'descriptions', 'formtype'])



#####CREATE  EXPORTS for general documentation
####################################################prepare all exports. 
for uid in  to_download['uids']: 
    export=gcsv.create_export(asset=uid,  username=username, passwd=passwd, domain=domain, lang='English (en)', type_='csv')





####################add something here so the there's some wait time between making the export and download the data. 


####################get a list of urls to to download and add to to_download
urls = []
for uid in to_download['uids']: 
    url=gcsv.latest_url(asset=uid, username=username, passwd=passwd, domain=domain)
    urls.append(url)

to_download['url']=urls
#download and export to datafile
#get list to iterate over 
assetnames=to_download['uids'].to_list()
countrynames=to_download['cntrys'].to_list()
forms=to_download['descriptions'].to_list()
formtype=to_download['formtype'].to_list()
links=to_download['url'].to_list()



for assetname, countryname, form, link, formtype in zip(assetnames,countrynames, forms, links, formtype):
    headers = {"Authorization": f'Token {token}'}
    data_dict = []
    urlData = requests.get(link, headers=headers).content
    df = pd.read_csv(io.StringIO(urlData.decode('utf-8')), sep=';', error_bad_lines=False)
    df['country']=countryname
    df['form']=form
    df['asset_id']=assetname
    df['downloaded_at']=pd.Timestamp.today()
    #sort by time. 
    df['endtime']=pd.to_datetime(df['end'], infer_datetime_format=True)
    df.sort_values(by='endtime', inplace=True)                            
    filename=form.replace("\n", "")+'.csv'
    if formtype=='Participatory Variety Selection (PVS)':                
        data_path=Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PVS")
    if formtype=='General Documentation':
        data_path=Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\PPB")
    if formtype=='End of season evaluation':
        data_path=Path(r"C:\Users\RikL\Box\MEAL_SDHS\KOBO\Kobo Pillar 1_PPB\Data\RAW\End_of_season")
    print(assetname, countryname, form, link, formtype)
    df.to_csv(data_path/filename, encoding='utf-8')                                                                                  

                            
                                                               
                                                          
                                                                                                                                           