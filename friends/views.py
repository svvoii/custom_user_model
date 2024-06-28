from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from friends.forms import SendFriendRequestForm, HandleFriendRequestForm, RemoveFriendForm
from friends.models import FriendRequest, FriendList
from account.models import Account


def friend_requests_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to view friend requests')
		return redirect('login')

	user_id = kwargs.get('user_id')
	account = Account.objects.get(pk=user_id)
	if account == user:
		friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
		context['friend_requests_count'] = friend_requests
	else:
		messages.error(request, 'You can only view your own friend requests')

	return render(request, 'friends/friend_requests.html', context)


def send_friend_request_view(request):
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to send a friend request')
		return redirect('login')
	if request.method == 'POST':
		form = SendFriendRequestForm(request.POST)
		if form.is_valid():
			receiver = form.cleaned_data.get('receiver_id')
			FriendRequest.objects.create(sender=request.user, receiver=receiver)
			messages.success(request, f'Friend request sent to {receiver.username}')
			return redirect('account:profile', user_id=receiver.id)
		else:
			return HttpResponse('Invalid form data')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=request.user.id)


def cancel_friend_request_view(request):
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to cancel a friend request')
		return redirect('login')

	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request_id = form.cleaned_data.get('friend_request_id')
			friend_request_id.cancel()
			messages.success(request, f'Friend request cancelled')
			return redirect('account:profile', user_id=friend_request_id.receiver.id)
		else:
			# print(form.errors)
			return HttpResponse('Invalid form data.. cancel_friend_request_view')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=user.id)


def accept_friend_request_view(request):
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to accept a friend request')
		return redirect('login')

	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request_id = form.cleaned_data.get('friend_request_id')
			friend_request_id.accept()
			messages.success(request, f'You are now friends with {friend_request_id.sender.username}')
			return redirect('account:profile', user_id=user.id)
		else:
			return HttpResponse('Invalid form data.. accept_friend_request_view')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=user.id)


def remove_friend_view(request):
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to remove a friend')
		return redirect('login')

	if request.method == 'POST':
		form = RemoveFriendForm(request.POST)
		if form.is_valid():
			to_be_removed_user = form.cleaned_data.get('friend_id')
			try:
				friend_list = FriendList.objects.get(user=user)
			except ObjectDoesNotExist:
				messages.error(request, 'Invalid user id or FriendList not found')
				return redirect('account:profile', user_id=user.id)

			friend_list.unfriend(to_be_removed_user)
			messages.success(request, f'Friend removed')
			return redirect('account:profile', user_id=to_be_removed_user.id)
		else:
			# DEBUG #
			print(form.errors)
			return HttpResponse('Invalid form data.. remove_friend_view')
	
	else: # Never happens..
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=user.id)


def decline_friend_request_view(request):
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to decline a friend request')
		return redirect('login')

	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request_id = form.cleaned_data.get('friend_request_id')
			friend_request_id.decline()
			messages.success(request, f'Friend request declined')
			# return redirect('account:profile', user_id=friend_request_id.sender.id) # Redirect to the profile of the user who sent the request
			return redirect('account:profile', user_id=request.user.id) # Redirect to the user's profile
		else:
			return HttpResponse('Invalid form data.. decline_friend_request_view')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=request.user.id)


def friend_list_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if not user.is_authenticated:
		messages.error(request, 'You must be authenticated to view your friend list')
		return redirect('login')

	user_id = kwargs.get('user_id')
	if user_id:
		try:
			this_user = Account.objects.get(pk=user_id)
			context['this_user'] = this_user
		except Account.DoesNotExist:
			messages.error(request, 'User not found')
			return redirect('home')
		try:
			friend_list = FriendList.objects.get(user=this_user)
		except FriendList.DoesNotExist:
			messages.error(request, 'Friend list not found')
			return redirect('home')

		# Must be friend to view friend list
		if user != this_user:
			if not user in friend_list.friends.all():
				messages.error(request, 'You must be friends to view their friend list')
				return redirect('home')

		# Get the friend list
		friends = [] # List of friends [(account1, True), (account2, False), ...]
		user_friend_list = FriendList.objects.get(user=user)
		for friend in friend_list.friends.all():
			friends.append((friend, user_friend_list.is_mutual_friend(friend)))
		context['friends'] = friends

	return render(request, 'friends/friend_list.html', context)
