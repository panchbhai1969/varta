import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JioKisan.settings')

import django
django.setup()

import random
import string
import uuid
from JioKisan.models import User_reg, Produce, Consignment, FarmEntity, Request
from faker import Faker
from faker.providers import geo, date_time


fakegen = Faker()
fakegen.add_provider(geo)
fakegen.add_provider(date_time)
# fakegen.add_provider(ssn)
# fakegen.add_provider(company)
# fakegen.add_provider(bank)


def randomString(stringLength=10):
    """Generate a random string of letters, digits and special characters """
    randomString = uuid.uuid4().hex # get a random string in a UUID fromat
    randomString  = randomString.upper()[0:stringLength] # convert it in a uppercase letter and trim to your size.
    return randomString

def populateUser_reg(N=5):
    for entry in range(N):
        name = fakegen.name()
        phone_number = fakegen.phone_number()
        role = random.randint(1,4)
        location = fakegen.local_latlng(country_code="IN", coords_only=False)
        address = location[2]
        PAN = randomString(17)
        licence_number = randomString()
        vehicle_number = fakegen.license_plate()
        vehicle_model = random.randint(1,2)
        vehicle_capacity = random.randint(400,2000)
        organisation_name = fakegen.company()
        bank_account_number= randomString(13)
        GST_number= randomString(15)
        i = random.randint(0,1)
        isVerified= (i==0)
        position_latitude = location[0]
        position_longitude = location[1]
         
        if(role==3):
            user = User_reg.objects.get_or_create(name=name,phone_number=phone_number,role=role,address=address,
                                            PAN=PAN, licence_number=licence_number, vehicle_number=vehicle_number,
                                            vehicle_model=vehicle_model, vehicle_capacity=vehicle_capacity,
                                            organisation_name=organisation_name, bank_account_number=bank_account_number,
                                            GST_number=GST_number, isVerified=isVerified, 
                                            position_latitude=position_latitude, position_longitude=position_longitude,
                                            isHired = False, path=None, available_capacity =vehicle_capacity, current_address = address)
        else:
            user = User_reg.objects.get_or_create(name=name,phone_number=phone_number,role=role,address=address,
                                            PAN=PAN, licence_number=licence_number, vehicle_number=vehicle_number,
                                            vehicle_model=vehicle_model, vehicle_capacity=vehicle_capacity,
                                            organisation_name=organisation_name, bank_account_number=bank_account_number,
                                            GST_number=GST_number, isVerified=isVerified, 
                                            position_latitude=position_latitude, position_longitude=position_longitude)
                                            


def populateProduce(N=5):
    for entry in range(N):
        farmEntities = FarmEntity.objects.all()
        farmEntityCount = farmEntities.count()
        farmers = User_reg.objects.all().filter(role=1)
        farmersCount = farmers.count()
        amount = random.randint(200,800)
        FE_info = farmEntities[random.randint(0,farmEntityCount-1)]
        farmer_info = farmers[random.randint(0,farmersCount-1)]
        
        produce = Produce.objects.get_or_create(amount=amount, FE_info= FE_info,
                                                farmer_info = farmer_info)


def populateRequest(N=5):
    for entry in range(N):
        farmEntities = FarmEntity.objects.all()
        farmEntityCount = farmEntities.count()
        mandis = User_reg.objects.all().filter(role=3)
        mandisCount = mandis.count()
        amount = random.randint(200,800)
        FE_info = farmEntities[random.randint(0,farmEntityCount-1)]
        mandi_info = mandis[random.randint(0,mandisCount-1)]
        currentBid = random.randint(100,500)*10
        before_date = fake.future_date(end_date="+20d", tzinfo=None)


def populateConsignments:
    pass


if __name__ == "__main__":
    populateUser_reg(5)


