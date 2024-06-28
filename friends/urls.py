from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
	path('friend-requests/<user_id>/', views.friend_requests_view, name='friend_requests'),
	path('send-friend-request/', views.send_friend_request_view, name='send_friend_request'),
	path('cancel-friend-request/', views.cancel_friend_request_view, name='cancel_friend_request'),
	path('accept-friend-request/', views.accept_friend_request_view, name='accept_friend_request'),
	path('decline-friend-request/', views.decline_friend_request_view, name='decline_friend_request'),
	path('remove-friend/', views.remove_friend_view, name='remove_friend'),
	path('friend-list/<user_id>/', views.friend_list_view, name='friend_list'),
]
