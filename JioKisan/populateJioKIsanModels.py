import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JioKisan.settings')

import django
django.setup()

import random
from JioKisan.models import User_reg, Produce, Consignment, FarmEntity, Request
from faker import Faker
from faker.providers import geo, date_time


fakegen = Faker()
fakegen.add_provider(geo)
fakegen.add_provider(date_time)
# fakegen.add_provider(ssn)
# fakegen.add_provider(company)
# fakegen.add_provider(bank)

def populateUser_reg(N=5):
    for entry in range(N):
        name = fakegen.name()
        phone_number = fakegen.phone_number()
        role = random.randint(1,4)
        address = fakegen.local_latlng(country_code="IN", coords_only=False)[2]
        PAN = fakegen.bban()
        licence_number = 'ADSWAD23543'
        vehicle_number = fakegen.license_plate()
        vehicle_model = random.randint(1,2)
        vehicle_capacity = random.randint(400,2000)
        organisation_name = fakegen.company()
        bank_account_number= fakegen.bban()
        GST_number= fakegen.iban()
        i = random.randint(0,1)
        isVerified= (i==0)

        user = User_reg.objects.get_or_create(name=name,phone_number=phone_number,role=role,address=address,
                                            PAN=PAN, licence_number=licence_number, vehicle_number=vehicle_number,
                                            vehicle_model=vehicle_model, vehicle_capacity=vehicle_capacity,
                                            organisation_name=organisation_name, bank_account_number=bank_account_number,
                                            GST_number=GST_number, isVerified=isVerified)


if __name__ == "__main__":
    populateUser_reg(5)


