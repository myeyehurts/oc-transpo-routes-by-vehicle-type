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
