import os
import requests
import time
import csv
import config

#final data
allListings = {}

def getListingsByLatAndLng(ne_lat, ne_lng, sw_lat, sw_lng):
    #get listings based on lat, lng
    print("iteration for", ne_lat, ne_lng, sw_lat, sw_lng)

    variableString = '{"isInitialLoad":true,"hasLoggedIn":false,"cdnCacheSafe":false,"source":"EXPLORE","exploreRequest":{"metadataOnly":false,"version":"1.8.3","itemsPerGrid":100000,"tabId":"home_tab","refinementPaths":["/homes"],"flexibleTripDates":["february","january"],"flexibleTripLengths":["weekend_trip"],"datePickerType":"calendar","placeId":"ChIJGzE9DS1l44kRoOhiASS_fHg","source":"structured_search_input_header","searchType":"user_map_move","neLat":"%s","neLng":"%s","swLat":"%s","swLng":"%s","searchByMap":true,"query":"Boston, MA, United States","cdnCacheSafe":false,"treatmentFlags":["flex_destinations_june_2021_launch_web_treatment","new_filter_bar_v2_fm_header","merch_header_breakpoint_expansion_web","flexible_dates_12_month_lead_time","storefronts_nov23_2021_homepage_web_treatment","flexible_dates_options_extend_one_three_seven_days","super_date_flexibility","micro_flex_improvements","micro_flex_show_by_default","search_input_placeholder_phrases","pets_fee_treatment"],"screenSize":"large","isInitialLoad":true,"hasLoggedIn":false}}' % (ne_lat, ne_lng, sw_lat, sw_lng)

    headers = {
        'x-airbnb-api-key': config.apiKey,
    }

    params = (
        ('operationName', 'ExploreSections'),
        ('locale', 'en'),
        ('currency', 'USD'),
        ('variables', variableString),
        ('extensions', '{"persistedQuery":{"version":1,"sha256Hash":"8b7a938d8ce06e5d25f220a16a3afdd14f018cc91644393ef659fed909fd34f9"}}'),
    )

    response = requests.get('https://www.airbnb.com/api/v3/ExploreSections', headers=headers, params=params)
    return(response)

def searchByCoordinates(ne_lat, ne_lng, sw_lat, sw_lng, emptyZoom = 0):
    
    #Sleeping for 2 seconds before every API call / rate limiting 
    time.sleep(2)
   
    noListingAdded = True
    
    res = getListingsByLatAndLng(ne_lat, ne_lng, sw_lat, sw_lng)

    try:
        listings = res.json()['data']['presentation']['explore']['sections']['sections'][3]['section']['child']['section']['items']
        for listing in listings:
            listingId = listing["listing"]["id"]
            print(listingId)
            
            #check if this id exists in the data alread, if not add it
            if(listingId in allListings):
                continue

            print("adding", listingId, "to list")
            noListingAdded = False
            allListings[listingId] = {
                "id": listingId,
                "avgRating": listing["listing"]["avgRating"],
                "lat": listing["listing"]["lat"],
                "lng": listing["listing"]["lng"],
                "personCapacity": listing["listing"]["personCapacity"],
                "price": listing["pricingQuote"]["priceString"]
            }
    except:
        #This section runs only when the coordinates have 0 listings or the data is malformed
        #We can just ignore such data
        print("An error has occurred.")
        pass

    #using counter and not flag for finer control in the future
    if(noListingAdded):
        emptyZoom += 1
    else:
        emptyZoom = 0

    if(emptyZoom >= 1):
        return

    #recursively search smaller sections (in quarters)
    mid_lat = (ne_lat+sw_lat)/2
    mid_lng = (ne_lng+sw_lng)/2

    #quarter 1 ne_lat, ne_lng, mid_lat, mid_lng
    searchByCoordinates(ne_lat, mid_lng, mid_lat, sw_lng, emptyZoom)
    #quarter 2 ne_lat, mid_lng, mid_lat, sw_lng
    searchByCoordinates(ne_lat, ne_lng, mid_lat, mid_lng, emptyZoom)
    #quarter 3 mid_lat, ne_lng, sw_lat, mid_lng
    searchByCoordinates(mid_lat, mid_lng, sw_lat, sw_lng, emptyZoom)
    #quarter 4 mid_lat, mid_lng, sw_lat, sw_lng
    searchByCoordinates(mid_lat, ne_lng, sw_lat, mid_lng, emptyZoom)

#Searching coordinates of boston
searchByCoordinates(42.39734520885358, -70.90794825385785, 42.304989066820355, -71.21642374824262)

print("Final list of listing IDs")
print(allListings.keys())
print("Total number of listings:", len(allListings.keys()))

fields = ['ID', 'Average Rating', 'Latitude', 'Longitude', 'Person Capacity', 'Price']
rows = []

for listingId, listing in allListings.items():
    listingRow = [listing["id"], listing["avgRating"], listing["lat"], listing["lng"], listing["personCapacity"], listing["price"]]
    rows.append(listingRow)

# name of csv file 
filename = "boston_listings.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)
