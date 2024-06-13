# Custom User Model

This repository contains the code for the tutorial on how to create a custom user model in Django. The tutorial covers the following topics:

- Creating a new Django project
- Adding a new apps to the project
- Creating templates
- Adding and referencing static files
- Adding default profile image
- Building a custom user model
- Handling case-insensitive input with backends model
- Custom forms for registration and login
- Password reset functionality
- Profile page with update functionality

You can follow along the tutorial to create the project from scratch or run the project from this repository. The project is built using Django 3.2.7 and Python 3.9.6.  

## Creating New Django Project

*Assuming `python` and `pipenv` are installed.*

### To run the project from this repository:

*If you want to run the project from this repository, follow the steps below to set up the environment and run the server*  

1. Clone the repository

```bash
git clone https://github.com/svvoii/custom_user_model.git

cd custom_user_model
```

2. Install the dependencies

```bash
pipenv install requirements.txt
```

3. Run the server

```bash
python manage.py runserver
```

*This shall be it for the project setup*


### To follow along this tutorial:

*If you want to follow along this tutorial and create the project from scratch, follow the steps below to set up the environment*

1. Creating new directory for the project and install Django with pipenv

```bash
mkdir custom_user_model
cd custom_user_model

pipenv install django
```

2. Create a new Django project

```bash
django-admin startproject main .
```
*This will create a new Django project in the current directory with the name `main`*  


**NOTE**: *The following command can be used at any point or whenever additional packages are installed to save the requirements of the project to a file named `requirements.txt`. This helps to track the dependencies of the project as well as to install the same dependencies at once in a new environment*

```bash
pip freeze > requirements.txt
```


## Creating Homepage App and Templates

1. Creating new app to handle the homepage

```bash
python manage.py startapp homepage
```

2. Adding the `homepage` app to the `INSTALLED_APPS` list in the `main/settings.py` file:

```python
INSTALLED_APPS = [
	'homepage',
	...
]
```

3. Create a new directory named `templates` at the same level as `account` app directory  

```bash
mkdir templates
```

4. Create new directories named `homepage/templates` and `homepage/templates/homepage`: 

```bash
mkdir homepage/templates
mkdir homepage/templates/homepage
``` 

*This will contain the templates for the homepage app*

5. Add the `templates` directory to the `DIRS` list in the `main/settings.py` file  

```python
# Adding the following include to use `os` module.
import os
...

TEMPLATES = [
	{
		...
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		...
	}
]
...
```

*This will allow Django to look for templates in the main `templates` directory as well as `templates` in the app directories*  

6. Create a `layout.html` file in the main `templates` directory:

```html
<!DOCTYPE html>
<html lang=en>

<head>
    <meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
</head>

<body>
	<div>
		{% block content %}
		{% endblock content %}
	</div>
</body>

</html>

```

7. Create a `home.html` file in the `homepage/templates/homepage` directory:

```html
{% extends 'layout.html' %}

{% block content %}
	<h1>Welcome to the homepage</h1>
{% endblock content %}
```

8. Adding `home_view` function to the `homepage/views.py` file:

```python
from django.shortcuts import render

def home_view(request, *args, **kwargs):
	context = {} # ..for illustration purposes, this is how you pass data to the template
	return render(request, "home.html", context)
```

9. Adding reference to the `home_view` function in the `main/urls.py` file:

```python
from django.contrib import admin
from django.urls import path

# Adding the following include to import the home_view function
from homepage.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', home_view, name='home') # Adding the home_view function to the root URL
]
```

*At this point, we can now run the server and see the homepage template we created at `http://localhost:8000`*  


## Adding and Referencing Static Files

### Setting Up Static Files Directory

