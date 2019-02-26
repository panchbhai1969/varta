from django.db import models
import uuid
import time
from pymemcache.client import base
 


STATUS_CHOICES = {
    1: "farmer",
    2: "truck_driver",
    3: "mandi",
    4: "farm_tool_sellers"
}
VEHICLE_MODELS= {
    1:'AC',
    2:'NON AC'
}
MEASUREMENT_TYPES = {
    1:'KG',
    2:'METRIC TON',
    3:'DOZENS',
    4:'LITRES'
}

class User_reg(models.Model):
    name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=40,unique=True)
    role = models.IntegerField(default=0)
    address = models.CharField(max_length=100)
    PAN = models.CharField(max_length=10,primary_key=True)
    licence_number=models.CharField(max_length=20,default=None, blank=True, null=True)
    vehicle_number=models.CharField(max_length=20,default=None, blank=True, null=True)
    vehicle_model=models.IntegerField(default=None, blank=True, null=True)
    vehicle_capacity=models.IntegerField(default=None, blank=True, null=True)
    organisation_name=models.CharField(max_length=80,default=None, blank=True, null=True)
    bank_account_number=models.CharField(max_length=20,default=None, blank=True, null=True)
    GST_number=models.CharField(max_length=20,default=None, blank=True, null=True)
    isVerified=models.BooleanField()

class FarmEntity(models.Model):
    ufid = models.IntegerField(primary_key=True)
    name =models.CharField(max_length=40)
    measured_in=models.IntegerField()
    MSP=models.IntegerField()

class  Produce(models.Model):
    upid=models.IntegerField(primary_key=True)
    amount=models.IntegerField()
    FE_info=models.ForeignKey(FarmEntity,on_delete=models.CASCADE,db_column='ufid')
    farmer_info=models.ForeignKey(User_reg,on_delete=models.CASCADE,db_column='PAN')

class Request(models.Model):
    urid=models.IntegerField(primary_key=True)
    amount=models.IntegerField()
    FE_info=models.ForeignKey(FarmEntity,on_delete=models.CASCADE,db_column='ufid')
    mandi_info=models.ForeignKey(User_reg,on_delete=models.CASCADE,db_column='PAN')
    current_bid=models.IntegerField()
    before_date=models.DateField()
class Consignment(models.Model):
    ucid=models.IntegerField(primary_key=True)
    req=models.ForeignKey(Request,on_delete=models.CASCADE,db_column='urid')
    prod=models.ForeignKey(Produce,on_delete=models.CASCADE,db_column='upid')
    expected_delivery=models.DateField()
    truck=models.ForeignKey(User_reg,on_delete=models.CASCADE,db_column='PAN')
    cost=models.IntegerField()

##
#Requirements for cacheing
# install memcached for linux
# pip install pymemcache
# run memcached before running the server
##
def AddFarmEntity(mname,mMSP,mMeasured_in):
    exists=FarmEntity.objects.filter(name=mname).count()
    if exists !=0:
        return 'already exists'
    fe=FarmEntity()
    fe.name=mname
    fe.MSP=mMSP
    fe.ufid=uuid.uuid1().int%1000000000
    fe.measured_in=mMeasured_in
    fe.save()

