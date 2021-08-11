from django.shortcuts import render
from .models import Config

#imported sawopy
from sawo import createTemplate,getContext,verifyToken
import json
from django.http import HttpResponse

#test classverifyToken
load = ''
loaded = 0


createTemplate("templates/partials") #location name for partial file creation

def index(request):
    config = Config.objects.order_by('-api_key')[:1]
    setLoaded()
    setPayload(load if loaded<2 else '')
    context = {"sawo":getContext(config,"main/recive") if(config) else {},"load":load,"title":"Home"} # getContext(config,"main/recive")
    return render(request,"index.html",context)

def recive(request):
    if request.method == 'POST':
        payload = json.loads(request.body)["payload"]
        print("*"*50)
        print(payload)
        setLoaded(True)
        setPayload(payload)
        print(load)
        print("*"*50)
        status = 200 if verifyToken(payload) else 404
        response_data = {"status":status}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def setPayload(payload):
    global load
    load = payload
def setLoaded(reset=False):
    global loaded
    if reset:
        loaded=0
    else:
        loaded+=1