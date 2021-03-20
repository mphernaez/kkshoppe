from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate

from django.http import JsonResponse, HttpResponseRedirect

from common.utils import json_response, get_general_context

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')

    context = {}
    try:
        context = request.session['context']
    except:
        print('there is no context for index')
    return render(request, 'main/login.html', context)

def user_login(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/dashboard')
    else:
        context = {
            "error": "Incorrect username or password"
        }
        request.session['context'] = context
        return redirect('/')
        # return json_response("Username or password is incorrect.", 401)

def user_logout(request):
    logout(request)
    return redirect('/')

def dashboard(request):
    return render(request, 'main/dashboard.html', get_general_context(request))



