import io
import os
from django import forms
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
class UploadImageForm(forms.Form):
    image = forms.ImageField()

@csrf_exempt
def save_images(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save("7440934465"+".wav", myfile)
        uploaded_file_url = fs.url(filename)
        return v_tex_trans(uploaded_file_url[1:] )
    

def v_tex_trans(location):
    # Instantiates a client
    GOOGLE_APPLICATION_CREDENTIALS = "secret.json"
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = location
    print(file_name)
    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz= 44100,
        language_code='hi-IN')


    # Detects speech in the audio file
    response = client.recognize(config, audio)

    accum = []
    for result in response.results:
        accum.append(result.alternatives[0].transcript)
    accum= " ".join(accum)
    #print(accum.encode())

    # Imports the Google Cloud client library
    from google.cloud import translate

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    text = accum
    # The target language
    target = 'en'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))
    #str_val  =  translation['translatedText'].encode()
    print (translation['translatedText'].encode('utf-8').strip())
    return translation['translatedText'].encode('utf-8').strip()
