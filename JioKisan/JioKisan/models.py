from django.db import models
####### states
# 0  first msg
# 1  Buyers available
# 
# 2  buying price
#   
#
#######

class PhoneUser(models.Model):
    phone_number=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=40)
    chat_state=models.CharField(max_length=10)

class Categary(models.Model):
    name=models.CharField(max_length=40,primary_key=True)
    MSP=models.IntegerField()
    cid=models.IntegerField(default=5)
class Sellable(models.Model):
    cost=models.IntegerField()
    seller=models.ForeignKey(PhoneUser,on_delete=models.CASCADE,db_column='phone_number')
    categary=models.ForeignKey(Categary,on_delete=models.CASCADE,db_column='cid')

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
