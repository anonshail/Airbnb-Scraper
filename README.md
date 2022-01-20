# INTRODUCTION
A PoC script that lets you scrape Airbnb listings data in a certain time frame in a certain coordinate box. For this PoC, I have assumed the edges of Boston and found out all the Airbnb listings in that time in Boston. However, by simple changing the coordinates, this script could be used to scrape any and all Airbnb listings based on your requirements.

# ALGORITHM
Airbnb limits the amount of listings returned per call to a max of 50.
So the way I have solved this problem is by calling the API to obtain listings data in between two coordinates which form the corners of the rectangle of the area that we want location data. Then, I break down the rectangle into 4 quarters, and recursively call the same function that does the same thing. The recursion ends when no new listing data is rturned.
This can be used to scrape each and every listing within a given location. At the moment, the script does this only for Boston, but this can be used to scrape data for any location, however big for any time range as per your requirements.

# DATA RECORDED:
For now, the following data has been recorded in the CSV file:
1) Airbnb ID
2) Average Rating
3) Latitude
4) Longitude
5) Capacity
6) Price

# FUTURE UPGRADES:
In the future, the following changes can be made to make the program more utilitarian:
1) Allow the user to specify constraints such as duration and date range without making
any assumptions. (This change can easily be made if required)
2) Allow the user to specify the latitude and longitude constraints so that the user get’s
specific data. (This change can easily be made if required)
3) Include more data in the CSV such as (but not limited to) the following:
&emsp;* Link to listing. This would basically just be a concatenation of
  ‘https://www.airbnb.com/rooms/’ with the Airbnb ID. (This change can easily be
  made if required)
&emsp;* Description (This change can easily be made if required)
&emsp;* Picture URL (This change can easily be made if required)
&emsp;* Host ID (This change can easily be made if required)
&emsp;* Host URL (This change can easily be made if required)
&emsp;* Is host super host (boolean) (This change can easily be made if required)
&emsp;* Roomtype (This change can easily be made if required)
&emsp;* Bedroom data (This change can easily be made if required)

4) Chaining multiple coordinate “boxes” to allow for more control over the area scraped
