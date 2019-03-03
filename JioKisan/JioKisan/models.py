from django.db import models
import uuid
from django.utils import dateparse
from pymemcache.client import base
import hmac
import hashlib
import base64
from faker import Faker
from faker.providers import *
import datetime
from django.forms.models import model_to_dict

ROLE_CHOICES = {
    1: "farmer",
    2: "truck_driver",
    3: "mandi",
    4: "farm_tool_sellers"
}
VEHICLE_MODELS= {
    0:'AC',
    1:'NON AC'
}
MEASUREMENT_TYPES = {
    1:'KG',
    2:'METRIC TON',
    3:'DOZENS',
    4:'LITRES'
}

STATUS_CHOICES = (
    ("PENDING","Pending"),
    ("TRANSIT","Transit"),
    ("COMPLETED", "Completed")
)

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
    #only for truck driver
    isHired=models.BooleanField(default=None, blank=True, null=True)
 # Syntax of path :         farmEntity?status>purpose:pk of consignment;latitude,logitude|status>purpose:pk of consignment;latitude,logitude|...
    path=models.TextField(default=None, blank=True, null=True)
    available_capacity=models.IntegerField(default=None, blank=True, null=True)
    current_address=models.CharField(max_length=40,default=None, blank=True, null=True)
    #only for truck driver
    position_latitude=models.FloatField(default=None, blank=True, null=True)
    position_longitude=models.FloatField(default=None, blank=True, null=True)
    isVerified=models.BooleanField()
    def __str__(self):
        return (self.name +" "+ self.PAN)


class FarmEntity(models.Model):
    ufid = models.AutoField(primary_key=True)
    name =models.CharField(max_length=40)
    measured_in=models.IntegerField()
    MSP=models.IntegerField()
    isFarmTool=models.BooleanField(default=False)
    display_image=models.ImageField(upload_to='fe_sample_images',blank=True)
    def __str__(self):
        return (self.name +" "+ str(self.ufid))

class Produce(models.Model):
    upid=models.AutoField(primary_key=True)
    amount=models.IntegerField()
    price=models.IntegerField(default=None,blank=True,null=True)
    FE_info=models.ForeignKey(FarmEntity,on_delete=models.CASCADE,db_column='ufid')
    farmer_info=models.ForeignKey(User_reg,on_delete=models.CASCADE,db_column='PAN')
    isAssigned=models.BooleanField(default=False)
    def __str__(self):
        return (self.FE_info.name +" by "+self.farmer_info.name+" "+ str(self.upid))

class Request(models.Model):
    urid=models.AutoField(primary_key=True)
    amount=models.IntegerField()
    FE_info=models.ForeignKey(FarmEntity,on_delete=models.CASCADE,db_column='ufid')
    mandi_info=models.ForeignKey(User_reg,on_delete=models.CASCADE,db_column='PAN')
    isAssigned=models.BooleanField(default=False)
    current_bid=models.IntegerField()
    before_date=models.DateField()
    def __str__(self):
        return (self.FE_info.name +" by "+self.mandi_info.name+" "+ str(self.urid))

class Consignment(models.Model):
    ucid=models.AutoField(primary_key=True)
    req=models.ForeignKey(Request,on_delete=models.CASCADE,db_column='urid')
    prod=models.ForeignKey(Produce,on_delete=models.CASCADE,db_column='upid')
    expected_delivery=models.DateField()
    status=models.CharField(max_length=25,choices=STATUS_CHOICES,default='PENDING')
    truck=models.ForeignKey(User_reg,on_delete=models.CASCADE,db_column='PAN',default=None, blank=True, null=True)
    cost=models.IntegerField()
    # def __str__(self):
    #     return (self.FE_info.name +" to "+self.farmer_info.name" "+ self.upid)

##
#Requirements for cacheing
# install memcached for linux
# pip install pymemcache
# run memcached before running the server
##

def getPositionCoordinates(address):
    fakegen = Faker()
    fakegen.add_provider(geo)
    location = fakegen.local_latlng(country_code="IN", coords_only=False)

    return location[0], location[1]

def getDeliveryInfo(mrequest,mproduce):
    cost=40
    fakegen = Faker()
    cdate = datetime.date.today()
    bdate = (mrequest.before_date)
    edate = fakegen.date_between_dates(date_start=cdate, date_end=bdate)
    return (cost,edate)