**NOTE**: *Take a look on the official Django docs for [static files](https://docs.djangoproject.com/en/5.0/howto/static-files/)*


1. Adding the following to the bottom of the `main/settings.py` file:

```python
...
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static'),
	os.path.join(BASE_DIR, 'media'),
]

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn') # ..cdn is short for content delivery network
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')

TEMP = os.path.join(BASE_DIR, 'media_cdn/temp') # ..for temporary files used in the project when cropping images

BASE_DIR = "http://127.0.0.1:8000" # ..for the base URL of the project. Will be easier to access the project URL in the future (This shall be changed to the actual URL of the project when deployed)
```

2. Adding the following to the `main/urls.py` file:

```python
...
from django.conf import settings
from django.conf.urls.static import static # Adding the following include to use static files
...
# after `urlpatterns` list

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

*This is to tell Django to serve the static files in the `static` directory*  


3. Create a new directory named `static` at the same level as the `templates` directory and other apps directories:  

```bash
mkdir static
mkdir static_cdn
mkdir media
mkdir media_cdn
```

**NOTE** *`static_cdn` and `media_cdn` directories are an example of the directories where the static and media files will be stored when the project is deployed*  

4. Using `collectstatic` command to collect all the static files in the project to the `static_cdn` directory:

```bash
python manage.py collectstatic
```

*This will collect all the static files in the project to the `static_cdn` directory*  

**NOTE**: *The `collectstatic` command will create a new directory named `static_cdn` in the project directory and copy all the static files in the project to this directory. I was not using `collectstatic` command in order to avoid bunch of copied in this repository*   


5. Adding `load static` to the top of the `layout.html` file in the `templates` directory:

```html
{% load static %}
...
```

*This will allow us to use the static files (img, css, js etc) in the project*  


### Adding & Using Stsatic Images

1. Create a new directory named `images` in the `static` directory:

```bash
mkdir static/images
```

2. Add the images of choice to the `static/images` directory:

*For example, [emoticon smile icon](https://www.iconexperience.com/o_collection/icons/?icon=emoticon_smile)*  

3. Adding the image to the html file of choice:

For example adding the image to the `layout.html` file as a link to the profile page :

```html
{% load static %}
...
<nav>
	...
	<a href="/profile" title="PROFILE"> <img src="{% static 'images/smile_32-32.png' %}"> </a>
</nav>
...
```

**NOTE**: **`{% load static %} must be added to the top of the html file to use the static files in the project`**

4. Using `collectstatic` command to collect all the static files in the project to the `static_cdn` directory:

```bash
python manage.py collectstatic
```

*This will collect all the static files in the project to the `static_cdn` directory*  

*The image will now be displayed on the navigation bar and will redirect to the profile page (which doesnt exist yet)*


### Adding Default Profile Image

1. Create a new directory named `profile_images` in the `media_cdn` directory:

```bash
mkdir media_cdn/profile_images
```

*This will be used to store the profile images of the users*  

2. Add the `default.png` image to the `media_cdn/profile_images` directory:  

*This will be used as the default profile image for the users who don't upload their own profile image*  

For example, [this image](https://www.iconninja.com/avatar-anonym-person-user-default-unknown-head-icon-15892) can be used as the default profile image.  

**NOTE**: *We can test the availability of the default profile picture later in Custom User Model section*  


### Adding & Using Goggle Icons

**Optional** *This part can be skipped.*
*However, it might be a nice touch, let alone the all the fun..*

1. Getting the link to the google icons.

- Go to the [Google Icons](https://fonts.google.com/icons) website
- Visit the respective GitHub repository for the icons [here](https://github.com/google/material-design-icons)
- Copy the link to the icons : 
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
```
**NOTE**: *verify if this is the right link.. for me the second link in the repo worked not the 1st one*

2. Adding the link to the `layout.html` file in the `templates` directory:

```html
...
<head>
	...
	<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
</head>
...
```

*Now the google icons can be used in the project*  

3. Example of the link to the `Home` icon in the `layout.html` file:

```html
...
<body>
	<a href="/" title="HOME">
	<span class="material-symbols-outlined">home</span>
	</a>
	...
</body>
...
```
*This will display the `Home` icon which is clickable and will redirect to the home page*  

**NOTE**:  
*To add any other icons simply use the name of the icon in the `<span ..>` tag*  
*Or, alternatively, the complete `<span ..>` tag is available on [Google Icons](https://fonts.google.com/icons) website. When the icon is clicked, there is a `<span ..>` tag on the right side panel in the `Inserting the icon` section*  


## Building Custom User Model

**NOTE**: *If curious, take a look at the original `AstractBaseUser` and `BaseUserManager` models on the [Django GitHub](https://github.com/django/django/blob/main/django/contrib/auth/base_user.py)*

1. Create a new Django app

```bash
python manage.py startapp account
```
*This will create a new Django app in the project directory with the directory name `account`*

2. Add the app to the installed apps in the `main/settings.py` file

*Also adding the necessary parameter to tell Django to use our custom user model*

```python
...
# This is to tell Django to use the custom user model we are creating
AUTH_USER_MODEL = 'account.Account'

INSTALLED_APPS = [
	...
	'account',
]
...
```

3. Create a custom user model in the `account/models.py` file

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager # importing the AbstractBaseUser and BaseUserManager classes to extend them in custom user model


class MyAccountManager(BaseUserManager):

	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have a username")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
		)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


# This function will be used to get the profile image path of the user. User custom images will be stored in the `media_cdn/profile_images` directory
def get_profile_image_filepath(self, filename):
	return f'profile_images/{self.pk}/{"profile_image.png"}'

# This function will be used to get the default profile image of the user.. in `static/images` directory
def get_default_profile_image():
	return "profile_images/default.png"

class Account(AbstractBaseUser):

	# Overriding the default fields of the AbstractBaseUser class
	email = models.EmailField(verbose_name="email", max_length=60, unique=True) # unique=True is to make sure the email is unique
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	prfile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email = models.BooleanField(default=True)

	objects = MyAccountManager()

	USERNAME_FIELD = 'email' # This will be used to login the user
	REQUIRED_FIELDS = ['username'] # This will be required as well to create an account
	
	def __str__(self):
		return self.username
	
	# This will be used to get the profile image name of the user
	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/{self.pk}/'):]	

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

```

**Note**: *`ImageField` is a part of the `Pillow` library. So, make sure it is installed before running the server*  

```bash
pipenv install Pillow
```

4. Add the custom user model to the `main/admin.py` file

*This will allow us to see the custom user model in the admin page and all the fields we specified*  

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from account.models import Account


class AccountAdmin(UserAdmin):
	# These properties will be display the following fields in the admin page (as columns)
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')

	# This will define the search fields in the admin page (when using the search bar)
	search_fields = ('email', 'username')

	# This will define the fields that can NOT be edited in the admin page (when clicking on a user)
	readonly_fields = ('id', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

# Register the Account model with the custom AccountAdmin
admin.site.register(Account, AccountAdmin)

# This will remove the Group model from the admin page (we don't need it here)
admin.site.unregister(Group)
``` 

**NOTe**: *This is necessary to see the custom user model in the admin page, so Django knows how to display the custom user model*  

5. Making migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
*This will create the necessary migrations for the custom user model and apply them to the database*

6. Create a superuser

```bash
python manage.py createsuperuser
```
*This is the necessary to be able to login to the admin page as well as see the custom user model we created*  
*`createsuperuser` command will use the custom user model we created to create the superuser, where `email` will be used to login the user*    

7. Run the server

```bash
python manage.py runserver
```

**Note:**  
*At this point, we can now login to the admin panel and see the custom user model we created with the fields we specified.*  

*The email will be used to login the user and the username will be displayed in the admin page*  

*The default profile image (stored in the `media_cdn/profile_images` directory) shall be displayed via link in the admin page in the `Change account` --> `Profile Image` section once we click on the account email* 


## Handling Case-Insensitive Input

*This functionality ensures that the user can login with the email or username in any case. For this to work, we need to create a custom authentication backend module to handle the authentication process with case-insensitive email and username*  

1. Create a custom authentication backend in the `account/backends.py` file in the `account` app  

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CaseInsensitiveModelBackend(ModelBackend):

	# Overriding the authenticate method
	def authenticate(self, request, username=None, password=None, **kwargs):
		
		UserModel = get_user_model() # Getting the user model defined in the settings.py file (AUTH_USER_MODEL..)

		if username is None:
			username = kwargs.get(UserModel.USERNAME_FIELD) # Getting the username field from models.py (USERNAME_FIELD..)
		try:
			# case_insensitive_username_field = f'{UserModel.USERNAME_FIELD}__iexact'
			case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
			user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
		except UserModel.DoesNotExist:
			UserModel().set_password(password)

		else:
			if user.check_password(password) and self.user_can_authenticate(user):
				return user
```

2. Add the custom authentication backend to the `main/settings.py` file

```python
# after the AUTH_USER_MODEL adding the custom authentication backend
AUTH_USER_MODEL = 'account.Account'
AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.AllowAllUsersModelBackend',
	'account.backends.CaseInsensitiveModelBackend',
]
```

*This will allow us to authenticate the user if the email or username is entered in either upper or lower case*  

3. Setting up profile image in the `layout.html` file

*The following code will display the profile image of the user in the navigation bar on the homepage if the user is authenticated. We add this code to the `layout.html` file in the `templates` directory:*

```html
...
<nav>
	...
	{% if request.user.is_authenticated %}
		<p>{{ request.user.username }} is authenticated.</p>
		<p>Profile image: {{ request.user.profile_image.url }}</p>
		<img src="{{ request.user.profile_image.url }}" alt="LOGO" width="40" height="40">
	{% else %}
		<p>Not logged in</p>
	{% endif %}
</nav>
...
```

**NOTE**: *We dont have yet the profile page nor the login page, so to check if the profile image (default.png) is displayed in the navigation bar, we can login to the admin page and then navigate to `http://localhost:8000`*

*This should display the profile image as well as show the username of the user and the link to the current profile image in the browser window*  


## Adding Registration, Login, Logout, Password Reset, Profile Pages

**NOTE**: *The is no styling applied to any of html files, so it looks a bit ugly.. no judgement please.. ;)*  


