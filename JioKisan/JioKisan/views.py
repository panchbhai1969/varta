from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from . forms import UserRequest
from . models import *
from . process_text import process_content
from  .voice import *
from trucksFunctions import *
from AssignDelivery import *

def create_dict(data_rec):
    diction = {}
    for val in data_rec:
        if(val['name'] =='' or val['value'] ==''):
            continue
        diction[val['name']] = val['value']
    
    return diction

@csrf_exempt
def new_registration(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
            #print ('Raw Data: "%s"' % str(data_rec) )
    
    response = JsonResponse({'newTheme': "Hey" })
    response['Access-Control-Allow-Origin'] = '*'
    diction = create_dict(data_rec)
    print(diction)
    RegisterUser(diction)
    return response 

@csrf_exempt
def otp_check(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
            #print ('Raw Data: "%s"' % str(data_rec) )
    
    response = JsonResponse({'newTheme': "Hey" })
    response['Access-Control-Allow-Origin'] = '*'
    diction = create_dict(data_rec)
    print(diction)
    VerifyUser(diction)
    return response
@csrf_exempt    
def login(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
            #print ('Raw Data: "%s"' % str(data_rec) )
    
    response = JsonResponse({'newTheme': "Hey" })
    response['Access-Control-Allow-Origin'] = '*'
    diction = create_dict(data_rec)
    print(diction)
    LoginUser(diction)
    return response 

@csrf_exempt
def login_check(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
            #print ('Raw Data: "%s"' % str(data_rec) )

    diction = create_dict(data_rec)
    print(diction)
    ret=VerifyLogin(diction)
    if type(ret)==type('str'):
        response = JsonResponse({'wasSuccess': "false" })
    else:
        mdict=model_to_dict(ret)
        mdict['secret'] = create_secret(mdict)
        mdict['wasSuccess']="true"
        response = JsonResponse(mdict)
    response['Access-Control-Allow-Origin'] = '*'
    return response            

def speechtotext(request):
    if(request.method == 'POST'):
        if 'finalTranscripts' in request.POST:
            textMessage = request.POST['finalTranscripts']
            print(textMessage)
    return render(request, template_name='index.html')


@csrf_exempt  
def voice_input(request):
    """ data_rec = []
    if request.method == 'POST':
        data_rec = json.loads(request.body)
        #print ('Raw Data: "%s"' % str(data_rec) ) 
    diction = create_dict(data_rec)"""
    exists=User_reg.objects.filter(PAN="pan").count()
    if exists!=0:
        user=User_reg.objects.get(PAN="pan")
    else:
        print('User does not exist')
        return 'Failure'
    #Input code for voice input
    input_string = save_images(request) #Return value
    processed_data = process_content(input_string.decode('utf-8'))
    amount = processed_data['quantity']
    FE_info = processed_data['commodity']
    unit = processed_data['unit']
    dict_ = {}
    if(processed_data['request_type'] == 'sell'):
        dict_['amount'] = int(amount)
        # dict['ufid'] = FE_info
        fe = FarmEntity.objects.all()
        for farm_entity in fe:
            if(farm_entity.name == FE_info):
                dict_['ufid'] = farm_entity.ufid
        #Add farmer_info to function call
        dict_['PAN'] = "pan"
        User_reg.objects.get(PAN='pan')
        print(dict_)
        create_produce(dict_)
    elif(processed_data['request_type'] == 'buy'):
        #Call the buy seeds function
        pass
    else:
        print('Invalid request')
    return HttpResponse("Created")
    
@csrf_exempt
def getProduceList(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)
    print(diction)    
    response = JsonResponse(list_produce(diction),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def getFToolList(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    response = JsonResponse(list_ftool(),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def getReqList(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    response = JsonResponse(list_request(diction),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def getFTBuyList(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    response = JsonResponse(list_farm_tools_for_farmers(diction),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response
    
def ResponsePage(request):
    user_request=UserRequest(request.POST or None)
    server_response='Welcome to JioKisan'
    number=5674567311
    if user_request.is_valid():
        msg=user_request.cleaned_data.get('msg')
        if msg != '':
            server_response=GiveResponse(msg,number)
        # some_data_to_dump = {'some_var_1': msg
        # }
        # data = json.dumps(some_data_to_dump)
        # return HttpResponse(data, content_type='application/json')
        # some_data_to_dump = {'some_var_1': msg
        # }
        # data = json.dumpscount(some_data_to_dump)
        # return HttpResponse(data, content_type='application/json')
    context={
            'msg_response': server_response,
            'form':user_request
        }
    return render(request,template_name='message.html',context=context)

@csrf_exempt
def getDriverInfo(request):
    data_rec =[]
    if request.method == 'POST':
        data_rec = json.loads(request.body)
    mDict = create_dict(data_rec)

    return getDriverDetails(mDict)

@csrf_exempt
def getDriverPath(request):
    data_rec =[]
    if request.method == 'POST':
        data_rec = json.loads(request.body)
    mDict = create_dict(data_rec)
    print('Hai hai mDict \n\n', mDict)
    path = getPath(mDict)
    json_path = JsonResponse(path, safe=False)
    json_path['Access-Control-Allow-Origin'] = '*'

    return json_path
    
@csrf_exempt   
def list_farmEnitity(request):
    fe=FarmEntity.objects.filter(isFarmTool=False)
    f_list=[]
    for f in fe:
        f_dict={}
        f_dict['name']=f.name
        f_dict['ufid']=f.ufid
        f_list.append(f_dict)
    f_list
    response = JsonResponse(f_list,safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt   
def addFtoMConsignment(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    response = JsonResponse(create_consignments(diction),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt   
def addFTStoFConsignment(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    prod=Produce.objects.get(upid=diction['upid'])
    farmer=User_reg.objects.get(PAN=diction['PAN'])
    dummy_req=Request()              # A dummy request required for consignment 
    dummy_req.mandi_info=farmer      # coz farmer is the buyer in this case
    dummy_req.current_bid=1          # random value ... will be replaced
    dummy_req.amount=1               # does not matter
    dummy_req.before_date=datetime.datetime.today()
    del_cost,exp_del_date=getDeliveryInfo(dummy_req,prod)
    dummy_req.current_bid=del_cost+prod.price       #now giving some values
    dummy_req.before_date=exp_del_date              #that make sense
    dummy_req.FE_info=prod.FE_info
    dummy_req.save()
    create_consignments({'urid':dummy_req.urid,'upid':prod.upid})
    response = JsonResponse(create_consignments(diction),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt   
def getPastConsignment(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    response = JsonResponse(list_past_consignment(diction),safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def list_farmTool(request):
    fe=FarmEntity.objects.filter(isFarmTool=True)
    f_list=[]
    for f in fe:
        f_dict={}
        f_dict['name']=f.name
        f_dict['ufid']=f.ufid
        f_list.append(f_dict)
    response = JsonResponse(f_list,safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def add_farmTool(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    ftool=Produce()
    ftool.FE_info=FarmEntity.objects.get(ufid=int(diction['ufid']))
    ftool.isAssigned=False
    ftool.farmer_info=User_reg.objects.get(PAN=diction['PAN'])
    ftool.price=int(diction['price'])
    ftool.amount=int(diction['amount'])
    ftool.save()
    response = JsonResponse(model_to_dict(ftool))
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def add_farmProd(request):
    data_rec = []
    if request.method == 'POST':
            data_rec = json.loads(request.body)
    diction = create_dict(data_rec)    
    print(diction)
    fprod=Produce()
    fprod.FE_info=FarmEntity.objects.get(ufid=int(diction['ufid']))
    fprod.isAssigned=False
    fprod.farmer_info=User_reg.objects.get(PAN=diction['PAN'])
    fprod.amount=int(diction['amount'])
    fprod.save()
    response = JsonResponse(model_to_dict(fprod))
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def getHired(request):
    data_rec =[]
    if request.method == 'POST':
        data_rec = json.loads(request.body)
    mDict = create_dict(data_rec)
    user = User_reg.objects.get(PAN=mDict['PAN'])
    if user.role==2 and user.isHired == False : 
        print('Hai Hai Hai \n\n')
        mapConsignments(mDict)
        print('LOl lol lol \n\n')
    return getDriverPath(request)

    
def updateDeliveryStatus(request):
    data_rec =[]
    if request.method == 'POST':
        data_rec = json.loads(request.body)
    mDict = create_dict(data_rec)
    print("Printing mDIct : \n\n")
    print(mDict)
    print('\n\n')
    