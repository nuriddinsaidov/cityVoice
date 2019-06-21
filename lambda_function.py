# importing the requests library
import requests


class Flight:

    headers = {
        "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "2c2e4d17b0mshcc471f8a7475016p16c892jsn034748cb94d5"
    }

    type = ""

    # Class Attribute
    version = "v1.0"

    URI = " https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices"

    # Initializer / Instance Attributes
    def __init__(self, attr):
        self.attr = attr

    # instance method
    def browsequotes(self):
        self.build_url("browsequotes")
        response = requests.get(self.URI, headers=self.headers)
        return response.json()

    def build_url(self, type):
        separator = "/"
        self.URI += separator + type + separator + self.version
        for k, v in self.attr.items():
            self.URI += separator + v


param = dict()
param["country"] = "US"
param["currency"] = "USD"
param["locale"] = "en-US"
param["originplace"] = "SFO-sky"
param["destinationplace"] = "JFK-sky"
param["outboundpartialdate"] = "2019-09-01"

flight = Flight(param)

print(flight.browsequotes())

#
# version = "v1.0"
#
# type = "browsequotes"
#
# country = "US"
#
# currency = "USD"
#
# locale = "en-US"
#
# originplace = "SFO-sky"
#
# destinationplace = "JFK-sky"
#
# outboundpartialdate = "2019-09-01"
#
# # api-endpoint
# URI = " https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/%s/%s/%s/%s/%s/%s/%s/%s/" % (type, version, country, currency, locale, originplace, destinationplace, outboundpartialdate)
#
# # location given here
# location = "delhi technological university"
#
# # defining a params dict for the parameters to be sent to the API
# headers = {
#     "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
#     "X-RapidAPI-Key": "2c2e4d17b0mshcc471f8a7475016p16c892jsn034748cb94d5"
# }
# payload = {}
#
# # sending get request and saving the response as response object
# r = requests.get(URI, headers=headers)
#
#
# # extracting data in json format
# data = r.json()
#
# print(data)

# extracting latitude, longitude and formatted address
# of the first matching location
#latitude = data['results'][0]['geometry']['location']['lat']
#longitude = data['results'][0]['geometry']['location']['lng']
#formatted_address = data['results'][0]['formatted_address']

# printing the output
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
#      % (latitude, longitude, formatted_address))