def RegisterUser(mdict):
    client = base.Client(('localhost', 11211))
    try:
        nu=None
        exists=User_reg.objects.filter(phone_number=mdict['phone_number']).count()
        if exists!=0:
            nu=User_reg.objects.get(phone_number=mdict['phone_number'])
            if nu.isVerified:
                return 'fail phone already exists'
        exists=User_reg.objects.filter(PAN=mdict['PAN']).count()
        if exists!=0:
            nu=User_reg.objects.get(PAN=mdict['PAN'])
            if nu.isVerified:
                return 'fail user already exists'
        if nu is None:
            nu=User_reg()
        nu.name=mdict['name']
        nu.phone_number=mdict['phone_number']
        nu.role=int(mdict['role'])
        nu.PAN=mdict['PAN']
        nu.address=mdict['address']
        if nu.role==1:# is Farmer
            pass
        elif nu.role==2:
            nu.vehicle_model=int(mdict['vehicle_model'])
            nu.vehicle_capacity=int(mdict['vehicle_capacity'])
            nu.vehicle_number=mdict['vehicle_number']
            nu.licence_number=mdict['licence_number']
        elif nu.role==3:
            nu.organisation_name=mdict['organisation_name']
        elif nu.role==4:
            nu.bank_account_number=mdict['bank_account_number']
            nu.GST_number=mdict['GST_number']
        else:
            raise ('invalid role')
        nu.isVerified=False
        otp=str(uuid.uuid1().int%1000000)
        print('otp is '+otp)
        client.set(mdict['PAN'],otp,90)
        print(client.get(mdict['PAN']))       
        nu.save()
        return 'success'
    except:
        print ('fail exception occured')
        return 'fail exception occured'

def VerifyUser(mdict):
    client = base.Client(('localhost', 11211))
    otp_sent=client.get(mdict['PAN'])
    otp_sent=otp_sent.decode()
    if otp_sent==None:
        print('timeout')
        return 'timeout'
    otp_recv=mdict['OTP']
    print(type(otp_sent))
    print(type(otp_recv))
    if otp_recv != otp_sent:
        print('wrong otp')
        return ('wrong otp')
    else:
        nu=User_reg.objects.get(PAN=mdict['PAN'])
        nu.isVerified=True
        nu.save()
        print('verification successful')
        return ('verification successful')


def LoginUser(mdict):
    client = base.Client(('localhost', 11211))
    try:
        nu=None
        exists=User_reg.objects.filter(phone_number=mdict['phone_number']).count()
        if exists!=0:
            nu=User_reg.objects.get(phone_number=mdict['phone_number'])
            if nu.isVerified:
                otp=str(uuid.uuid1().int%1000000)
                print('otp is '+otp)
                client.set(mdict['phone_number'],otp,90)
                print(client.get(mdict['phone_number']))
            else:
                print ('user has not been verified')
                return 'failure'
        else:
            return 'no such user exists'       
        return 'success'
    except:
        print ('fail exception occured')
        return 'failure'
        
def VerifyLogin(mdict):
    client = base.Client(('localhost', 11211))
    otp_sent=client.get(mdict['phone_number'])
    otp_sent=otp_sent.decode()
    if otp_sent==None:
        print('timeout')
        return 'timeout'
    otp_recv=mdict['OTP']
    if otp_recv != otp_sent:
        print('wrong otp')
        return ('wrong otp')
    else:
        print('verification successful')
        return User_reg.objects.get(phone_number=mdict[phone_number])


suppliers=[]
categ=None

"""
Consignments will be made by the transportations guys based on information present in the database.
Cleanly define the problem for the transportation in comments before integrating the code. Don't
forget to comment your code 
"""


def verify_response(data,hash, secret_key):
    """
    The function takes in the data , hash value and the secret key to 
    determine if the calculate hash of data with secret key and the 
    provided hash are the same
    """
    return 0

def create_secret(user_information_PAN):
    """
    The function creates a random key and saves it in the database to be 
    used in the next request to verfy the users request.(verify_response()).
    """
    return 0

# Issue #2
def create_produce(amount, FE_info, farmer_info):
    """
    The function creates a new produce object according to the models presented
    in the model.py file. it first checks if the request was made by the farmer.
    """
    try:
        produce = Produce(amount=amount, FE_info=FE_info, farmer_info=farmer_info)
        produce.save()
        print("successfully produce created")
        return "success"
    except:
        print("create produce error")
        return "failure"

