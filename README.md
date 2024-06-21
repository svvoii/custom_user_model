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

BASE_URL = "http://127.0.0.1:8000" # ..for the base URL of the project. Will be easier to access the project URL in the future (This shall be changed to the actual URL of the project when deployed)
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

**NOTE**: *Resetting the password in the development environment is different from the production environment. In the development environment, the password reset link will be displayed in the console. In the production environment, the password reset link will be sent to the user's email, and the process is different*  

The following steps will be done in the development environment:  

1. Adding the `pasword_reset` directory in the `templates` which is at the same level as the `account` app directory:

```bash
mkdir templates/password_reset
```

2. Addting several files in the `password_reset` directory:
`password_change.html`
`password_change_done.html`
`password_reset_complete.html`
`password_reset_done.html`
`password_reset_email.html`
`password_reset_form.html`
`password_reset_subject.txt`

- Adding the `password_change.html` :

```html
{% extends 'layout.html' %}
{% block content %}
<form method="POST">
	{% csrf_token %}
	<h1>Change password</h1>
    <input name="old_password" placeholder="Old password" type="password" required="true">
    <input name="new_password1" placeholder="New password" type="password" required="true">
    <input name="new_password2" placeholder="Confirm password" type="password" required="true">

    {% for field in form %}
		{% for error in field.errors %}
			<p style="color: red"> {{ error }} </p>
		{% endfor %}
    {% endfor %}

  <button type="submit">Update</button>  
</form>
{% endblock %}
``` 

- Adding the `password_change_done.html` :

```html
{% extends 'layout.html' %}
{% block content %}
<div>
	<p>Your password has been Updated.</p>
</div>
{% endblock %}
```

- Adding the `password_reset_complete.html` :

```html
{% extends 'layout.html' %}
{% block content %}
<div>
	<p>Your password has been reset. You may go ahead and <a href="{% url 'login' %}">sign in</a> now.</p>
</div>
{% endblock %}
```

- Adding `password_reset_done.html` :

```html
{% extends 'layout.html' %}
{% block content %}
<div>
	<p>
	We've emailed you instructions for setting your password, if an account exists with the email you entered.
	You should receive them shortly.
	</p>
	<p>
	If you don't receive an email, please make sure you've entered the address you registered with,
	and check your spam folder.
	</p>
	<p><a href="{% url 'home' %}">Return to home page</a></p>
</div>
{% endblock %}
```

- Adding `password_reset_email.html` :

```html
{% autoescape off %}
To initiate the password reset process for your Account {{ user.email }},
click the link below:

{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}

If clicking the link above doesn't work, please copy and paste the URL in a new browser
window instead.

Sincerely,
The Open-Chat Team
{% endautoescape %}
```

- Adding `password_reset_form.html` :

```html
{% extends 'layout.html' %}
{% block content %}
<form method="POST">
	{% csrf_token %}
	<h1>Reset password</h1>
	<input name="email" placeholder="Email address" type="email" required="true" >
	<button>Send reset email</button>  
</form>
{% endblock %}
```

- Adding `password_reset_subject.txt` :

```txt
PASSWORD RESET
```

3. Adding the following urls to the `main/urls.py` file:

```python
...
from django.contrib.auth import views as auth_views # For password reset (built-in Django)
...
urlpatterns = [
	...
	# Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
]	
...
```

