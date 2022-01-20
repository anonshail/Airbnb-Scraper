# Airbnb-Scraper
A PoC script that lets you scrape Airbnb listings data in a certain time frame in a certain coordinate box. For this PoC, I have assumed the edges of Boston and found out all the Airbnb listings in that time in Boston. However, by simple changing the coordinates, this script could be used to scrape any and all Airbnb listings based on your requirements.

The way the algorithm works
Airbnb limits the amount of listings returned per call to a max of 50.

So the way I have solved this problem is by calling the API to obtain listings data in between two coordinates which form the corners of the rectangle of the area that we want location data. Then, I break down the rectangle into 4 quarters, and recursively call the same function that does the same thing. The recursion ends when no new listing data is rturned.

This can be used to scrape each and every listing within a given location. At the moment, the script does this only for Boston, but this can be used to scrape data for any location, however big for any time range as per your requirements.
