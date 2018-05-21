from django.shortcuts import render, HttpResponse, redirect
import random, datetime
from datetime import datetime, time, date

def index(request):
    if 'yourGold' not in request.session and 'newGold' not in request.session:
        request.session['yourGold'] = 0
        request.session['newGold'] = 0
    return render(request, "ninja/index.html")

def process_money(request):
    time = datetime.now()
    now = time.strftime("%B %d, %Y %H:%M:%S")
    if 'activityLog' not in request.session:
        request.session['activityLog'] = []
    if request.POST['location'] == "farm":
        request.session['newGold'] = random.randint(10,20)
        request.session['activityLog'].insert(0, "<p style='color:green;'>You visited the farm and collected " + str(request.session['newGold']) + " gold. (" + now + ")</p>")
    if request.POST['location'] == "cave":
        request.session['newGold'] = random.randint(5,10)
        request.session['activityLog'].insert(0, "<p style='color:green;'>You visited the cave and collected " + str(request.session['newGold']) + " gold. (" + now + ")</p>")
    if request.POST['location'] == "house":
        request.session['newGold'] = random.randint(2,5)
        request.session['activityLog'].insert(0, "<p style='color:green;'>You visited the house and collected " + str(request.session['newGold']) + " gold. (" + now + ")</p>")
    if request.POST['location'] == "casino":
        if request.session['yourGold'] < 50:
            request.session['activityLog'].insert(0, "<p>You're too poor to gamble. (" + now + ")</p>")
            request.session['newGold'] = 0
        else:
            request.session['newGold'] = random.randint(-50,50)
            if request.session['newGold'] == 0:
                request.session['activityLog'].insert(0, "<p style='color:green;'>You visited the casino and broke even. (" + now + ")</p>")
            elif request.session['newGold'] > 0:
                request.session['activityLog'].insert(0, "<p style='color:green;'>You visited the casino and won " + str(request.session['newGold']) + " gold. (" + now + ")</p>")
            elif request.session['newGold'] < 0:
                request.session['activityLog'].insert(0, "<p style='color:red;'>You visited the casino and lost " + str(-request.session['newGold']) + " gold. (" + now + ")</p>")
    request.session['yourGold'] += request.session['newGold']
    if request.POST['location'] == "start_over":
        request.session.clear()
    return redirect('/')