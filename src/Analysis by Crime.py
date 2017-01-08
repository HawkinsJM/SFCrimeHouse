
# coding: utf-8

# In[94]:

import pandas as pd
import ujson
import pickle
import numpy as np


# In[95]:

fpath = '../data/SFPD.csv'
pddf = pd.read_csv(fpath)
pddf.head(1)


# In[96]:

hpdf = pd.read_csv('../data/SFlistingsN.csv')
hpdf.head()


# In[97]:

nbhoods = hpdf['neighborhoodName'].values
nbh = set(nbhoods)
print nbh


# In[98]:

pddf.replace(to_replace=['FORGERY/COUNTERFEITING','DRUG/NARCOTIC','PORNOGRAPHY/OBSCENE MAT','LARCENY/THEFT'], value=['FORGERY-COUNTERFEITING','DRUG-NARCOTIC','PORNOGRAPHY-OBSCENE MAT','LARCENY-THEFT'], inplace=True, limit=None, regex=False, method='pad', axis=None)
ctype = pddf['Category'].values
ctp = set(ctype)
print ctp


# In[99]:

## Clean Trulia dataset

#only use data for 2 bedroom poperties
hpdf = hpdf[hpdf['type'] == '2 Bedroom Properties']

#make east SF neighborhoods into SFPD districts, those are the ones that map decently/semi-easily with Trulia data. Get rid of the others
Bayview = ['Bayview', 'Central Waterfront', 'Hunters Point', 'Mission Bay', 'Portola', 'Potrero Hill', 'Silver Terrace']
Central = ['Central', 'Downtown', 'Financial District', 'Nob Hill', 'North Beach', 'Russian Hill', 'Telegraph Hill']
Mission = ['Mission', 'Mission Dolores', 'Noe Valley']
Northern = ['Northern', 'Alamo Square', 'Cow Hollow', 'Duboce Triangle', 'Hayes Valley', 'Lower Pacific Heights', 'Marina', 'Pacific Heights', 'Western Addition']
Southern = ['Southern', 'SoMa', 'South Beach']
Tenderloin = ['Tenderloin', 'Civic Center']

districts = [Bayview, Central, Mission, Northern, Southern, Tenderloin]

hpd = pd.DataFrame()

for district in districts:
    hpdnh = pd.DataFrame()
    
    for nh in district:
        hnh=hpdf[hpdf['neighborhoodName'] == nh]
        hnh['SFPD District'] = str(district[0]).upper()
        hpdnh=pd.concat([hpdnh,hnh])

    hpd=pd.concat([hpd,hpdnh])

#drop other columns
hpd.drop('Unnamed: 0', axis=1, inplace=True)
hpd.drop('medianListingPrice', axis=1, inplace=True)
hpd.drop('numberOfProperties', axis=1, inplace=True)
hpd.drop('TruliaNID', axis=1, inplace=True)

#average together multiple listings from the same week
hpd = hpd.set_index(pd.to_datetime(hpd['weekEndingDate']))
hpd = hpd.groupby(['weekEndingDate','SFPD District']).mean()
hpd = pd.DataFrame(hpd).reset_index()
hpd = hpd.set_index(pd.to_datetime(hpd['weekEndingDate']))
hpd.drop('weekEndingDate', axis=1, inplace=True)


# In[100]:

#Fix Northern NoRthern in HPD
rsfl = ['12M','6M', '3M','1M']

dist_list = ['Bayview','Central','Mission','Northern','SOUTHERN','TENDERLOIN']

ctypes = sorted(['WEAPON LAWS','SECONDARY CODES','WARRANTS','ROBBERY','BURGLARY',
	 'SUSPICIOUS OCC','ASSAULT','DRUNKENNESS','OTHER OFFENSES','FRAUD','DRUG-NARCOTIC',
	 'TRESPASS', 'LARCENY-THEFT','VANDALISM','NON-CRIMINAL','VEHICLE THEFT','MISSING PERSON',
	 'DISORDERLY CONDUCT'])


# In[113]:

crime = 'Drug-Narcotic'
rsf = "6M"
pdi = pddf[pddf['Category'] != None]
pdct = pd.crosstab(pdi['Date'],pdi['PdDistrict'])
pdct = pdct.set_index(pd.to_datetime(pdct.index))
pdct = pdct.resample(rsf, how='sum')
pdct.head()


# In[104]:

for rsf in rsfl:
    #create Housing for every dist table
    hpi = hpd[['averageListingPrice']]
    hpi = hpd.reset_index().pivot(index='weekEndingDate', columns='SFPD District', values='averageListingPrice')
    hpct = hpi.set_index(pd.to_datetime(hpi.index))
    hpct = hpct.resample(rsf, how='mean')
    hpct['ALL'] = hpct.mean(axis=1)
    hpct.drop(hpct.head(1).index, inplace=True)
    hpct.drop(hpct.tail(1).index, inplace=True)
    print hpct.head()
    fname = '../cast2/app/static/data/AllDistHouse-{}.csv'.format(rsf.upper())
    hpct.to_csv(fname)
print 'Data Exported'


# In[107]:

#Create Crime Data Tables
for rsf in rsfl:
    for crime in ctypes:
        pdi = pddf[pddf['Category'] == crime.upper()]
        pdct = pd.crosstab(pdi['Date'],pdi['PdDistrict'])
        pdct = pdct.set_index(pd.to_datetime(pdct.index))
        pdct = pdct.resample(rsf, how='sum')
        pdct['ALL'] = pdct.sum(axis=1)
        pdct.drop(pdct.head(1).index, inplace=True)
        pdct.drop(pdct.tail(1).index, inplace=True)
        fname = '../cast2/app/static/data/perc/{}-{}.csv'.format(crime.upper(), rsf.upper())
        pdct.to_csv(fname)
        print '%s %s Data Exported' % (crime.upper(), rsf.upper())  
    print 'All %s Data Exported' % (rsf.upper()) 
print 'All Data Exported'


# In[116]:

#Create Crime Data Tables
for rsf in rsfl:
        pdi = pddf[pddf['Category'] != None]
        pdct = pd.crosstab(pdi['Date'],pdi['PdDistrict'])
        pdct = pdct.set_index(pd.to_datetime(pdct.index))
        pdct = pdct.resample(rsf, how='sum')
        pdct['ALL'] = pdct.sum(axis=1)
        pdct.drop(pdct.head(1).index, inplace=True)
        pdct.drop(pdct.tail(1).index, inplace=True)
        fname = '../cast2/app/static/data/perc/{}-{}.csv'.format('ALL', rsf.upper())
        pdct.to_csv(fname) 
        print 'All %s Data Exported' % (rsf.upper()) 
print 'All Data Exported'


# In[106]:

pdct.head()


# In[ ]:



