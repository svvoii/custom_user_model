from django.urls import path
from account.views import profile_view, edit_profile_view

app_name = 'account'

urlpatterns = [
	path('<user_id>/', profile_view, name='profile'),
	path('<user_id>/edit/', edit_profile_view, name='edit'),
]

# `<user_id>/` is a dynamic URL pattern that will be passed to the `profile_view` function in the `account/views.py` file. 
# The `name` attribute is used to reference this URL pattern in the Django templates. 
# The `app_name` attribute is used to namespace the URL pattern. 
# This is useful when you have multiple apps in your Django project and you want to avoid naming conflicts between URL patterns. 
# The `app_name` attribute is used in the `main/urls.py` file to include the URL patterns from this file.
