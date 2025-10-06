from datetime import datetime

from .models import Route, Trip
from google.transit import gtfs_realtime_pb2
import requests
import pytz
import os
from dotenv import load_dotenv

def get_trips():
    try:
        load_dotenv()
        url = "https://nextrip-public-api.azure-api.net/octranspo/gtfs-rt-vp/beta/v1/VehiclePositions"
        hdr = {
            # Request headers
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': os.getenv('SUBSCRIPTION_KEY'),
        }

        response = requests.get(url, headers=hdr)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content) # get gtfs data from endpoint

        for entity in feed.entity:
            if entity.HasField("vehicle"):
                print(entity.vehicle.trip.route_id)
                route_number = entity.vehicle.trip.route_id
                if route_number not in {'', ' ', '1-350', '2-354', '4-354'}: # omit trains, missing route numbers
                    try:
                        route = Route.objects.get(number=route_number) # try to find route matching number
                        new_trip = Trip()
                        new_trip.route = route
                        new_trip.vehicle_number = entity.vehicle.vehicle.id
                        new_trip.time_entered = datetime.now(pytz.timezone('US/Eastern')) # get current time
                        new_trip.save()
                    except Route.DoesNotExist:
                        continue
    except Exception as e:
        print(e)

def bus_types_by_route(route_number):
    try:
        route = Route.objects.get(number=route_number)
        bus_types = {
        "Electric Bus" : 0,
        "Tiny Bus" : 0,
        "Old Bus": 0,
        "Accordion Bus": 0,
        "Double Decker": 0
        }
        for trip in Trip.objects.filter(route=route):
            trip_bus_type = get_bus_type(trip.vehicle_number)
            if trip_bus_type in bus_types.keys():
                bus_types[trip_bus_type] += 1
        print("Results for route " +route_number+ ":")
        for key in bus_types:
            print(key+ ": " + str([bus_types[key]]))
    except Route.DoesNotExist:
        print("Route " +route_number+ " not found")

def get_bus_type(vehicle_id):
    if len(vehicle_id) != 4:
        return None
    else:
        first_digit = int(vehicle_id[0])
        if first_digit == 2:
            return "Electric Bus"
        elif first_digit == 4:
            second_digit = int(vehicle_id[1])
            if second_digit > 5:
                return "Tiny Bus"
            else:
                return "Old Bus"
        elif first_digit == 6:
            return "Accordion Bus"
        elif first_digit == 8:
            return "Double Decker"
        else:
            return None

def input_route():
    print("Enter a bus route number.")
    route_number = input()
    bus_types_by_route(route_number)
    while route_number is not 'X':
        route_number = input()
        bus_types_by_route(route_number)