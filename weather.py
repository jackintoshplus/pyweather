import json
import geojson
from urllib.request import urlopen
from urllib.error import URLError

# Variable Storage
#URLS
target = "https://api.weather.gov/"
forecastURL = ""

#Data
initialJSON = "";
forecastResponse = "";
forecastJSON = ""
latitude = float(0.0000)
longitude = float(0.000)
city = ""
count = 0
forecastStorage = ""

#Reset Locks
latitudeCheckActive = True;
longitudeCheckActive = True;



# Main Application
#Attempt to connect to target weather URL
try:
    initialJSON = urlopen(target)
except URLError:
    print("Connection to " + target + "failed. Exiting.")
    quit();

#Read JSON Response from URL
initialResponse = json.loads(initialJSON.read())

if(initialResponse['status'] == 'OK'):
    print("URL Online!")
else:
    print("Website abnormal response: " + initialResponse['status'] + ". Exiting.")
    quit();


#Collect latitude and logitude from user
while(latitudeCheckActive):
    try:
        latitude = input("Enter your latitude:")
        latitude = float(latitude)
    except ValueError:
        print("Invalid entry. Please try again.")
        continue

    if(latitude < -90 or latitude > 90):
        print("Latitude out of range [-90, 90]")
    else:
        latitudeCheckActive = False;

while(longitudeCheckActive):
    try:
        longitude = input("Enter your longitude:")
        longitude = float(longitude)
    except ValueError:
        print("Invalid entry. Please try again.")
        continue

    if(longitude < -90 or longitude > 90):
        print("Longitude out of range [-90, 90]")
    else:
        longitudeCheckActive = False;

#Request data from URL using latitude and longitude

#Convert integers to string in order for forecastURL string concentation  
latitude = str(latitude)
longitude = str(longitude)
forecastURL = target + "points/"+ latitude + "," + longitude


#Attempt to connect to forecast URL
try:
    forecastJSON = urlopen(forecastURL)
except URLError:
    print("Connection to " + forecastURL + " failed. Exiting.")
    quit();

#Read JSON Response from forecast URL
forecastResponse = json.loads(forecastJSON.read())

#Capture nearby city
city = forecastResponse['properties']['relativeLocation']['properties']['city'] + "," + forecastResponse['properties']['relativeLocation']['properties']['state']
print(city)

#Change forecast URL to localized forecast URL using the JSON Response 
forecastURL = forecastResponse['properties']['forecast']

#Attempt to connect to new forecast URL
try:
    forecastJSON = urlopen(forecastURL)
except URLError:
    print("Connection to " + forecastURL + " failed. Exiting.")
    quit();

#Read JSON Response from new forecast URL
forecastResponse = json.loads(forecastJSON.read())

#Print forecast
print("Weather Forecast for " + city + ":");

#Forecast output loop
while(count < 14):
    forecastStorage = forecastResponse['properties']['periods'][count]['name'] + "\n" + forecastResponse['properties']['periods'][count]['detailedForecast'] + "\n"
    print(forecastStorage)
    count += 1

quit();
