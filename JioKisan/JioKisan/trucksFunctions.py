from JioKisan.models import User_reg, Consignment
from AssignDelivery import *

def assignJob(mDict):
    user = User_reg.objects.get(PAN=mDict['PAN'])
    if (user.role == 2) and (user.isHired == False):
        mapConsignments(mDict)


def getDriverDetails(mDict):
    user = User_reg.objects.get(PAN=mDict['PAN'])
    if(user.role!=2):
        raise "Invalid User, User Not A Driver"
    
    if(user.isHired==true):
        path = getPath(mDict)

def getPath(mDict):
    user = User_reg.objects.get(PAN=mDict['PAN'])
    if (user.role == 2) and (user.isHired == True):
        stop_strings = (user.path).split('|')

    locations = {}
    i=0
    for stop in stop_strings:
        purpose = stop.split(':')[0]
        rem_string = stop.split(':')[1]
        pk_consignment = rem_string.split(';')[0]
        rem_string = rem_string.split(';')[1]
        latitude = rem_string.split(',')[0]
        longitude = rem_string.split(',')[1]
        consignment_object= Consignment.objects.get(pk=pk_consignment)
        consignment_id = consignment_object.ucid
        if(purpose=='Pickup Location'):
            person_name = consignment_object.prod.farmer_info.name
            phone_number = consignment_object.prod.farmer_info.phone_number
            address = consignment_object.prod.farmer_info.address 
            
        else:
            person_name = consignment_object.req.mandi_info.name
            phone_number = consignment_object.req.mandi_info.phone_number
            address = consignment_object.req.mandi_info.address 
        location_info = {
            'purpose':purpose,
            'consignment_id':consignment_id,
            'person_of_concern':person_name,
            'phone_number':phone_number,
            'address':address,
            'latitude':latitude,
            'longitude':longitude
        }
        locations[str(i)] = location_info
        i=i+1
    
    return locations
    

if __name__ == "__main__":
    users = User_reg.objects.all().filter(role=2)
    user = users[3]
    