def AddFarmEntity(mname,mMSP,mMeasured_in):
    exists=FarmEntity.objects.filter(name=mname).count()
    if exists !=0:
        return 'already exists'
    fe=FarmEntity()
    fe.name=mname
    fe.MSP=mMSP
    fe.measured_in=mMeasured_in
    fe.save()


def RegisterUser(mdict):
    client = base.Client(('localhost', 11211))
    #try:
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
    nu.position_latitude, nu.position_longitude = getPositionCoordinates(nu.address)
    if nu.role==1:# is Farmer
        pass
    elif nu.role==2:
        nu.vehicle_model=(int(mdict['vehicle_model'])%2)
        nu.vehicle_capacity=int(mdict['vehicle_capacity'])
        nu.vehicle_number=mdict['vehicle_number']
        nu.licence_number=mdict['licence_number']
        nu.available_capacity=mdict['vehicle_capacity']
        nu.isHired=False
        nu.current_address=mdict['address']
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
    #except:
    #    print ('fail exception occured')
    #    return 'fail exception occured'


def VerifyUser(mdict):
    client = base.Client(('localhost', 11211))
    otp_sent=client.get(mdict['PAN'])
    if otp_sent==None:
        print('timeout')
        return 'timeout'
    otp_sent=otp_sent.decode()
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
    if otp_sent==None:
        print('timeout')
        return 'timeout'
    otp_sent=otp_sent.decode()
    otp_recv=mdict['OTP']
    if otp_recv != otp_sent:
        print('wrong otp')
        return ('wrong otp')
    else:
        print('verification successful')
        return User_reg.objects.get(phone_number=mdict['phone_number'])


suppliers=[]
categ=None

"""
Consignments will be made by the transportations guys based on information present in the database.
Cleanly define the problem for the transportation in comments before integrating the code. Don't
forget to comment your code 
"""


def verify_response(mdict,data,hash_rec):
    """
    The function takes in the data , hash value and the secret key to 
    determine if the calculate hash of data with secret key and the 
    provided hash are the same
    """
    client = base.Client(('localhost', 11211))
    secret=client.get(mdict['phone_number'])
    if secret==None:
        print('timeout')
        return False
    secret=secret.decode()
    otp_recv=mdict['OTP']
    if otp_recv != secret:
        print('wrong otp')
        return False
    else:
        d = hmac.new(secret.encode(),data.encode(),hashlib.sha256)
        hash_val = base64.b64encode(d.digest()).decode()
        if(hash_val == hash_rec):
            return True
        else:
            return False
    return 0

def create_secret(mdict):
    """
    The function creates a random key and saves it in the database to be 
    used in the next request to verfy the users request.(verify_response()).
    """
    client = base.Client(('localhost', 11211))
    try:
        nu=None
        exists=User_reg.objects.filter(phone_number=mdict['phone_number']).count()
        if exists!=0:
            nu=User_reg.objects.get(phone_number=mdict['phone_number'])
            if nu.isVerified:
                secret=str(uuid.uuid1().int%1000000)
                print('otp is '+secret)
                client.set(mdict['phone_number'],secret,90)
                print(client.get(mdict['phone_number']))
            else:
                print ('user has not been verified')
                return 'failure'
        else:
            return 'no such user exists'       
        return secret
    except:
        print ('fail exception occured')
        return 'failure'
    return 0

# Issue #2
def create_produce(mdict):
    """
    The function creates a new produce object according to the models presented
    in the model.py file. it first checks if the request was made by the farmer.
    """

    produce = Produce()
    produce.amount=int(mdict['amount'])
    produce.FE_info=FarmEntity.objects.get(ufid=int(mdict['ufid']))
    produce.farmer_info=User_reg.objects.get(PAN=mdict['PAN'])
    produce.save()
    print("successfully produce created")
    return "success"


