from django.db import models
import uuid

STATUS_CHOICES = {
    1:"Farmer",
    2: "Truck drivers",
    3: "Mandis",
    4: "Farm tool Sellers"
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
    address = models.CharField(max_length=100,)
    PAN = models.CharField(max_length=10,primary_key=True)
    license_number=models.CharField(max_length=20)
    vehicle_number=models.CharField(max_length=20)
    vehicle_model=models.IntegerField()
    vehicle_capacity=models.IntegerField()
    organisation_name=models.CharField(max_length=80)
    bank_account_number=models.CharField(max_length=20)

class FarmEntity(models.Model):
    ufid = models.IntegerField(primary_key=True)
    name =models.CharField(max_length=40,unique=True)
    measured_in=models.IntegerField()
    MSP=models.IntegerField()

class  Produce(models.Model):
    upid=models.IntegerField(primary_key=True)
    amount=models.IntegerField()
    FE_info=models.ForeignKey(FarmEntity,on_delete=models.CASCADE)
    farmer_info=models.ForeignKey(User_reg,on_delete=models.CASCADE)

class Request(models.Model):
    urid=models.IntegerField(primary_key=True)
    amount=models.IntegerField()
    FE_info=models.ForeignKey(FarmEntity,on_delete=models.CASCADE)
    mandi_info=models.ForeignKey(User_reg,on_delete=models.CASCADE)
    current_bid=models.IntegerField()
    before_date=models.DateField()
class Consignment(models.Model):
    ucid=models.IntegerField(primary_key=True)
    req=models.ForeignKey(Request,on_delete=models.CASCADE)
    prod=models.ForeignKey(Produce,on_delete=models.CASCADE)
    expected_delivery=models.DateField()
    truck=models.ForeignKey(User_reg,on_delete=models.CASCADE)
    cost=models.IntegerField()

def AddFarmEntity(mname,mMSP,mMeasured_in):
    exists=FarmEntity.objects.filter(name=mname).count()
    if exists !=0:
        return 'already exists'
    fe=FarmEntity()
    fe.name=mname
    fe.ufid=uuid
    fe.MSP=mMSP
    fe.measured_in=mMeasured_in
    fe.save()



suppliers=[]
categ=None




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
