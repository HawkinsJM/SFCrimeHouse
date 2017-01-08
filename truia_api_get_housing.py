import requests
import xmltodict
import pandas as pd
import os.path

###TRULIA'S API HAS BEEN CLOSED DOWN - THIS SCRIPT WILL NO LONGER WORK###
#Borrows heavily from  - https://github.com/mattkoskela/trulia/blob/master/trulia/location.py

#Input your API key here - e.x. api_key = '3h38sdf783hj47fjf7'
api_key = ''

#Function to get a list of neighborhoods in San Fransisco
def get_Neighborhoods():
    city = 'San Francisco'
    state = 'CA'
    url = "http://api.trulia.com/webservices.php"

    #We are seeking information about the neighborhoods from the LocationInfo portion of the API
    payload = {
        "library": "LocationInfo", 
        "function": "getNeighborhoodsInCity", #getCitiesInState #getNeighborhoodsInCity
        "city": city,
        "state": state,
        "apikey": api_key
    	}

    xml = requests.get(url, params=payload)
    results = xmltodict.parse(xml.content)
    neighborhoods = results["TruliaWebServices"]["response"]["LocationInfo"]["neighborhood"]
    nbh = pd.DataFrame.from_dict(neighborhoods)
    nbh.to_csv('nbh.csv')
    print 'Neghborhood IDs Exported'

#Get list of neighborhoods if it doesnt exist already.
#only needs to be run once since Neighborhoods are static
if os.path.isfile("nbh.csv") != True:
    get_Neighborhoods()

#Function to get housing data for each district
def get_Data():
    #Reads Neighborhoods ID file back and converts it to a list
    nbh = pd.read_csv('nbh.csv')
    nbhids = nbh['id'].tolist()
    #There appears to be no data for Fort Mason or Union Square, so we drop them
    del nbhids[85] 
    del nbhids[26] 

    #Creats a master dataframe to store all the data we want exported
    master = pd.DataFrame()

    for id in nbhids:

        city = 'San Francisco'
        state = 'CA'
        url = "http://api.trulia.com/webservices.php"
        neighborhood_id = id
        startDate = '2007-01-05'
        endDate = '2015-10-20'

        payload = {
            "library": "TruliaStats",
            "function": "getNeighborhoodStats",
            "neighborhoodId": neighborhood_id,
            "city": city,
            "state": state,
            "startDate": startDate,
            "endDate": endDate,
            "statType": "listings",
            "apikey": api_key
        	}


        xml = requests.get(url, params=payload)
        results = xmltodict.parse(xml.content)

        nname= results["TruliaWebServices"]["response"]["TruliaStats"]["location"]['neighborhoodName']
        nid= results["TruliaWebServices"]["response"]["TruliaStats"]["location"]['neighborhoodId']
        ncity= results["TruliaWebServices"]["response"]["TruliaStats"]["location"]['city']
        nstate= results["TruliaWebServices"]["response"]["TruliaStats"]["location"]['state']
        nstat = results["TruliaWebServices"]["response"]["TruliaStats"]['listingStats']['listingStat']
        
        #creates a data frame for this particular neighborhoodID
        listing_data = pd.DataFrame()

        #Creates a dataframe based on the data for each week, and then adds that to the listing_data dataframe
        for week in nstat:
            listing = week['listingPrice']['subcategory']
            try:
                listing_data_week = pd.DataFrame.from_dict(listing, orient='columns')
            #This excpetions skips blank enteries
            except ValueError:
                print("skipping one set")
                pass
            listing_data_week['weekEndingDate'] = week['weekEndingDate']
            listing_data_week['neighborhoodName'] = nname
            listing_data_week['TruliaNID'] = nid
            listing_data_week['City'] = ncity
            listing_data_week['State'] = nstate
            #adds new weekly data to listing_data dataframe
            listing_data=pd.concat([listing_data,listing_data_week])

        #adds all the weekly data from one neighborhoodID to the master dataframe
        master=pd.concat([master,listing_data])
    #Exports the data as a csv file
    master.to_csv('SFlistingsN.csv')
    print 'Data Exported'

#Pulls the data from the API
get_Data()