### Registration Page

1. Creating the followign new directory: `account/templates/account` and adding the `registration.html` in there:

```html
{% extends 'layout.html' %}

{% load static %}

{% block content %}

	<h1>Registration</h1>

	<form method="POST">
		{% csrf_token %}

		<img src="{% static 'images/smile_32-32.png' %}" alt="LOGO" width="40" height="40"></br>

		<input type="email" name="email" placeholder="Email address" required autofocus></br>
		<input type="text" name="username" placeholder="Username" required></br>
		<in		<input type="text" name="username" placeholder="Username" required></br>
		<input type="password" name="password2" placeholder="Confirm password" required></br>

		{% for field in registration_form %}
			{% for error in field.errors %}
				<div style="color: red;"> 
					<p> {{ error }} </p> 
				</div>
			{% endfor %}
		{% endfor %}

		{% if registration_form.non_field_errors %}
			<div style="color: red;"> 
				<p> {{ registration_form.non_field_errors }} </p>
			</div>
		{% endif %}

		<button type="submit">Register</button>
	</form>

{% endblock content %}
```

2. Creating the `RegistrationForm` in the `account/forms.py` file:

*First we create new file named `forms.py` in the `account` app directory and add the following class:*

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account

class RegistrationForm(UserCreationForm):

	email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address')
 
	class Meta:
		model = Account
		fields = ('email', 'username', 'password1', 'password2')

	# This method is used to clean the data of the form (validate the data)
	def clean_email(self):
		email = self.cleaned_data['email'].lower() # ..`email` is the name of the field which passed from `register.html`
		try:
			account = Account.objects.get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError(f'Email {email} is already in use.')
	
	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.get(username=username)
		except Exception as e:
			return username
		raise forms.ValidationError(f'Username {username} is already in use.')
