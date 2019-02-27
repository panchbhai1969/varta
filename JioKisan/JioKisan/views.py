from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from . forms import UserRequest
from . models import *
from . process_text import process_content

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
    
def voice_input(request):
    data_rec = []
    
    if request.method == 'POST':
        data_rec = json.loads(request.body)
        #print ('Raw Data: "%s"' % str(data_rec) )
    diction = create_dict(data_rec)
    exists=User_reg.objects.filter(PAN=diction['PAN']).count()
        if exists!=0:
            user=User_reg.objects.get(PAN=mdict['PAN'])
        else:
            print('User does not exist')
            return 'Failure'
    #Input code for voice input
    input_string = 'I want to sell two hundred kilo carrots' #Return value
    processed_data = process_content(input_string)
    amount = processed_data['quantity']
    FE_info = processed_data['commodity']
    unit = process_data['unit']
    if(processed_data['request_type'] == 'sell'):
        #Add farmer_info to function call
        create_produce(amount, FE_info, user)
    elif(processed_data['request_type'] == 'buy'):
        #Call the buy seeds function
        continue
    else:
        print('Invalid request')