# Issue #3
def create_request(amount, FE_info, mandi_info, current_bid, before_date):
    """
    Discuss the due date issue, if there is anything you should change.
    Create the request based on the input received from user, check first
    if the user in a mandi guy.
    """
    try:    
        request = Request(amount = amount, FE_info = FE_info, mandi_info = mandi_info, current_bid = current_bid, before_date = before_date)
        request.save()
        print("successfully request created")
        return "success"
    except:
        print("create request error")
        return "failure"

def list_consignments(user):
    """
    Return all information of the consignment related to this particular user.
    issue #9
    """
    role=user.role
    #if user is farm get his every/top 20 produces and corresponding consignment
    if role == 1:
        produces=Produce.objects.filter(farmer_info=user)
        consignments=[]
        for produce in produces:
            cons=Consignment.objects.get(prod=produce)
            consignments.append(cons)
    elif role==2:
        consignments=Consignment.objects.filter(truck=user)
    elif role==3:
        consignments=[]
        requests=Request.objects.filter(mandi_info=user)
        for requ in requests:
            cons=Consignment.objects.get(req=requ)
            consignments.append(cons)
    return consignments


# Issue #10
def list_20_requests():
    """
    Lists 20 recent requests.
    """
    try:
        list_of_request = Request.objects.all().order_by('urid')[:20]
        print("list of 20 recent request returned")
        return list_of_request
    except:
        print("error getting 20 recents requests")
        return "failure"

def list_request(farm_entity,user):
    """
    List all request related for a given farm entity in decreasing order of profits 
    obtained from the transport. Also list request with possible loss. 
    """





def GiveResponse(msg,number):
    global suppliers
    global categ
    if PhoneUser.objects.filter(phone_number=number).exists():
        p1=PhoneUser.objects.get(phone_number=number)
    else :
        p1=PhoneUser(phone_number=number,
                    name=('User'+number.__str__()),
                    chat_state='0')
        p1.save()
    curstate=p1.chat_state
    msg=msg.lower()
    word=msg.split(' ')
    reply=''
    if curstate == '0':
        if word[0] == 'sell':
            if Categary.objects.filter(name=word[1]).exists():
                categ=Categary.objects.get(name=word[1])
                suppliers=[]
                i=1
                for sellable in Sellable.objects.filter(categary=categ):
                    suppliers.append(sellable)
                    reply=reply+i.__str__()+". Sell at "+sellable.cost.__str__()+' to '+sellable.seller.name+'<br>'
                    i=i+1
                reply=reply+'\nEnter your choice'    
                p1.chat_state='1'
                p1.save()
            else :
                reply= 'No such object is traded here'
        elif word[0] == 'buy':
            print('it came here')
            if Categary.objects.filter(name=word[1]).exists():
                categ=Categary.objects.get(name=word[1])
                reply='How much are you ready to pay \n'+'The MSP for '+categ.name+' is'+categ.MSP.__str__()
                p1.chat_state='2'
                p1.save()
            else :
                reply= 'No such object is traded here'
        else:
            return 'sorry i could not unserstand you'
    elif curstate == '1':
        try:
            selr_num=int(word[0])
        except ValueError:
            reply = "Invalid  number \n What would you like to buy/sell"
            p1.chat_state = '0'
            p1.save()            
            return reply
        if selr_num > len(suppliers):
            reply = 'no such buyer exists '+selr_num.__str__()+" "+len(suppliers).__str__()
        else :
            selr=suppliers[selr_num -1]
            reply = 'You can contact buyer '+selr.seller.name +' using phone number '+selr.seller.phone_number.__str__()
            p1.chat_state = '0'
            p1.save()
    elif curstate == '2':
        try:
            price=int(word[0])
        except ValueError:
            reply = "Invalid  number \n What would you like to buy/sell"
            p1.chat_state = '0'
            p1.save()            
            return reply
        if price < categ.MSP:
            reply ='you cant buy below MSP give a different price'
        else:
            sell_ob=Sellable(cost=price,seller=p1,categary=categ)
            sell_ob.save()
            reply='Details Saved'
            p1.chat_state = '0'
            p1.save() 
    
    return reply