```

*If curious, take a look at the original `UserCreationForm` model on the [Django GitHub](https://github.com/django/django/blob/main/django/contrib/auth/forms.py)*  


3. Adding the `register_view` function to the `account/views.py` file:

*This function will handle the registration process and render the `registration.html` template*

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

from account.forms import RegistrationForm


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

			destination = det_redirect_if_exists(request) # this is created in the (Login, Logout) step
			# destination = kwargs.get('next')
			if destination:
				return redirect(destination)
			else:
				return redirect('home') # `home` is the name of the URL pattern in the `main/urls.py` file
		else:
			context['registration_form'] = form # this will pass any error message related to the form fields

	return render(request, 'account/register.html', context)


def det_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get('next'):
			redirect = str(request.GET.get('next'))
	return redirect
```

4. Adding the reference to the `register_view` function in the `main/urls.py` file:

```python
...
from account.views import register_view

urlpatterns = [
	...
	path('register/', register_view, name='register'),
]
...
```

5. Adding the link to the registration page in the `layout.html` file in the `templates` directory:

```html
<nav>
	...
	{% if request.user.is_authenticated %}
		...
	{% else %}
		<p>Not logged in</p>

		<a href="{% url 'register' %}" title="REGISTER"> <span class="material-symbols-outlined">person_add</span>Register</a>
	{% endif %}
</nav>
...
```

