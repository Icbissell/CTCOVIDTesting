import geopandas
from geopy.geocoders import Nominatim
from scipy.spatial import distance
import pandas as pd
import math

#Lat, Long values will be stored in zips array
def addressToLatLong():
    geolocator = Nominatim(user_agent='CTCounties')
    zips = []
    df = pd.read_csv("/home/bissell/Desktop/CTCounties/COVID_Testing_Locations_CT_Sheet1.csv", na_values = ['no info', '.'])
    for i in range(420):
        location = geolocator.geocode(df["Street Address"][i] + " " + df["City"][i] + " " + df["State"][i] + " " + df["ZIP Code"][i])
        if location:
            print((location.latitude, location.longitude))
            zips.append((location.latitude, location.longitude))
        else:
            zips.append("Not available")

    for i in range(len(zips)):
        print(zips[i])

def deg2rad(degree):
    return degree * math.pi / 180.0

def rad2deg(radians):
    return radians*180.0/math.pi

def calcDistance(lat1, lon1, lat2, lon2):
    theta = lon2 - lon1
    dist = math.sin(deg2rad(lat1)) * math.sin(deg2rad(lat2)) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.cos(deg2rad(theta))
    dist = math.acos(dist)
    dist = rad2deg(dist)
    dist = dist * 60 #60 nautical miles per degree of seperation
    return dist

def findNeighbors():
    geolocator = Nominatim(user_agent="CTCounties")
    df = pd.read_csv("/home/bissell/Desktop/CTCounties/COVID_Testing_Locations_CT_Sheet1.csv", na_values = ['no info', '.'])
    print("Enter your address: ")
    address = input()
    print("What number of closest COVID Testing sites would you like to see? ")
    numSites = int(input())
    addressLoc = geolocator.geocode(address)
    print((addressLoc.latitude, addressLoc.longitude))
    if addressLoc:
        testingLocs = []
        for i in range(420):
            testingLocs.append((df["Longitude"][i],df["Latitude"][i]))
        testingDists = []
        for i in range(420):
            if testingLocs[i][0] == "Not available":
                continue
            else:
                testingDists.append(calcDistance(float(addressLoc.latitude), float(addressLoc.longitude), float(testingLocs[i][1]), float(testingLocs[i][0])))
        testingDists.sort()
        for i in range(numSites):
            print("Location ", i + 1, "distance: ", testingDists[i])
    else:
        print("Invalid Address")


findNeighbors()
