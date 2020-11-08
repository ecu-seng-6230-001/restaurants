from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
from .forms import (
	AccountRegistration, DivErrorList,
	AccountLogin, PasswordChange
)
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required
from random import randint
from general.functions import getUsername, getRandomCode, valid_name
from informations.models import City
from reviews.models import Review
from foods.models import Food
from restaurants.models import Restaurant
from orders.models import Order


@login_required
def delete_view(request):
	template_name = 'accounts/delete-account.html'
	try:
		account = Account.objects.get(pk=request.user.pk)
	except:
		messages.warning(request, 'Account is not found!')
		return HttpResponseRedirect('/404notfound/')

	if request.is_ajax():
		password = request.POST['password']
		if account.check_password(raw_password=password):
			msg = 'yes'
		else:
			msg = "no"
		return HttpResponse(msg)

	if request.method == 'POST':
		if request.POST['confirm_delete'] == '1':
			logout(request)
			account.delete()
			messages.success(request, "Your account has been terminated.")
			return HttpResponseRedirect('/')
	contex = {

	}
	return render(request, template_name, contex)

@login_required
def changePassword_view(request):
	user = Account.objects.get(username=request.user.username)
	form = PasswordChange(user, request.POST or None)
	template_name = 'accounts/change-password.html'
	if form.is_valid():
		new_password = form.cleaned_data.get('new_password')
		user.set_password(raw_password=new_password)
		user.save()
		logout(request)
		user = authenticate(request, username=user.username, password=new_password)
		login(request, user)
		messages.success(request, "New password has been updated successfully.")
		return HttpResponseRedirect("/accounts/change-password/")

	contex = {
		'form': form
	}
	return render(request, template_name, contex)


def settings_view(request, pk):
	account = get_object_or_404(Account, pk=pk)
	if request.user != account or not request.is_ajax() or request.method != "POST":
		return HttpResponseRedirect("/404notfound/")
	template_name = 'accounts/__include/settings.html'
	contex = {
		'account': account
		#'active_settings': 'active',
	}
	return render(request, template_name, contex)


def orders_view(request, pk):
	if not request.is_ajax() or request.method != "POST" or request.user.username != username:
		return HttpResponseRedirect("/404notfound/")

	template_name = 'accounts/__include/orders.html'
	try:
		account= User.objects.get(pk=pk)
	except:
		return HttpResponseRedirect("/404notfound/")
	contex = {
		'orders': Order.objects.all().filter(account=account).filter(is_active=True)
	}
	return render(request, template_name, contex)


def reviews_view(request, pk):
	if not request.is_ajax() or request.method != "POST":
		return HttpResponseRedirect("/404notfound/")
	template_name = 'accounts/__include/reviews.html'
	try:
		account = Account.objects.get(pk=pk)
	except:
		return HttpResponseRedirect("/404notfound/")
	contex = {
		'reviews': Review.objects.all().filter(account=account),
		#'active_reviews': 'active',
	}
	return render(request, template_name, contex)


def favourites_view(request, pk):
	if not request.is_ajax() or request.method != "POST":
		return HttpResponseRedirect("/404notfound/")

	template_name = 'accounts/__include/favs.html'
	account = get_object_or_404(Account, pk=int(pk))

	contex = {
		'foods': Food.objects.all().filter(account=account),
		'restaurants': Restaurant.objects.all().filter(account=account),
		#'active_favourites': 'active'
	}
	return render(request, template_name, contex)



def profile_view(request, pk):
	template_name = 'accounts/profile.html'
	account = get_object_or_404(Account, pk=int(pk))

	contex = {
		'account': account,
		'cities': {"Greenville", "Winterville", "Ayden", "Kinston"},
		'selected': account.city,
		#'active_profile': 'active',
	}

	if request.is_ajax() and request.method == "POST":
		return render(request, "accounts/__include/__profile.html", contex)
	return render(request, template_name, contex)