**NOTE**: *Here is the link to [auth views on Django GitHub](https://github.com/django/django/blob/main/django/contrib/auth/views.py) if curious. It contains all indicated above views. This also corresponds to the files we created in the `password_reset` directory*  

4. Adding the necessary settings to the `main/settings.py` file:

**NOTE**: *The following settings are valid for the development environment !! In the production environment, the settings are different. It will be necessary to set up the email server and send the actual email to the user. While in the development environment, the password reset link will be displayed in the terminal window*  

```python
...
DEBUG = True # After the DEBUG setting

if DEBUG:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # This will display the password reset link in the terminal window
...
```

5. The following step would be to update the reference link in the `login.html` file in the `account/templates/account/login.html`. At the bottom of the file :

```html
...
<div>
	<a href="{% url 'password_reset' %}">Reset password?</a>
</div>
...
```

*This shall be it for the password reset pages. The password reset link will be displayed in the terminal window when the user enters the email address in the password reset form*.  


## ***Profile Page***

### ***ADDING BASIC PROFILE PAGE***

Lets first discuss the profile and its functionality.  
Profile page will be used to display the user's profile information as well as to update the profile image.  
Also profile page can have several states and functionalities :  

- **is_self**: *This is where the user is viewing their own profile page and can change the profile image, password, link to friends..*
- **is_user**: *This is where the user is viewing the profile page of another user and can send friend request..*  
- **is_friend**: *This is where the user is viewing the profile page of a friend and can send messages, remove friend..*

**NOTE**: *The end logic of how to represent a profile page can be quite complex and can be implemented in many ways. For now, we will implement the basic functionality of the profile page. For now we will treat the profile page based on two events*:  
- *The user is viewing their own profile page*
- *The user is viewing the profile page of another user*

1. Creating `profile.html` file in `account/templates/account/` directory:


```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}
<img src="{{ request.user.profile_image.url }}" alt="Profile Image" width="40" height="40">
<p>Email</p>
{%  if is_self %}
	<h5>{{ email }}</h5>
{% else %}
	{% if hide_email %}
		<h5>**********</h5>
	{% else %}
		<h5>{{ email }}</h5>
	{% endif %}
{% endif %}
<p>Username</p>
<h5>{{ username }}</h5>

<!-- If Auth user is viewing their own profile -->
{% if is_self %}
	<a href="#">Update</a></br>
	<a href="{% url 'password_change' %}">Change password</a></br>
{% endif %}

{% if request.user.is_authenticated %}

	<!-- THEM to YOU -->
	{% if request_sent == 0 %}
	<div>
		<span>Accept Friend Request</span>
		<span id="id_cancel_{{id}}" onclick='triggerDeclineFriendRequest("{{ pending_friend_request_id }}")'>cancel</span>
		<span id="id_confirm_{{id}}" onclick='triggerAcceptFriendRequest("{{ pending_friend_request_id }}")'>check</span>
	</div>
	{% endif %}

	<!-- Cancel Friend Request / Send Friend Request / Remove Friend -->
	{% if is_friend == False and is_self == False %}
		<!-- You sent them a request -->
		{% if request_sent == 1 %}
			<button> Cancel Friend Request </button></br>
		{% endif %}
		<!-- No requests have been sent -->
		{% if request_sent == -1 %}
			<button> Send Friend Request </button></br>
		{% endif %}
	{% endif %}
		
	{% if is_friend %}
		<button> Friends </button>
		<a href="#" onclick="removeFriend('{{ id }}', onFriendRemoved)">Unfriend</a>
	{% endif %}
	
	<!-- TODO -->
	<!-- Friend list link -->
	<a href="#">
		<span> contact_page </span></br>
		<span> Friends (0) </span></br>
	</a>

	<!-- TODO -->
	{#% if friend_requests %#}
	<!-- Friend requests -->
		<a href="#">
			<span> person_add </span></br>
			<span> Friend Requests (0) </span></br>
		</a>
	{#% endif %#}

	{% if is_friend %}
		<div onclick="createOrReturnPrivateChat('{{ id }}')">
			<span> message </span></br>
			<span> Message </span></br>
		</div>
	{% endif %}

{% endif %}
{% endblock content %}

```

2. Adding the `profile_view` function to the `account/views.py` file:

```python
...
from django.conf import settings

from account.models import Account
...
...
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

		is_self = True
		is_friend = False
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
		elif not user.is_authenticated:
			is_self = False

		content['is_self'] = is_self
		content['is_friend'] = is_friend
		content['BASE_URL'] = settings.BASE_URL

	return render(request, 'account/profile.html', content)
```

3. Adding new url file in the `account` app directory named `urls.py`:

in the `account/urls.py` file:

```python
from django.urls import path
from account.views import profile_view

app_name = 'account'

urlpatterns = [
	path('<user_id>/', profile_view, name='profile'),
]

``` 
**NOTE**: *`<user_id>/` is a dynamic URL pattern that will be passed to the `profile_view` function in the `account/views.py` file.*  
*`name` attribute is used to reference this URL pattern in the Django templates.*  
*`app_name` attribute is used to namespace the URL pattern.*  
*This is useful when you have multiple apps in your Django project and you want to avoid naming conflicts between URL patterns.*  
*`app_name` attribute is used in the `main/urls.py` file to include the URL patterns from this file.*  


4. Adding the reference to the account urls in the `main/urls.py` file:

```python
...
from django.conf.urls import include
...
urlpatterns = [
	...
	path('account/', include('account.urls', namespace='account')),
	...
]
```

5. Adding the link to the profile page in the `layout.html` file in the `templates` directory:

```html
<nav>
	...
	{% if request.user.is_authenticated %}
		...
		<a href="{% url 'account:profile' user_id=request.user.id %}" title="PROFILE"> <img src="{{ request.user.profile_image.url }}" alt="LOGO" width="40" height="40"></a>
	{% else %}
		...
	{% endif %}
</nav>
```
*This change to the navbar will allow us to access profile page by clicking on the profile image in the navigation bar*  

**NOTE**: *`account:profile` is the namespace of the URL pattern we created in the `account/urls.py` file*  
*So, that `account` is the app name indicated both in the `account/urls.py` as `app_name = 'account'` and in the `main/urls.py` as `namespace='account'`*  
*`profile` is the name of the URL pattern we created in the `account/urls.py` file*  

*We can go ahead and access the profile page at `http://localhost:8000/profile`*  


### ***IMPLEMENTING USER SEARCH***  

*This will allow the user to search for other users by their username or email address. The search results will be displayed in the search page*  

1. Creating the `search_results.html` file in the `account/templates/account` directory:

```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}

{% if accounts %}

	{% for account in accounts %}
		<a href="{% url 'account:profile' user_id=account.0.id %}">
			<img src="{{ account.0.profile_image.url }}" alt="profile_image">
		</a>

		<a href="{% url 'account:profile' user_id=account.0.id %}">
			<h4>{{ account.0.username }}</h4>
			{% if account.1 %}
				<p><a href="#" onclick="createOrReturnPrivateChat('{{ account.0.id }}')">Send a Message</a></p>
			{% endif %}
		</a>

		{% if account.1 %} <!-- If friends -->
			<p> Friends </p>
			<span> check_circle_outline </span>
		{% else %}
			{% if account.0 !=  request.user %} <!-- If not friends -->
				<p> Not Friends </p>
				<span> cancel </span>
			{% endif %}
		{% endif %}

		{% if account.0 == request.user %} <!-- If you -->
			<p> This is you </p>
			<span> person_pin </span>
		{% endif %}

	{% if forloop.counter|divisibleby:2 %} <!-- If even.. `forloop.counter` is to access the index -->
		<!-- <br> -->
	{% endif %}
	
	{% endfor %}
	
	{% else %} <!-- If no friends -->
		<p> No results </p>
{% endif %}

{#%  include 'chat/create_or_return_private_chat.html' %#}

{% endblock content %}
```

2. Adding the `account_search_view` function to the `account/views.py` file:

```python
...
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
```

3. Adding the reference to the `account_search_view` function in the `account/urls.py` file:

```python
...
from account.views import register_view, login_view, logout_view, account_search_view # ..adding the account_search_view function
...
urlpatterns = [
	...
	path('search/', account_search_view, name='search'),
	...
]
```

4. Modifying the navbar to show the search bar.

*Currently the navbar in the `layout.html` file in the main `templates` directory. We gonna move the navbar to its own file `header.html` in the `templates` to make it more readable and maintainable*  

So, in the `templates/header.html` file:

```html
<style type="text/css">

	nav {
		display: flex;
		justify-content: space-between;
		background-color: lightgray;
		padding: 10px;
		border-bottom: 1px solid black;
	}

	nav a {
		margin-right: 20px;
		color: darkblue;
		text-decoration: none;
	}

</style>

<nav>
	<a href="/" title="HOME"> <span class="material-symbols-outlined">home</span></a>

	<form action="{% url 'search' %}" method="get">
		<input type="text" name="q" id="id_q_large" placeholder="Search...">
		<input type="submit" value="Search">
	</form>

	{% if request.user.is_authenticated %}
		<a href="{% url 'account:profile' user_id=request.user.id %}" title="PROFILE"> <img src="{{ request.user.profile_image.url }}" alt="LOGO" width="32" height="32">
			{{ request.user.username }}
		</a>
		<a href="{% url 'logout' %}" title="LOGOUT"> <span class="material-symbols-outlined">logout</span>
			Logout
		</a>
	{% else %}
		<a href="{% url 'login' %}" title="LOGIN"> <span class="material-symbols-outlined">login</span>Login</a>
		<a href="{% url 'register' %}" title="REGISTER"> <span class="material-symbols-outlined">person_add</span>Register</a>
	{% endif %}

</nav>
```

5. Adding another separate file to render the footer in the `templates` directory:

So, for the same reason of better maintainability and readability, creating a new file `templates/footer.html`:

```html
<style>
	footer {
		background-color: #333;
		color: white;
		text-align: center;
		position: fixed;
		bottom: 0;
		width: 100%;
	}
</style>

<footer>
	<p> &copy; 2024 - All rights reserved, no BS 
	<span class="material-symbols-outlined">copyright</span>
	</p>
</footer>
```

**NOTE**: *The `<style..` tags in both header and footer are used to style the navigation bar and footer respectively for a better visual, it is still ugly.. but better. The styling shall be done separately in any desirable way with bootstrap (as minor project module) or manual css, etc.. Current styling is temporary*

**NOTE**: *The `<form..>` tag in header is used to create a search bar in the navigation bar. The search bar will be used to search for other users by their username or email address*  

5. Modify the `layout.html` file to include the `header.html` and `footer.html` files:

*This is how the `templates/layout.html` file can look like at this point:*

```html
{% load static %}

<!DOCTYPE html>
<html lang=en>

<head>
    <meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
</head>

<body>
	{% include 'header.html' %}

	<div>
		{% block content %}

			{% if request.user.is_authenticated %}
				<p>{{ request.user.username }} is authenticated.</p>
				<p>profile image: {{ request.user.profile_image.url }}</p>
			{% else %}
				<p>not logged in</p>

			{% endif %}	

		{% endblock content %}
	</div>

	{% include 'footer.html' %}
</body>

</html>
```

**NOTE**: *The `{% include 'header.html' %}` and `{% include 'footer.html' %}` syntax is used to include the `header.html` and `footer.html` files in the `layout.html` file. This will display the navigation bar on teh top and the footer at the bottom on the homepage*

*At this point, we can now access the search page at `http://localhost:8000/search` and search for other users by their username or any characters in tehir username*  


### ***EDIT ACCOUNT FUNCTIONALITY***

*This will allow the user to edit their account information, such as the email address, username, and profile image. The user will be able to update their account information in the edit account page*  

1. Creating the `edit_profile.html` file in the `account/templates/account` directory:

```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}

<div>
	<img src="{{ form.initial.profile_image.url }}" alt="profile_image" width="128" height="128">
</div>
<form method="post" enctype="multipart/form-data">
	{% csrf_token %}
	<input type="file" name="profile_image">
	<h6>Email</h6>
	<input type="email" name="email" id="id_input_email" placeholder="Email address" required autofocus value={{ form.initial.email }}> <h6 class="mt-4 field-heading">Username</h6>
	<input type="text" name="username" id="id_input_username" placeholder="Username" required value="{{ form.initial.username }}">
	<label>
		<input type="checkbox" name="hide_email" id="id_input_hide_email"
		{% if form.initial.hide_email %}
			checked
		{%endif%}>
		Hide Email
	</label>

	{% for field in form %}
	<p>
		{% for error in field.errors %}
			<p style="color: red">{{ error }}</p>
		{% endfor %}
	</p>
	{% endfor %}

	{% if form.non_field_errors %}
		<div style="color: red">
		<p>{{ form.non_field_errors }}</p>
		</div>

	{% endif %}

	<button type="submit">Save</button>
	
</form>

{% endblock content %}
```

2. Adding `AccountUpdateForm` class to the `account/forms.py` file:

```python
...
class AccountUpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ('email', 'username', 'profile_image', 'hide_email')
	
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError(f'Email {email} is already in use.')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError(f'Username {username} is already in use.')

	def save(self, commit=True):
		account = super(AccountUpdateForm, self).save(commit=False)
		account.email = self.cleaned_data['email']
		account.username = self.cleaned_data['username']
		account.profile_image = self.cleaned_data['profile_image']
		account.hide_email = self.cleaned_data['hide_email']
		if commit:
			account.save()
		return account
```

3. Adding the `edit_profile_view` function to the `account/views.py` file:

```python
...
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm # ..importing the AccountUpdateForm
...
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
``` 

4. Adding a global variable to the `main/settings.py` file:

*This is used to limit the size of the profile image that the user can upload to the server.*

```python
...
# This is to set a global variable for the maximum size od the uploaded profile image (5MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
``` 

5. Adding the reference to the `edit_account_view` function in the `account/urls.py` file:

```python
...
from account.views import profile_view, edit_profile_view # adding the edit_profile_view function
...

urlpatterns = [
	...
	path('<user_id>/edit/', edit_profile_view, name='edit'),
]
```

6. Adding the link to the edit profile page in the `profile.html` file in the `account/templates/account` directory:

*In order to access the edit profile page, we need to add a link to the edit profile page in the profile page. In there looking for `<a>` tag with `Update` text:* 

```html
...
<!-- If Auth user is viewing their own profile -->
{% if is_self %}
	<a href="{% url 'account:edit' user_id=id %}">Update</a></br>
	...
{% endif %}
...
```

*This will allow us to access the edit profile page at `http://localhost:8000/profile/edit`. From the profile page, we can click on the `Update` link to access the edit profile page*  

*This shall allow us to update the profile image, email address, username.*

**NOTE**: *Update image functionality is quite basic and can be improved. For example, the user can crop the image, as well as the experience of uploading the image can be improved.*  

*However, that would require implementing considerable amount of javascript logic on the client side (web browser) using external libraries, as well as python functions on the backend to be able to crop the image and save it.*  

*This is not an obligatory part of this project.*  

*For now, we will keep it simple and focus on the Django python backend.*


## ***FRIENDS SYSTEM***

### ***ADDING FRIENDS APP***

*The friends system will be managed by a separate app `friends` in the Django project. The friends app will be used to manage the friend requests, friends, and messages between friends.*  

1. Creating a new app named `friends`:

```bash
python manage.py startapp friends
```

2. Adding the `friends` app to the `INSTALLED_APPS` list in the `main/settings.py` file:

```python
...
INSTALLED_APPS = [
	...
	'friends',
]
...
```

3. Creating the `models.py` file in the `friends` app directory:

*Here we will create the `FriendList` model to store the friends of the user, the `FriendRequest` model to store the friend requests.*  

```python
from django.db import models
from django.conf import settings
from django.utils import timezone

class FriendList(models.Model):
	# This is the account who owns the friend list (one user has one friend list)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

	# This is the list of friends (many users have many friends)
	friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

	def __str__(self):
		return self.user.username
	
	def add_friend(self, account):
		if not account in self.friends.all():
			self.friends.add(account)
			self.save()
	
	def remove_friend(self, account):
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, to_be_removed):
		initiator_friends_list = self # This is the user who originally initiated the removal
		initiator_friends_list.remove_friend(to_be_removed)

		# Remove the initiator from the to_be_removed user's friend list
		friend_list = FriendList.objects.get(user=to_be_removed)
		friend_list.remove_friend(initiator_friends_list.user)	
	
	def is_mutual_friend(self, friend):
		if friend in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
	is_active = models.BooleanField(blank=False, null=False, default=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username
	
	def accept(self):
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		self.is_active = False
		self.save()

	def cancel(self):
		self.is_active = False
		self.save()
```

**NOTE**: *The `FriendList` table shall be created as soon as new user is created. So, we would need to add another function to the `Account` model later.*  


4. Adding a class `FriendListAdmin` to the `friends/admin.py` file:

*This class will be used to display the `FriendList` model in the Django admin page*

```python
from django.contrib import admin
from friends.models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
	list_filter = ['user']
	list_display = ['user']
	search_fields = ['user']
	readonly_fields = ['user']

	class Meta:
		model = FriendList

admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
	list_filter = ['sender', 'receiver']
	list_display = ['sender', 'receiver']
	search_fields = ['sender__username', 'sender__email', 'receiver__username', 'receiver__email']

	class Meta:
		model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)
```

5. Making migrations and migrating the database:

```bash
python manage.py makemigrations

python manage.py migrate
```

*At this point, the `FriendList` and `FriendRequest` models will be created in the database*  
*Respective `Friend list` and `Friend requests` sections can be seen in the admin pannel*  


### ***SENDING FRIEND REQUESTS***

*This will be the logic to view the profile page from the friends perspective:*
--> `is_self`: 
`True`: *..user is viewing their own profile page*  
`False`: *..user is viewing the profile page of another user*  
--> `is_friend`:  
`True`: *..user is viewing the profile page of a friend*  
`False`: *..user is not viewing the profile page of a NON-friend*   
- `NO_REQUEST_SENT`: *..no friend request has been sent to this user*
- `SENT_BY_YOU`: *..you have sent a friend request to this user*  
- `THEY_SENT_TO_YOU`: *..this user has sent a friend request to you*  

So, there will be 5 possible states of the profile page:  
1. `is_self` = `True` - *..user is viewing their own profile page*  
2. `is_friend` = `True` - *..user is viewing the profile page of a friend*  
3. `is_friend` = `False` = `NO_REQUEST_SENT` - *..user is not viewing the profile page of a NON-friend*  
4. `is_friend` = `False` = `SENT_BY_YOU` - *..you have sent a friend request to this user*  
5. `is_friend` = `False` = `THEY_SENT_TO_YOU` - *..this user has sent a friend request to you*  


#### ***ADDING FRIEND REQUEST FUNCTIONALITY***

1. Creating new file in `friends` app directory named `friend_request_status.py`:

in `friends/friend_request_status.py` file:  

```python
from enum import Enum

class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = 0
	SENT_BY_YOU = 1
	THEY_SENT_TO_YOU = 2
```

2. Creating a utility function to get the friend request status in the `friends/utils.py` file:

```python
from frineds.models import FriendRequest

def get_friend_request_or_false(sender, receiver):
	try:
		friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
		return friend_request
	except FriendRequest.DoesNotExist:
		return False

```

3. Adding / changing the `profile_view` function in the `account/views.py` file:

*So, in the `account/views.py` file, we will add the logic to get the friend request status in the `profile_view` function*  

*This is how the `profile_view` function can look like at this point:*  

```python
...
from friends.utils import get_friend_request_or_false
from friends.friend_request_status import FriendRequestStatus
from friends.models import FriendList, FriendRequest
...
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
					request_sent = FriendRequestStatus.SENT_BY_YOU.value
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

```

4. Updating the `profile.html` file in the `account/templates/account` directory:  

*This is how the `profile.html` file can look like at this point:*  

```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}

<img src="{{ request.user.profile_image.url }}" alt="Profile Image" width="64" height="64">
<p>Email</p>
{%  if is_self %}
	<h5>{{ email }}</h5>
{% else %}
	{% if hide_email %}
		<h5>**********</h5>
	{% else %}
		<h5>{{ email }}</h5>
	{% endif %}
{% endif %}
<p>Username</p>
<h5>{{ username }}</h5>

<!-- If Auth user is viewing their own profile -->
{% if is_self %}
	<a href="{% url 'account:edit' user_id=id %}">Update</a></br>
	<a href="{% url 'password_change' %}">Change password</a></br>
{% endif %}

{% if request.user.is_authenticated %}

	<!-- THEM to YOU -->
	{% if request_sent == 2 %}
	<div>
		<span>Accept Friend Request</span>
		<span id="id_cancel_{{id}}" onclick='triggerDeclineFriendRequest("{{ pending_friend_request_id }}")'>cancel</span>
		<span id="id_confirm_{{id}}" onclick='triggerAcceptFriendRequest("{{ pending_friend_request_id }}")'>check</span>
	</div>
	{% endif %}

	<!-- Cancel Friend Request / Send Friend Request / Remove Friend -->
	{% if is_friend == False and is_self == False %}
		<!-- You sent them a request -->
		{% if request_sent == 1 %}
			<button> Cancel Friend Request </button></br>
		{% endif %}
		<!-- No requests have been sent -->
		{% if request_sent == 0 %}
			<button> Send Friend Request </button></br>
		{% endif %}
	{% endif %}
		
	{% if is_friend %}
		<button> Friends </button>
		<a href="#" onclick="removeFriend('{{ id }}', onFriendRemoved)">Unfriend</a>
	{% endif %}
	
	<!-- Friend list link --><br>
	<a href="#">
		<span> contact_page </span></br>
		<span> Friends ({{ friends|length }}) </span></br>
	</a>

	{% if friend_request %}
	<!-- Friend requests -->
		<a href="#">
			<span> person_add </span></br>
			<span> Friend Requests ({{ friend_request|length }}) </span></br>
		</a>
	{% endif %}

	{% if is_friend %}
		<div onclick="createOrReturnPrivateChat('{{ id }}')">
			<span> message </span></br>
			<span> Message </span></br>
		</div>
	{% endif %}

{% endif %}
	
{% endblock content %}

```

*At this point, we can see the profile page given its current state. We also can visit the profile page of another user and see the appropriate friend request button.*  

*Next step would be to add the functionality and logic to send the friend request*  


#### ***SENDING FRIEND REQUESTS FUNCTIONALITY***  

1. Creating the forms which correspond to each of the friend request actions in the `friends/forms.py` file:

*First creating `friends/forms.py` file in the `friends` app directory:*  

```python
from django import forms
from friends.models import FriendRequest
from django.contrib.auth import get_user_model


User = get_user_model()

class SendFriendRequestForm(forms.Form):
	receiver = forms.ModelChoiceField(queryset=User.objects.all())


class HandleFriendRequestForm(forms.Form):
	friend_request_id = forms.ModelChoiceField(queryset=FriendRequest.objects.all())

```

2. Adding respective views to the `friends/views.py` file:

```python
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from friends.forms import SendFriendRequestForm, HandleFriendRequestForm
from friends.models import FriendRequest


def send_friend_request_view(request):
	if request.method == 'POST':
		form = SendFriendRequestForm(request.POST)
		if form.is_valid():
			receiver = form.cleaned_data.get('receiver')
			FriendRequest.objects.create(sender=request.user, receiver=receiver)
			messages.success(request, f'Friend request sent to {receiver.username}')
			return redirect('profile')
		else:
			return HttpResponse('Invalid form data')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('profile')

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

def cancel_friend_request_view(request):
	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request = form.cleaned_data.get('friend_request_id')
			friend_request.cancel()
			messages.success(request, f'Friend request cancelled')
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

```
**NOTE: LIKELY THE LOGIC IN THESE VIEWS MUST BE CHANGED SINCE THE SEND FRIEND REQUEST WONT WORK AS EXPECTED**

3. Including the forms to the `profile.html` file in the `account/templates/account` directory:

```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}

{% if messages %}
	{% for message in messages %}
		<li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
			{{ message }}
		</li>
	{% endfor %}
{% endif %}

<img src="{{ request.user.profile_image.url }}" alt="Profile Image" width="64" height="64">
<p>Email</p>
{%  if is_self %}
	<h5>{{ email }}</h5>
{% else %}
	{% if hide_email %}
		<h5>**********</h5>
	{% else %}
		<h5>{{ email }}</h5>
	{% endif %}
{% endif %}
<p>Username</p>
<h5>{{ username }}</h5>

<!-- If Auth user is viewing their own profile -->
{% if is_self %}
	<a href="{% url 'account:edit' user_id=id %}">Update</a></br>
	<a href="{% url 'password_change' %}">Change password</a></br>
{% endif %}

{% if request.user.is_authenticated %}

	<!-- THEM to YOU -->
	{% if request_sent == 2 %}
	<div>
		<span>Accept Friend Request</span>
		<form method="POST" action="{% url 'friends:accept_friend_request' %}">
			{% csrf_token %}
			<input type="hidden" name="friend_request_id" value="{{ pending_friend_request_id }}">
			<input type="submit" value="Accept">
		</form>
		<form method="POST" action="{% url 'friends:decline_friend_request' %}">
			{% csrf_token %}
			<input type="hidden" name="friend_request_id" value="{{ pending_friend_request_id }}">
			<input type="submit" value="Decline">
		</form>
	</div>
	{% endif %}

	<!-- Cancel Friend Request / Send Friend Request / Remove Friend -->
	{% if is_friend == False and is_self == False %}
		<!-- You sent them a request -->
		{% if request_sent == 1 %}
			<form method="POST" action="{% url 'friends:cancel_friend_request' %}">
				{% csrf_token %}
				<input type="hidden" name="friend_request_id" value="{{ pending_friend_request_id }}">
				<input type="submit" value="Cancel Friend Request">
			</form>
		{% endif %}

		<!-- No requests have been sent -->
		{% if request_sent == 0 %}
			<form method="POST" action="{% url 'friends:send_friend_request' %}">
				{% csrf_token %}
				<input type="hidden" name="receiver_id" value="{{ id }}">
				<input type="submit" value="Send Friend Request">
			</form>
		{% endif %}
	{% endif %}
		
	{% if is_friend %}
		<button> Friends </button>
		<form method="POST" action="{% url 'friends:remove_friend' %}">
			{% csrf_token %}
			<input type="hidden" name="friend_id" value="{{ id }}">
			<input type="submit" value="Unfriend">
		</form>
	{% endif %}
	
	<!-- Friend list link --><br>
	<a href="#">
		<span> contact_page </span></br>
		<span> Friends ({{ friends|length }}) </span></br>
	</a>

	{% if friend_request %}
	<!-- Friend requests -->
		<a href="#">
			<span> person_add </span></br>
			<span> Friend Requests ({{ friend_request|length }}) </span></br>
		</a>
	{% endif %}

	{% if is_friend %}
		<div onclick="createOrReturnPrivateChat('{{ id }}')">
			<span> message </span></br>
			<span> Message </span></br>
		</div>
	{% endif %}

{% endif %}
	
{% endblock content %}
```

4. Creating the `friends/urls.py` file in the `friends` app directory:

```python
from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
	path('send-friend-request/', views.send_friend_request_view, name='send_friend_request'),
	path('accept-friend-request/', views.accept_friend_request_view, name='accept_friend_request'),
	path('decline-friend-request/', views.decline_friend_request_view, name='decline_friend_request'),
	path('cancel-friend-request/', views.cancel_friend_request_view, name='cancel_friend_request'),
	path('remove-friend/', views.remove_friend_view, name='remove_friend'),
]
```

5. Adding the reference to the `friends` app urls in the `main/urls.py` file:

```python
...
urlpatterns = [
	...
	path('friends/', include('friends.urls', namespace='friends')),
	...
]
```

**NOTE: THIS VERSION IS NOT WORKING AS EXPECTED.. YET..**





