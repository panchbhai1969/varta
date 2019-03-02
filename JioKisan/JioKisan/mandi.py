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

@csrf_exempt   
def list_farmEnitity(request):
    fe=FarmEntity.objects.filter(isFarmTool=False)
    f_list=[]
    for f in fe:
        f_list.append(model_to_dict(f))
    f_list
    response = JsonResponse(f_list,safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response

@csrf_exempt
def list_farmTool(request):
    fe=FarmEntity.objects.filter(isFarmTool=True)
    f_list=[]
    for f in fe:
        f_list.append(model_to_dict(f))
    response = JsonResponse(f_list,safe=False)
    response['Access-Control-Allow-Origin'] = '*'
    print(response)
    return  response