def login_view(request):
	next = request.GET.get('next', '/')
	if request.user.is_authenticated:
		messages.success(request, "You are already logged in!")
		return HttpResponseRedirect(next)
	template_name = 'accounts/login.html'
	form 		  = AccountLogin(request.POST or None, auto_id=False)
	if form.is_valid():
		print(form.cleaned_data.get('username'))
		user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
		login(request, user)
		messages.success(request, "You are successfully logged in.")
		return HttpResponseRedirect(next)
	contex = {
		'form': form
	}
	return render(request, template_name, contex)


@login_required
def logout_view(request):
	next = request.GET.get('next', '/')
	if request.user.is_authenticated:
		logout(request)
		messages.success(request, "You have been logged out!")
	return HttpResponseRedirect(next)



def register_view(request):
	if request.user.is_authenticated:
		messages.warning(request, "Please, sign out first then register.")
		return HttpResponseRedirect('/')
	next = request.GET.get('next', '/')
	template_name = 'accounts/register.html'
	form 		  = AccountRegistration(request.POST or None, auto_id=False, error_class=DivErrorList)
	if request.method == "POST":
		if form.is_valid():
			account = Account()
			account.username = getUsername(form.cleaned_data.get('name'))
			account.set_password(raw_password=form.cleaned_data.get('password'))
			account.name = form.cleaned_data.get('name')
			account.save()
			auth_user = authenticate(request, username=account.username, password=form.cleaned_data.get('password'))
			login(request, auth_user)
			messages.success(request, 'Hey, ' + account.username + '! your account has been created successfully. Please check your inbox to <a href="/accounts/activate/" class="alert-link">confirm your account</a>.')
			return HttpResponseRedirect(next)
	contex = {
		'form': form
	}
	return render(request, template_name, contex)


@login_required
def activate_view(request):
	template_name = 'accounts/activate.html'
	account = Account.objects.get(username=request.user.username)
	if account.is_active == True:
		messages.success(request, "You account is already activated.")
		return HttpResponseRedirect('/accounts/'+account.username+'/')

	# Response to ajax request
	if request.is_ajax() and request.method == "POST":
		code = request.POST['code']
		if account.activation_code == code:
			account.is_active = True
			account.save()
			return JsonResponse({'msg': "Congrats! Your account is activated now."})
		else:
			if len(code) == 0:
				return JsonResponse({'msg': "Please enter the code."})
			return JsonResponse({'msg': "Code didn't match."})
		# if re_code then resend code

	contex = {'account': account}
	return render(request, template_name, contex)




def sendCode_view(request):
	msg = ''
	if request.user.is_authenticated and request.is_ajax() and request.method == "POST":
		account = get_object_or_404(Account, user=request.user)
		if account.is_active == False:
			account.activation_code = getRandomCode()
			account.save()
			msg = 'New code has been sent. It normally takes 1~5 mins. to receive a code.'
		else:
			msg = 'Account is already registered.'
	else:
		msg = 'Bad request.'
	return JsonResponse({'msg': msg})





@login_required
def updateBasicInfo(request):
	msg    = ''
	signal = 'success'
	if request.is_ajax() and request.method == "POST":
		account = Account.objects.get(username=request.user.username)
		name    = request.POST['name']
		city    = request.POST['city']
		about   = request.POST['about']
		if valid_name(name):
				account.name     = name
				account.about_me = about
				account.city     = city
				account.save()
				msg = 'Information has been updated.'

		else:
			msg = 'Invalid name.'
	else:
		msg = 'Bad request!'

	if msg != "Information has been updated.":
		signal = 'error'
	return JsonResponse(
		{
			'signal': signal,
			'msg': msg,
		}
	)



@login_required
def accountNotices_view(request):
	if request.is_ajax() and request.method == "POST":
		account = Account.objects.get(username=request.user.username)
		template_name = 'accounts/account-notices.html'
		return render(request, template_name, {'account': account})
	else:
		return HttpResponse('')