*This will allow us to access the registration page at `http://localhost:8000/register` directly from the homepage*  

*Also there is an error pops up when trying to delete the user from the admin page.. this will be fixed later*  


### Login, Logout

1. Creating the `login.html` file in the `account/templates/account` directory:

```html
{% extends 'layout.html' %}
{% load static %}
{% block content %}
	<h1>Login</h1>
	<form method="POST">
		{% csrf_token %}

		<img src="{% static 'images/smile_32-32.png' %}" alt="LOGO" width="40" height="40"></br>

		<input type="email" name="email" placeholder="Email address" required autofocus></br>
		<input type="password" name="password" placeholder="Password" required></br>

		{% for field in login_form %}
			{% for error in field.errors %}
				<div style="color: red;"> 
					<p> {{ error }} </p> 
				</div>
			{% endfor %}
		{% endfor %}

		{% if login_form.non_field_errors %}
			<div style="color: red;"> 
				<p> {{ login_form.non_field_errors }} </p>
			</div>
		{% endif %}

		<button type="submit">Login</button>
	</form>

	<div>
		<a href="#">Reset password</a>
	</div>
{% endblock content %}
```

2. Creating new class in the `account/forms.py` file:

*This class will be used to create the login form*

```python
...
# Adding new class to handle the login form
class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput) # `widget..` makes the password field to be displayed as a password field

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError('Invalid login')
```

3. Adding the `login_view` function to the `account/views.py` file:

*This function will handle the login process and render the `login.html` template*

```python
...

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
```

4. Adding the reference to the `login_view` function in the `main/urls.py` file:

```python
...
from account.views import register_view, login_view, logout_view

urlpatterns = [
	...
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
]
...
```

5. Adding the link to the login page in the `layout.html` file in the `templates` directory:

```html
...
<nav>
	<a href="/" title="HOME"> <span class="material-symbols-outlined">home</span></a>
	<a href="/profile" title="PROFILE"> <img src="{% static 'images/smile_32-32.png' %}"></a>

	{% if request.user.is_authenticated %}
		<img src="{{ request.user.profile_image.url }}" alt="LOGO" width="40" height="40">
		<a href="{% url 'logout' %}" title="LOGOUT"> <span class="material-symbols-outlined">logout</span>Logout</a>
	{% else %}
		<a href="{% url 'login' %}" title="LOGIN"> <span class="material-symbols-outlined">login</span>Login</a>
		<a href="{% url 'register' %}" title="REGISTER"> <span class="material-symbols-outlined">person_add</span>Register</a>
	{% endif %}
</nav>
...
```

*This will allow us to access the login page at `http://localhost:8000/login` directly from the homepage. As well as to show the `Logout` option*


### Password Reset Pages



