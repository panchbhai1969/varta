import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sihtrucks.settings')

import django
django.setup()

import random
from KdramaRocks.models import Driver
from faker import Faker
from faker.providers import geo


fakegen = Faker()
fakegen.add_provider(geo)

def populate(N=5):
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


if __name__=='__main__':
    populate(6)

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Driver

#     id = factory.Faker('id')
#     name = factory.Faker('name')
#     currentPositionLongitude = factory.Faker('currentPositionLongitude')
#     currentPositionLatitude = factory.Faker('currentPositionLatitude')
#     homeAddressLongitude = factory.Faker('homeAddressLongitude')
#     homeAddressLatitude = factory.Faker('homeAddressLatitude')
#     truckCapacity = factory.Faker('truckCapacity')
#     hired = factory.Faker('hired')
#     currentCapacity = factory.Faker('currentCapacity')