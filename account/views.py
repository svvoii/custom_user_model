from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.conf import settings

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from friends.utils import get_friend_request_or_false
from friends.friend_request_status import FriendRequestStatus
from friends.models import FriendList, FriendRequest


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return HttpResponse(f"You are already authenticated as {user.email}.")

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST) # this will create a form object with the data passed from the `register.html`
		if form.is_valid(): # this will validate the form data (all the fields of the form are valid)
			form.save() # this will trigger the `clean_email` and `clean_username` methods of the `RegistrationForm` class
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)

			destination = det_redirect_if_exists(request)
			# destination = kwargs.get('next')
			if destination:
				return redirect(destination)
			else:
				return redirect('home') # `home` is the name of the URL pattern in the `main/urls.py` file
		else:
			context['registration_form'] = form # this will pass any error message related to the form fields

	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('home')


def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect('home')
	
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				destination = det_redirect_if_exists(request)
				if destination:
					return redirect(destination)
				else:
					return redirect('home')
		else:
			context['login_form'] = form

	return render(request, 'account/login.html', context)

def det_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get('next'):
			redirect = str(request.GET.get('next'))
	return redirect


def profile_view(request, *args, **kwargs):
	content = {}
	user_id = kwargs.get('user_id')

	try:
		account = Account.objects.get(pk=user_id)
	except Account.DoesNotExist:
		return HttpResponse("User not found.")

	if account:
		content['id'] = account.id
		content['email'] = account.email
		content['username'] = account.username
		content['profile_image'] = account.profile_image
		content['hide_email'] = account.hide_email

		# determine the relationship status between the logged-in user and the user whose profile is being viewed
		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		content['friends'] = friends

		is_self = True
		is_friend = False
		user = request.user
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		friend_request = None
		
		# This check says : `If you are not looking at your own profile, then..`
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				# case 1: the user is not a friend and request status = `THEY_SENT_YOU`
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEY_SENT_TO_YOU.value
					content['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# case 2: the user is not a friend and request status = `YOU_SENT_TO_THEM`	
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# case 3: the user is not a friend and request status = `NO_REQUEST_SENT`
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

		# This check means : `If you are not logged in, then..`
		elif not user.is_authenticated:
			is_self = False
		
		# This check means : `If you are looking at your own profile, then..`
		else:
			try:
				friend_request = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				friend_request = None

		content['is_self'] = is_self
		content['is_friend'] = is_friend
		content['BASE_URL'] = settings.BASE_URL
		content['request_sent'] = request_sent
		content['friend_request'] = friend_request

	return render(request, 'account/profile.html', content)


def account_search_view(request, *args, **kwargs):
	context = {}

	if request.method == 'GET':
		search_query = request.GET.get('q')
		if len(search_query) > 0:
			# the following query will return all the accounts whose email or username contains the search query
			search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
			user = request.user
			accounts = [] # ..list structure: `[(account1, True), (account2, False), ...]` true/False is for friend status
			for account in search_results:
				accounts.append((account, False)) # False for indicating that the user is not a friend
			context['accounts'] = accounts

	return render(request, 'account/search_results.html', context)


def edit_profile_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect('login')

	user_id = kwargs.get('user_id')
	try:
		account = Account.objects.get(pk=user_id)
	except Account.DoesNotExist:
		return HttpResponse("User not found.")

	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone else's profile.")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('account:profile', user_id=account.pk)
			# context['success_message'] = "Updated"
		else:
			form = AccountUpdateForm(
				request.POST,
				instance=request.user,
				initial={
					'id': account.pk,
					'email': account.email,
					'username': account.username,
					'profile_image': account.profile_image,
					'hide_email': account.hide_email,
				}
			)
	else:
		form = AccountUpdateForm(
			initial={
				'id': account.pk,
				'email': account.email,
				'username': account.username,
				'profile_image': account.profile_image,
				'hide_email': account.hide_email,
			}
		)

	context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE

	return render(request, 'account/edit_profile.html', context)