# Issue #3
def create_request(mdict):
    """
    Discuss the due date issue, if there is anything you should change.
    Create the request based on the input received from user, check first
    if the user in a mandi guy.
    """
    try:
        request = Request()
        request.amount=int(mdict['amount'])
        request.FE_info=FarmEntity.objects.get(ufid=mdict['ufid'])
        request.mandi_info=User_reg.objects.get(PAN=mdict['PAN'])
        request.current_bid=int(mdict['current_bid'])
        request.before_date=dateparse(mdict['before_date'])
        request.save()
        print("successfully produce created")
        return "success"
    except:
        print("create produce error")
        return "failure"

def create_consignments(mdict):
    cons=Consignment()
    cons.status='PENDING'
    cons.req=Request.objects.get(urid=mdict['urid'])
    cons.prod=Produce.objects.get(upid=mdict['upid'])
    cons.truck=None
    cons.cost,cons.expected_delivery=getDeliveryInfo(cons.req,cons.prod)
    cons.req.isAssigned=True
    cons.prod.isAssigned=True
    cons.req.save()
    cons.prod.save()
    cons.save()  
    return {'ucid':cons.ucid}



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

def list_request(mdict):
    """
    List all request related for a given farm entity in decreasing order of profits 
    obtained from the transport. Also list request with possible loss. 
    """
    prod=Produce.objects.get(upid=mdict['upid'])
    farm_entity=prod.FE_info
    reqs=Request.objects.filter(isAssigned=False,FE_info=farm_entity)
    farmer=User_reg.objects.get(PAN=mdict['PAN'])
    ret_reqs=[]
    for req in reqs:
        r_dict={}
        cost,del_date=getDeliveryInfo(req,prod)
        if del_date > req.before_date:
            pass
        else:
            r_dict=model_to_dict(req)
            r_dict['delivery_cost']=cost
            r_dict['expected_delivery']=del_date
            r_dict['final_price']=req.current_bid-cost
            r_dict['mandi_name']=req.mandi_info.organisation_name
            r_dict['upid']=prod.upid
            ret_reqs.append(r_dict)
    ret_reqs_sorted=sorted(ret_reqs,key= lambda req: req['final_price'],reverse=True )
    return ret_reqs_sorted

def list_farm_tools_for_farmers(mdict):
    """
    List all request related for a given farm entity in decreasing order of profits 
    obtained from the transport. Also list request with possible loss. 
    """
    ft=FarmEntity.objects.get(ufid=mdict['ufid']) #ft for farm tool
    produces=Produce.objects.filter(FE_info=ft,isAssigned=False)
    farmer=User_reg.objects.get(PAN=mdict['PAN'])
    #some workaround since farmer is the buyer in this case
    #different selling model but using the same function
    req=Request()
    req.mandi_info=farmer
    req.current_bid=0 ##value doesnt matter here just to get delivery costs
    req.amount=1 ##value doesnt matter here just to get delivery costs
    req.before_date=datetime.datetime.today()##value doesnt matter here just to get delivery costs
    ret_produces=[]
    for  prod in produces:
        p_dict={}
        cost,del_date=getDeliveryInfo(req,prod)
        p_dict=model_to_dict(prod)
        p_dict['seller_name']=prod.farmer_info.name #in this case farmer info contains ft seller
        p_dict['expected_delivery']=del_date
        p_dict['final_price']=prod.price+cost
        p_dict['seller_pan']=prod.farmer_info.PAN
        ret_produces.append(p_dict)
    ret_prods_sorted=sorted(ret_produces,key= lambda req: req['final_price'] )
    print(ret_prods_sorted)
    return ret_prods_sorted
        
            

def list_produce(mdict):
    farmer=User_reg.objects.get(PAN=mdict['PAN'])
    produce_list=[]
    produces=Produce.objects.filter(isAssigned=False,farmer_info=farmer)
    for prod in produces:
        p_dict=model_to_dict(prod)
        p_dict['FE_name']=prod.FE_info.name
        p_dict['img_url']=prod.FE_info.display_image.url
        produce_list.append(p_dict)
    print(produce_list)
    return produce_list

def list_ftool():
    tool_entities=FarmEntity.objects.filter(isFarmTool=True)
    tool_list=[]
    for tools in tool_entities:
        t_dict={}
        t_dict['name']=tools.name
        t_dict['price']=tools.MSP
        t_dict['ufid']=tools.ufid
        t_dict['img_url']=tools.display_image.url
        tool_list.append(t_dict)
    print(tool_list)
    return tool_list
