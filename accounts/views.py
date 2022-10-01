from email import message
from pickletools import read_string4

from tkinter.tix import Form
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from platformdirs import user_config_dir
from . forms import UserRegistrationForm, EditProfileForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . models import Message, UserProfile
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
from django.utils.functional import SimpleLazyObject 




# Create your views here.
def home(request):
    return render(request, 'accounts/base.html')




def register_request(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = UserRegistrationForm()
	return render (request=request, template_name="registration/signup.html", context={"register_form":form})

def inbox(request):
	
	messages = Message.get_message(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipent=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		'profile': profile,
		}

	template = loader.get_template('accounts/inbox.html')

	return HttpResponse(template.render(context, request))


@login_required
def Directs(request, username):
	user = request.user
	users = User.objects.all()
	
	messages = Message.get_message(user=user)
	profile= UserProfile.objects.get(user=user)
	active_direct= username
	directs = Message.objects.filter(user=user, recipent__username=username)
	directs.update(is_read=True)
	
	

	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
		'profile': profile,
		'users': users,
		
			
	}

	template = loader.get_template('accounts/cht.html')

	return HttpResponse(template.render(context, request))

	



@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))
	

		
		paginator = Paginator(users, 1)
		
		
		page_number = request.GET.get('page')
	

		
		users_paginator = paginator.get_page(page_number)

		
		context = {
				'users': users_paginator,
				
				
				}
	
	template = loader.get_template('accounts/SMALL.html')
	
	return HttpResponse(template.render(context, request))



@login_required
def NewConversation(request, username):
	from_user = request.user
	body = 'Hello'
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('search')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')

@login_required
def SendDirect(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method=='POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user,body)
		
		
	
	return redirect('direct', username=str(to_user_username))	


def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}

@login_required
def profile(request, username):
	
	user = get_object_or_404(User, username=username)
	profile = UserProfile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	context = {
		'profile': profile,
		'url_name':url_name,
	}
	return render(request, 'accounts/profile.html', context )

@login_required
def EditProfile(request):
	user = request.user.id
	profile = UserProfile.objects.get(user__id=user)
	BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.profile_Picture = form.cleaned_data.get('profile_Picture')
			profile.Bio = form.cleaned_data.get('Bio')
			profile.save()
			return redirect('home')
	else:
		form = EditProfileForm()

	context = {
			'form':form,
	}

	return render(request, 'accounts/newprofile.html', context)

def ajax_posting(request):
    if request.is_ajax():
        message = request.POST.get('message', None) # getting data from first_name input 
        if message: #cheking if first_name and last_name have value
            response = {
                         'msg':'Your form has been submitted successfully' # response message
            }
            return JsonResponse(response) # return response as JSON
