from django import forms
from friends.models import FriendRequest
from django.contrib.auth import get_user_model


User = get_user_model()

class SendFriendRequestForm(forms.Form):
	receiver_id = forms.ModelChoiceField(queryset=User.objects.all())


class HandleFriendRequestForm(forms.Form):
	friend_request_id = forms.ModelChoiceField(queryset=FriendRequest.objects.all())
