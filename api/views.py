from pathlib import Path
from django.shortcuts import render
from openai import OpenAI
import json
from fsary.settings import API_KEY_OPENAI, STANDARD_SIZE_GENERATE, IMAGE_MODEL, BASE_DIR, MEDIA_ROOT, MEDIA_URL
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import uuid
from django.views.decorators.csrf import csrf_protect

# Create your views here.

opnai = OpenAI(api_key=API_KEY_OPENAI)

@csrf_exempt
def index(request):
    return JsonResponse({"message":'hello'})

@csrf_exempt
def chat(request):
    
    if request.method=="POST":
        data = json.loads(request.body)
        text = data.get('content')

        res = opnai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"user","content":text},
            ]
        )
        result = str(res.choices[0].message.content)
        #print(result)
        return JsonResponse({"answer": result})

    return JsonResponse({"error": "wdym?"}, status=405)




@csrf_exempt
def gen_image(request):

    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get('prompt')
        res = opnai.images.generate(
            model=IMAGE_MODEL,
            n=1,
            prompt=prompt,
            size=STANDARD_SIZE_GENERATE)
        return JsonResponse({"image": res.data[0].url})
    
    return JsonResponse({"error": "seriously wdym?"}, status=405)


@csrf_exempt
def tts(request):

    if request.method == "POST":
        data = json.loads(request.body)
        txt = data.get('txt')
        if len(txt)>200:
            return JsonResponse({"error":"toomanysymbol"},status=400) # too many abcdef(symbol) 
            # 400 Bad Request

        speech_file_path = Path(MEDIA_ROOT) / f"s{uuid.uuid4()}.mp3"
        res =  opnai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=txt
        )
        res.stream_to_file(speech_file_path)
        
        media_url = MEDIA_URL
        speech_file_url = f"{media_url}{speech_file_path.name}"
        print(speech_file_url)
        return JsonResponse({"mp3": speech_file_url})

    return JsonResponse({"error": "HELLO?!(ROBOTIC) wdym?"}, status=405)


