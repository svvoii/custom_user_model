from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from friends.forms import SendFriendRequestForm, HandleFriendRequestForm
from friends.models import FriendRequest
from account.models import Account


def send_friend_request_view(request):
	# DEBUG #
	print(request.POST)
	# # # # #
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
	# DEBUG #
	print(request.POST)
	# # # # #
	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request = form.cleaned_data.get('friend_request_id')
			friend_request.cancel()
			messages.success(request, f'Friend request cancelled')
			return redirect('account:profile', user_id=friend_request.receiver.id)
		else:
			# print(form.errors)
			return HttpResponse('Invalid form data.. cancel_friend_request_view')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=request.user.id)


def accept_friend_request_view(request):
	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request = form.cleaned_data.get('friend_request_id')
			friend_request.accept()
			messages.success(request, f'You are now friends with {friend_request.sender.username}')
			return redirect('profile')
		else:
			return HttpResponse('Invalid form data')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('profile')


def decline_friend_request_view(request):
	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request = form.cleaned_data.get('friend_request_id')
			friend_request.decline()
			messages.success(request, f'Friend request declined')
			return redirect('profile')
		else:
			return HttpResponse('Invalid form data')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('profile')

def remove_friend_view(request):
	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request = form.cleaned_data.get('friend_request_id')
			friend_request.cancel()
			messages.success(request, f'Friend removed')
			return redirect('profile')
		else:
			return HttpResponse('Invalid form data')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('profile')

