
# coding: utf-8

# In[9]:

import pandas as pd
import ujson
import pickle


# In[10]:

fpath = '../data/SFPD.csv'
pddf = pd.read_csv(fpath)
pddf.head(1)
pddf.replace(to_replace=['FORGERY/COUNTERFEITING','DRUG/NARCOTIC','PORNOGRAPHY/OBSCENE MAT','LARCENY/THEFT'], value=['FORGERY-COUNTERFEITING','DRUG-NARCOTIC','PORNOGRAPHY-OBSCENE MAT','LARCENY-THEFT'], inplace=True, limit=None, regex=False, method='pad', axis=None)


# In[11]:

hpdf = pd.read_csv('../data/SFlistingsN.csv')
hpdf.head()


# In[12]:

nbhoods = hpdf['neighborhoodName'].values
nbh = set(nbhoods)
print nbh


# In[13]:

ctype = pddf['Category'].values
ctp = set(ctype)
print ctp


# In[14]:

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


# In[18]:

rsfl = ['12M','6M', '3M','1M']

dist_list = ['TENDERLOIN']

for rsf in rsfl:
    for dist in dist_list:
        pdi = pddf[pddf['PdDistrict'] == dist.upper()]
        hpi = hpd[hpd['SFPD District'] == dist.upper()]

        pdct = pd.crosstab(pdi['Date'],pdi['Category'])
        pdct = pdct.set_index(pd.to_datetime(pdct.index))
        pdct['ALL'] = pdct.sum(axis=1)
        print pdct.head()
        break
    break



# In[27]:

#Output Crime and Housing for each district
rsfl = ['12M','6M', '3M','1M']

dist_list = ['Bayview','Central','Mission','Northern','SOUTHERN','TENDERLOIN']

for rsf in rsfl:
    for dist in dist_list:
        pdi = pddf[pddf['PdDistrict'] == dist.upper()]
        hpi = hpd[hpd['SFPD District'] == dist.upper()]

        pdct = pd.crosstab(pdi['Date'],pdi['Category'])
        pdct = pdct.set_index(pd.to_datetime(pdct.index))
        pdct = pdct.resample(rsf, how='sum')
        pdct['ALL'] = pdct.sum(axis=1)
        pdct.drop(pdct.head(1).index, inplace=True)
        pdct.drop(pdct.tail(1).index, inplace=True)
        
        
        hpdc = hpi.resample(rsf, how='mean')

        #find average housing cost in all of SF
        hop = hpd.resample(rsf, how='mean')
        #append to hpdc
        hpdc['alp_allsf'] = hop['averageListingPrice']

        #merge dataframes for plotting
        merge = pdct.join(hpdc)
        merge = merge.drop(merge.head(1).index)
        merge = merge.drop(merge.tail(1).index)

        merge.columns.name = 'Date'

        fname = '../cast2/app/static/data/perd/{}-{}.csv'.format(dist.upper(), rsf.upper())
        merge.to_csv(fname)
        #print fname
        #print '%s %s Data Exported' % (dist.upper(), rsf.upper())
    

    pdi = pddf.copy()
    hpi = hpd.copy()
    dist = 'All'    
    pdct = pd.crosstab(pdi['Date'],pdi['Category'])
    pdct = pdct.set_index(pd.to_datetime(pdct.index))
    pdct = pdct.resample(rsf, how='sum')
    pdct['ALL'] = pdct.sum(axis=1)
    pdct.drop(pdct.head(1).index, inplace=True)
    pdct.drop(pdct.tail(1).index, inplace=True)
    
    hpdc = hpi.resample(rsf, how='mean')
    
    #find average housing cost in all of SF
    hop = hpd.resample(rsf, how='mean')
    #append to hpdc
    hpdc['alp_allsf'] = hop['averageListingPrice']

    #merge dataframes for plotting
    merge = pdct.join(hpdc)
    merge = merge.drop(merge.head(1).index)
    merge = merge.drop(merge.tail(1).index)

    merge.columns.name = 'Date'
    fname = '../cast2/app/static/data/perd/{}-{}.csv'.format(dist.upper(), rsf.upper())
    merge.to_csv(fname)
    #print '%s %s Data Exported' % (dist.upper(), rsf.upper())  
    print 'All %s Data Exported' % (rsf.upper()) 
print 'All Data Exported'


# In[ ]:



