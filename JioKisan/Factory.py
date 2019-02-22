import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JioKisan.settings')

import django
django.setup()

import random
from trucks.models import Driver, Delivery
from faker import Faker
from faker.providers import geo, date_time


fakegen = Faker()
fakegen.add_provider(geo)
fakegen.add_provider(date_time)

def populateDriver(N=5):
    for entry in range(N):
        name = fakegen.name()
        currentPositionLongitude = fakegen.longitude()
        currentPositionLatitude = fakegen.latitude()
        homeAddressLongitude = fakegen.longitude()
        homeAddressLatitude = fakegen.latitude()
        truckCapacity = random.randint(400,2000)
        hired = False
        currentCapacity = 0
        
        driver = Driver.objects.get_or_create(name=name,
                                              currentPositionLongitude=currentPositionLongitude,
                                              currentPositionLatitude=currentPositionLatitude,
                                              homeAddressLongitude=homeAddressLongitude,
                                              homeAddressLatitude=homeAddressLatitude,
                                              truckCapacity=truckCapacity
                                              )[0]

def populateDelivery(N=5):
    for entry in range(N):
        pickupLocationLongitude = fakegen.longitude()
        pickupLocationLatitude = fakegen.latitude()
        dropLocationLongitude = fakegen.longitude()
        dropLocationLatitude = fakegen.latitude()
        pickupDate = fakegen.date_time_this_month(before_now=True, after_now=False, tzinfo=None)
        dropDate = fakegen.date_time_this_month(before_now=False, after_now=True, tzinfo=None)
        weight = random.randint(0,2000)
        choices = ["PENDING", "TRANSIT", "COMPLETED"]
        index = random.randint(0,2)
        chosen = choices[index]

        delivery = Delivery.objects.get_or_create(pickupLocationLongitude=pickupLocationLongitude,
                                                  pickupLocationLatitude=pickupLocationLatitude,
                                                  dropLocationLongitude=dropLocationLongitude,
                                                  dropLocationLatitude=dropLocationLatitude,
                                                  pickupDate=pickupDate,
                                                  dropDate=dropDate,
                                                  weight=weight,
                                                  status=chosen)


if __name__=='__main__':
    populateDriver(6)
    populateDelivery(6)
