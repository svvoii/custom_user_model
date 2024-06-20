from friends.models import FriendRequest


def get_friend_request_or_false(sender, receiver):
	try:
		friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
	except FriendRequest.DoesNotExist:
		return False
	return friend_request
