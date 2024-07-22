# USER MANAGEMENT SYSTEM

This repository contains the code for the tutorial on how to create a custom user model in Django. The tutorial covers the following topics:

- Creating a new Django project
- Adding a new apps to the project
- Creating templates
- Adding and referencing static files
- Adding default profile image
- Building a custom user model
- Handling case-insensitive input with backends model
- Custom forms for registration and login pages
- Password reset functionality
- Profile page with personal info update functionality



# CREATING NEW DJANGO PROJECT

*Assuming `python` and `pipenv` are installed.*

## To run the project from this repository:

*If you want to run the project from this repository, follow the steps below to set up the environment and run the server*  

*1. Clone the repo and install the dependencies.*

```bash
pipenv install requirements.txt
```

*2. Run the server*

```bash
python manage.py runserver
```


## To follow along this tutorial:

*1. **Creating new directory for the project and install Django with pipenv***

```bash
mkdir custom_user_model
cd custom_user_model

pipenv shell
pipenv install django
```

*The following package is for the `ImageField` in the Custom User Model section:*  

```bash
pipenv install Pillow
```

*2. **Create a new Django project***

```bash
django-admin startproject main .
```
*This will create a new Django project in the current directory with the name `main`*  


**NOTE**: *The following command can be used at any point or whenever additional packages are installed to save the requirements of the project to a file named `requirements.txt`. This helps to track the dependencies of the project as well as to install the same dependencies at once in a new environment*

```bash
pip freeze > requirements.txt
```


## Creating Homepage App and Templates

*1. **Creating new app to handle the homepage***

```bash
python manage.py startapp homepage
```

*2. **Adding the `homepage` app to the `INSTALLED_APPS` list in the `main/settings.py` file:***

```python
INSTALLED_APPS = [
	...
	'homepage',
]
```

*3. **Create a new directory named `templates` at the same level with `manage.py` file***

```bash
mkdir templates
```

*4. **Create new directories named `homepage/templates` and `homepage/templates/homepage`:***

```bash
mkdir homepage/templates
mkdir homepage/templates/homepage
``` 

*5. **Add the `templates` directory to the `DIRS` list***

*In the `main/settings.py` file:*

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

**NOTE:** *This will allow Django to look for templates in the main `templates` directory as well as `templates` in the app directories*  

*6. **Create a `layout.html` file in the main `templates` directory:***

**NOTE**: *We will breake down the `layout.html` file into smaller parts by adding `header.html`, `footer.html` files in the `templates` directory as well. This will make the `layout.html` file cleaner and easier to read*  

*6.1. In `templates/layout.html` file:*

```html
<!DOCTYPE html>
<html lang=en>

<head>
    <meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
</head>

<body>
	{% include 'header.html' %}

	<div>
		{% block content %}

		{% endblock content %}
	</div>

	{% include 'footer.html' %}
</body>

</html>

```

**NOTE**:  
- *The `{% block content %}` and `{% endblock content %}` are used to define the content of the page in the child templates, which will be created later*    
- *The `{% include .. %}` is used to extend the `layout.html` file with the `header.html` and `footer.html` files*  


*6.2. In `templates/header.html` file:*

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

	{% if request.user.is_authenticated %}

	{% else %}

	{% endif %}

</nav>

```

**NOTE**:  
*The `<style>` block is just a basic styling for the top navigation bar (for it not to look too ugly). This shall be styled properly with Bootstrap or CSS as a part of the frontend module*  
*In the `<nav>` block we will add the links to the homepage, login, register, profile, logout pages, which shall appear based on the user authentication status*  


- *In `templates/footer.html` file:*

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

*Just an example*  


*7. **Creating `home.html` file.***

*In `homepage/templates/homepage/home.html` file:*

```html
{% extends 'layout.html' %}

{% block content %}
	<h1>Welcome to the homepage</h1>
{% endblock content %}
```

*8. **Adding `home_view` function***

*In the `homepage/views.py` file:*

```python
from django.shortcuts import render

def home_view(request, *args, **kwargs):
	context = {} # ..for illustration purposes, this is how you pass data to the template
	return render(request, "home.html", context)
```

*9. **Adding reference to the `home_view` function in the `main/urls.py` file:***

*In the `main/urls.py` file:*  

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


# REFERENCING STATIC FILES

## Setting Up Static Files Directory

**NOTE**: *Here are the official Django docs for [static files](https://docs.djangoproject.com/en/5.0/howto/static-files/)*


*1. **Adding the following to the bottom of the `main/settings.py` file:***

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

*2. **Adding the following to the `main/urls.py` file:***

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

**NOTE:** *This is to tell Django to serve the static files in the `static` directory*  


*3. **Create directories to serve static and media files:***

```bash
mkdir static
mkdir static_cdn
mkdir media
mkdir media_cdn
```

**NOTE** *`static_cdn` and `media_cdn` directories are an example of the directories where the static and media files will be stored when the project is deployed. `_cdn` directories are created once the following command is run in the production environment:*  

```bash
python manage.py collectstatic
```

*By creating `static_cdn` and `media_cdn` directories, we can test the availability of the static files in the project in the development environment. (No need to run the `collectstatic` for now).*


*4. **Adding `load static` to the top of the `layout.html` and `header.html` files in the `templates` directory:***

```html
{% load static %}
...
```

**NOTE:**  
- *This line needs to be added to all the html files where the static files are used. To `layout.html` as well as to the `header.html` and `footer.html` files if the static files are referenced there.*
- *This will allow us to use the static files (img, css, js etc) in the project*  



# USING STATIC IMAGES

*1. **Create a new directory named `images` in the `static` directory:***

```bash
mkdir static/images
```


*2. **Add the images of choice to the `static/images` directory:***

*For example, [emoticon smile icon](https://www.iconexperience.com/o_collection/icons/?icon=emoticon_smile)*  


*3. **Adding the image to the html file of choice:***

*Adding the image to the navigation bar in the `header.html` to display the image which will redirect to the profile page (which doesn't exist yet)*  

*In the `templates/header.html` file:*

```html
...
<nav>

	{% if request.user.is_authenticated %}
		<a href="/profile" title="PROFILE"> <img src="{% static 'images/smile_32-32.png' %}"> </a>
	{% else %}

	{% endif %}

</nav>
```


## Adding Default Profile Image

*1. **Create a new directory named `profile_images` in the `media_cdn` directory:***

```bash
mkdir media_cdn/profile_images
```

*This will be used to store the profile images of all users*  


*2. **Add the `default.png` image to the `media_cdn/profile_images` directory:***

*This will be used as the default profile image for the users who don't upload their own profile image*  

*For example, [this image](https://www.iconninja.com/avatar-anonym-person-user-default-unknown-head-icon-15892) can be used as the default profile image.*  

**NOTE:** *We will be able to test the availability of the default profile picture later in Custom User Model section*  


## Using Goggle Icons

**Optional** *This part can be skipped.*
*However, it might be a nice touch, let alone the all the fun..*

*1. **Getting the link to the google icons.***

- Go to the [Google Icons](https://fonts.google.com/icons) website
- Visit the respective GitHub repository for the icons [here](https://github.com/google/material-design-icons)
- Copy the link to the icons : 

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
```

**NOTE**: *verify if this is the right link.. for me the second link in the repo worked not the 1st one*


*2. **Adding the link to the `layout.html` file in the `templates` directory:***

*In the header of the `layout.html` file:*  

```html
...
<head>
	...
	<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
</head>
...
```

*Now the google icons can be used in the project*  


*3. **Example of the link to the `Home` icon.***

*Adding the `Home` icon to the navigation bar in the `templates/header.html` file:*

```html
...
<nav>
	<a href="/" title="HOME">
	<span class="material-symbols-outlined">home</span>
	</a>

	{% if request.user.is_authenticated %}
	...
</nav>
```

*This will display the `Home` icon which is clickable and will redirect to the home page*  

**NOTE:**    
- *To add any other icons simply use the name of the icon in the `<span ..>` tag*  
- *Complete `<span ..>` tag is available on [Google Icons](https://fonts.google.com/icons) website. When any icon is clicked, there will be a `<span ..>` tag on the right side panel in the `Inserting the icon` section*  



# BUILDING CUSTOM USER MODEL

**NOTE**: *If curious, take a look at the original `AstractBaseUser` and `BaseUserManager` models on the [Django GitHub](https://github.com/django/django/blob/main/django/contrib/auth/base_user.py)*


*1. **Create a new Django app:***

```bash
python manage.py startapp account
```

*This will create a new Django app in the project directory with the directory name `account`*

**NOTE: *If another `app_name` is used, make sure to replace `account` with the `app_name` in the following steps, (where necessary)***


*2. **Add the app to the installed apps in the `main/settings.py` file***

*Also adding the necessary parameter to tell Django to use our custom user model*

*In the `main/settings.py` file:*

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


*3. **Create a Custom User Model***

*In the `account/models.py` file:*

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
	profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
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

**Note**:  
- *`ImageField` is a part of the `Pillow` library. So, make sure it is installed before running the server.*  


*4. **Add the custom user model to the `account/admin.py` file:***

*This will allow us to see the custom user model in the admin page and all the fields we specified*  

*In the `account/admin.py` file:*

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

**NOTE:** *This is needed to be able to view the Custom User Model in the admin page.*


*5. **Making migrations:***

```bash
python manage.py makemigrations
python manage.py migrate
```
*This will create the necessary migrations for the custom user model and apply them to the database*


*6. **Create a superuser:***

```bash
python manage.py createsuperuser
```

**NOTE**:  
- *This is necessary step that allows to login to the admin page*  
- *`createsuperuser` command will use the custom user model we created to create the superuser, where `email` will be used to login the user*    


*7. **Run the server:***

```bash
python manage.py runserver
```

**Note:**  
- *now we can login to the admin panel and see the custom user model we created with the fields we specified.*  
- *user email will be used to login the user and the username will be displayed in the admin page*  
- *default profile image (stored in the `media_cdn/profile_images` directory) shall be displayed via link in the admin page in the `Change account` --> `Profile Image` section once we click on the account email* 



# SETTING UP PROFILE IMAGE

*The following code will display the profile image of the user in the navigation bar on the homepage if the user is authenticated.*

*Adding the following code to the `header.html` file in the `templates` directory:*

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

**NOTE**:  
- *We dont have yet the profile page nor the login page, so to check if the profile image (default.png) is displayed in the navigation bar, we can login to the admin page and then navigate to `http://localhost:8000`*
- *This should display the profile image as well as show the username of the user and the link to the current profile image in the browser window*  



# HANDLING CASE-INSENSITIVE INPUT

*This functionality ensures that the user can login with the email or username in any case. For this to work, we need to create a custom authentication backend module to handle the authentication process with case-insensitive email and username*  

*1. **Create a custom authentication backend class.***

*In the `account/backends.py` file:*  

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

*2. **Add the custom authentication backend to the `main/settings.py` file:***  

```python
# after the AUTH_USER_MODEL adding the custom authentication backend
AUTH_USER_MODEL = 'account.Account'
AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.AllowAllUsersModelBackend',
	'account.backends.CaseInsensitiveModelBackend',
]
```

*This will allow us to authenticate the user if the email or username is entered in either upper or lower case*  


# REGISTRATION

## Adding Registration Page

*1. **Creating the followign new directory: `account/templates/account` and adding the `register.html` in there:***

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
		<input type="password" name="password1" placeholder="Password" required></br>
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


*2. **Creating the `RegistrationForm`***

*First we create new file named `forms.py` in the `account` app directory and add the following class. So, in the `account/forms.py` file:***

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


*3. **Adding the `register_view` function.***

*This function will handle the registration process and render the `register.html` template.*  

*In the `account/views.py` file:*

```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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


*4. **Adding the reference to the `register_view` function in the `main/urls.py` file:***

```python
...
from account.views import register_view

urlpatterns = [
	...
	path('register/', register_view, name='register'),
]
...
```


*5. **Adding the link to the registration page.*** 

*In the `templates/header.html` file:*  

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
```

**NOTE**:  
- *This will allow us to access the registration page at `http://localhost:8000/register` directly from the homepage*  
- *Also if there is an error pops up when trying to delete the user from the admin page.. this will be fixed later*  



# LOGIN AND LOGOUT

*1. **Creating the `login.html` file***

*In the `account/templates/account/login.html` file:*

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


*2. **Creating Authentication Form***

*This class will be used to create the login form*

*In the `account/forms.py` file:*   

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

*3. **Adding the `login_view` function***

*This function will handle the login process and render the `login.html` template*

*In the `account/views.py` file:*  

```python
from django.contrib.auth import authenticate, login, logout

from account.forms import RegistrationForm, AccountAuthenticationForm
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

**NOTE:**  
- *Make sure the proper imports are added on the top of the file : `from django.contrib.auth import authenticate, login, logout` !*  
- *Make sure to include the new form : `AccountAuthenticationForm` as well*  


*4. **Adding the reference to the `login_view` function in the `main/urls.py` file:***

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


*5. **Adding the link to the login page.*** 

*In the `templates/header.html` file:***

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
```

*This will allow us to access the login page at `http://localhost:8000/login` directly from the homepage. As well as to show the `Logout` option*



# PASSWORD RESET

**NOTE**:  
- *Resetting the password in the development environment is different from the production environment.*  
- *In the development environment, the password reset link will be displayed in the console.*  
- *In the production environment, the password reset link will be sent to the user's email, and the process is different*   

***The following steps will be done in the development environment:***


*1. **Adding the `password_reset` directory in the `templates` which is at the same level as the `account` app directory:***

```bash
mkdir templates/password_reset
```


*2. **Addting several files in the `password_reset` directory:***  
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

*3. **Adding the following urls to the `main/urls.py` file:***

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


*4. **Adding the necessary settings to the `main/settings.py` file:***


```python
...
DEBUG = True # After the DEBUG setting

if DEBUG:
	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # This will display the password reset link in the terminal window
...
```

**NOTE**:  
- *The following settings are valid for the development environment !!*
- *In the production environment, the settings are different. It will be necessary to set up the email server and send the actual email to the user.*
- *In the development environment, the password reset link will be displayed in the terminal window*  


*5. **Updating the reference link in the `login.html`***

*In the `account/templates/account/login.html` file:*

```html
{% block content %}
	...

	<div>
		<a href="{% url 'password_reset' %}">Reset password?</a>
	</div>
{% endblock content %}
```

*This shall be it for the password reset pages. The password reset link will be displayed in the terminal window when the user enters the email address in the password reset form*.  



# PROFILE PAGE

***Profile page logic:***  

*Profile page will be used to display the user's profile information as well as to update the profile image.  etc.*  

*Also profile page can have several states and functionalities :* 

- **is_self**: *This is where the user is viewing their own profile page and can change the profile image, password, link to friends..*
- **is_user**: *This is where the user is viewing the profile page of another user and can send friend request..*  
- **is_friend**: *This is where the user is viewing the profile page of a friend and can send messages, remove friend..*

**NOTE**: *We will implement the simple functionality of the profile page based on two events*:  
- *The user is viewing their own profile page*
- *The user is viewing the profile page of another user*


*1. **Creating `profile.html` file***

*In `account/templates/account/profile.html` file:***

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
		<span>cancel</span>
		<span>check</span>
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
		<a href="#">Unfriend</a>
	{% endif %}
	
	<!-- TODO -->
	<!-- Friend list link -->
	<a href="#">
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
		<span> Message </span></br>
	{% endif %}

{% endif %}
{% endblock content %}

```

**NOTE**:  
- *Most of the logic in the `profile.html` is not implemented yet. Those are just placeholders for the future functionalities*  


*2. **Adding the `profile_view` function.***

*In `account/views.py` file:*  

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


*3. **Adding new url file in the `account` app directory named `urls.py`:***

*In the `account/urls.py` file:*

```python
from django.urls import path
from account.views import profile_view

app_name = 'account'

urlpatterns = [
	path('<user_id>/', profile_view, name='profile'),
]

``` 
**NOTE**:  
- *`<user_id>/` is a dynamic URL pattern that will be passed to the `profile_view` function in the `account/views.py` file.*  
- *`name` attribute is used to reference this URL pattern in the Django templates.*  
- *`app_name` attribute is used to namespace the URL pattern. This is useful when you have multiple apps in your Django project and you want to avoid naming conflicts between URL patterns.*  
- *`app_name`: `account` attribute is used in the `main/urls.py` file to include the URL patterns from this file.*  


*4. **Adding the reference to the account urls in the `main/urls.py` file:***

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


*5. **Adding the link to the profile page*** 

*In the `templates/header.html` directory (this is how the navbar block might look like at this point):***

```html
...
<nav>
	<a href="/" title="HOME"> <span class="material-symbols-outlined">home</span></a>

	{% if request.user.is_authenticated %}
		<a href="{% url 'account:profile' user_id=request.user.id %}" title="PROFILE"> 
			<img src="{{ request.user.profile_image.url }}" alt="LOGO" width="40" height="40">
		</a>

		<a href="{% url 'logout' %}" title="LOGOUT"> <span class="material-symbols-outlined">logout</span>Logout</a>
	{% else %}
		<a href="{% url 'login' %}" title="LOGIN"> <span class="material-symbols-outlined">login</span>Login</a>
		<a href="{% url 'register' %}" title="REGISTER"> <span class="material-symbols-outlined">person_add</span>Register</a>
	{% endif %}
</nav>
```

**NOTE**:  
- *`account:profile` is the namespace of the URL pattern we created in the `account/urls.py` file*  
- *`account` is the app name indicated both in the `account/urls.py` as `app_name = 'account'` and in the `main/urls.py` as `namespace='account'`*  
- *`profile` is the name of the URL pattern we created in the `account/urls.py` file*  
- *We can access the profile page by clicking on the profile image in the navigation bar, once the user is logged in*  



# USER SEARCH

***IMPLEMENTING USER SEARCH***  

*This will allow the user to search for other users by their username or email address. The search results will be displayed in the search page*  

*1. **Creating the `search_results.html` file***

*In the `account/templates/account/search_results.html` file:*

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
				<a href="#">Send a Message</a>
			{% endif %}
		</a>

		{% if account.1 %} <!-- If friends -->
			<p> Friends </p>
		{% else %}
			{% if account.0 !=  request.user %} <!-- If not friends -->
				<p> Not Friends </p>
			{% endif %}
		{% endif %}

		{% if account.0 == request.user %} <!-- If you -->
			<p> This is you </p>
		{% endif %}

	{% if forloop.counter|divisibleby:2 %} <!-- If even.. `forloop.counter` is to access the index -->
		<!-- <br> -->
	{% endif %}
	
	{% endfor %}
	
	{% else %} <!-- If no friends -->
		<p> No results </p>
{% endif %}

{% endblock content %}
```


*2. **Adding the `account_search_view` function***

*In the `account/views.py` file:*

```python
...
def account_search_view(request, *args, **kwargs):
	context = {}

	if request.method == 'GET':
		search_query = request.GET.get('q', '') # ..getting the search query from the URL (will default to an empty string if none)
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

*3. **Adding the reference to the `account_search_view` function***

*In the `main/urls.py` file:*

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

**NOTE:** *Make sure to add all the necessary imports in the `account/views.py` file.*  


*4. **Modifying the navbar to show the search bar.***

*This is how the `templates/header.html` file can look like at this point:*

```html
{% load static %}
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
		<a href="{% url 'account:profile' user_id=request.user.id %}" title="PROFILE"> 
			<img src="{{ request.user.profile_image.url }}" alt="LOGO" width="32" height="32">
			{{ request.user.username }}
		</a>

		<a href="{% url 'logout' %}" title="LOGOUT"> 
			<span class="material-symbols-outlined">logout</span>
			Logout
		</a>
	{% else %}
		<a href="{% url 'login' %}" title="LOGIN"> <span class="material-symbols-outlined">login</span>Login</a>
		<a href="{% url 'register' %}" title="REGISTER"> <span class="material-symbols-outlined">person_add</span>Register</a>
	{% endif %}

</nav>
```

**NOTE:**  
- *The `<form..>` tag in header is used to create a search bar in the navigation bar.*  
- *The search bar will be used to search for other users by their username or email address*  


***Also, this is how the `templates/layout.html` file can look like at this point:***

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

*At this point, we can use the search bar in the navigation bar to search for other users by their username or email.*  



# EDIT ACCOUNT FUNCTIONALITY

*This will allow the user to edit their account information, such as the email address, username, and profile image. The user will be able to update their account information in the edit account page*  

*1. **Creating the `edit_profile.html` file***

*In the `account/templates/account/edit_profile.html` file:*  

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
	<input type="email" name="email" id="id_input_email" placeholder="Email address" required autofocus value={{ form.initial.email }}> 
	<label>
		<input type="checkbox" name="hide_email" id="id_input_hide_email"
		{% if form.initial.hide_email %}
			checked
		{%endif%}>
		Hide Email
	</label>

	<h6 class="mt-4 field-heading">Username</h6>
	<input type="text" name="username" id="id_input_username" placeholder="Username" required value="{{ form.initial.username }}">

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


*2. **Adding `AccountUpdateForm` class to the `account/forms.py` file:***

*In the `account/forms.py` file:*

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


*3. **Adding the `edit_profile_view` function***

*In the `account/views.py` file:*

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


*4. **Adding a global variable to the `main/settings.py` file:***

*This is used to limit the size of the profile image that the user can upload to the server.*

```python
...
# This is to set a global variable for the maximum size of the uploaded profile image (5MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
``` 

*5. **Adding the reference to the `edit_account_view` function***

*In the `account/urls.py` file:*

```python
...
from account.views import profile_view, edit_profile_view # adding the edit_profile_view function
...

urlpatterns = [
	...
	path('<user_id>/edit/', edit_profile_view, name='edit'),
]
```

*6. **Adding the link to the edit profile page in the `profile.html` file***

*In the `account/templates/account/profile.html` file:*

*..looking for `<a>` tag with `Update` text in it:* 

```html
...
<!-- If Auth user is viewing their own profile -->
{% if is_self %}
	<a href="{% url 'account:edit' user_id=id %}">Update</a></br>
	...
{% endif %}
...
```

**NOTE:**  
- *This will allow access the edit profile page by clicking on the `Update` link on the profile page*  
- *This shall allow us to update the profile image, email address, username.*  



# IMPLEMENTING FRIENDS SYSTEM

*We will manage friends system in a separate django app `friends`.*  

*1. **Creating a new app named `friends`:***

```bash
python manage.py startapp friends
```

*2. **Adding the `friends` app to the `INSTALLED_APPS` list.***

*In the `main/settings.py` file:*

```python
...
INSTALLED_APPS = [
	...
	'friends',
]
...
```


# FRIENDS MODEL

*1. **Creating the `models.py` file in the `friends` app directory.***

*Here we will create the `FriendList` model to store the friends of the user, the `FriendRequest` model to store the friend requests.*  

*In the `friends/models.py` file:*

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

**NOTE:**  
- *The `FriendList` table shall be created as soon as new user is created. We would need to add another function to the `Account` model later.*  
- *Each friend request will be saved in the `FriendRequest` table.*
- *`is_active` field will be used to determine if the friend request is active or not.*
- *If friend request is active, it means that the request has not been accepted or declined yet.*
- *All requests will be available in the `FriendRequest` table, in database, even if they are declined or canceled.*    


*2. **Adding `FriendListAdmin` class to the `friends/admin.py` file:***

*This class will be used to display the `FriendList` model in the Django admin page*

*In the `friends/admin.py` file:*

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


*3. **Making migrations and migrating the database:***

```bash
python manage.py makemigrations

python manage.py migrate
```

**NOTE:**  
- *At this point, the `FriendList` and `FriendRequest` models will be created in the database*  
- *Respective `Friend list` and `Friend requests` sections can be seen on the admin pannel*  



# FRIENDS SYSTEM STRUCTURE AND LOGIC

***The following will be our logic to view the profile page from the friends system perspective:***   
--> if `is_self`:   
`True`: *..user is viewing their own profile page*    
`False`: *..user is viewing the profile page of another user*    
--> if `is_friend`:  
`True`: *..user is viewing the profile page of a friend*  
`False`: *..user is not viewing the profile page of a NON-friend*   
- `NO_REQUEST_SENT`: *..no friend request has been sent to this user*
- `SENT_BY_YOU`: *..you have sent a friend request to this user*  
- `THEY_SENT_TO_YOU`: *..this user has sent a friend request to you*  

***Given this logic, there will be 5 possible states to view the profile page:***    
1. `is_self` = `True` - *..user is viewing their own profile page*  
2. `is_friend` = `True` - *..user is viewing the profile page of a friend*  
3. `is_friend` = `False` = `NO_REQUEST_SENT` - *..user is not viewing the profile page of a NON-friend*  
4. `is_friend` = `False` = `SENT_BY_YOU` - *..you have sent a friend request to this user*  
5. `is_friend` = `False` = `THEY_SENT_TO_YOU` - *..this user has sent a friend request to you*  



# PROFILE VIEW FUNCTIONALITY

*1. **Creating new file in `friends` app directory named `friend_request_status.py`:***

*In `friends/friend_request_status.py` file:*  

```python
from enum import Enum

class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = 0
	SENT_BY_YOU = 1
	THEY_SENT_TO_YOU = 2
```

*This will represent the status of the friend request*  


*2. **Creating a utility function to get the friend request status***

*Creating new file `friends/utils.py` with the following function:*  

```python
from frineds.models import FriendRequest

def get_friend_request_or_false(sender, receiver):
	try:
		friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
		return friend_request
	except FriendRequest.DoesNotExist:
		return False

```


*3. **Adding / changing the `profile_view` function***

*We are adding the logic to get the friend request status in the `profile_view` function*  

*In the `account/views.py` file (this is how the `profile_view` function can look like at this point):*  

```python
...
from friends.utils import get_friend_request_or_false
from friends.friend_request_status import FriendRequestStatus
from friends.models import FriendList, FriendRequest
...
def profile_view(request, *args, **kwargs):
	context = {}
	user_id = kwargs.get('user_id')

	try:
		account = Account.objects.get(pk=user_id)
	except Account.DoesNotExist:
		return HttpResponse("User not found.")

	if account:
		context['id'] = account.id
		context['email'] = account.email
		context['username'] = account.username
		context['profile_image'] = account.profile_image
		context['hide_email'] = account.hide_email

		# determine the relationship status between the logged-in user and the user whose profile is being viewed
		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends

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
				pending_friend_request = get_friend_request_or_false(sender=account, receiver=user) 
				if pending_friend_request:
					request_sent = FriendRequestStatus.THEY_SENT_TO_YOU.value
					context['pending_friend_request_id'] = pending_friend_request.id

				# case 2: the user is not a friend and request status = `YOU_SENT_TO_THEM`	
				elif get_friend_request_or_false(sender=user, receiver=account) is not False:
					pending_friend_request = get_friend_request_or_false(sender=user, receiver=account)
					if pending_friend_request:
						request_sent = FriendRequestStatus.SENT_BY_YOU.value
						context['pending_friend_request_id'] = pending_friend_request.id

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

		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL
		context['request_sent'] = request_sent
		context['friend_request'] = friend_request

	return render(request, 'account/profile.html', context)
...
```

**NOTE:**  
- *At this point, we can not see the changes made on the profile page. Continue with the following section to add respective view functions.*



# SENDING FRIEND REQUEST

*1. **Creating the forms which correspond to each of the friend request actions.***

*First creating `friends/forms.py` file in the `friends` app directory.*  

*In the `friends/forms.py` file:*

```python
from django import forms
from friends.models import FriendRequest
from django.contrib.auth import get_user_model


User = get_user_model()

class SendFriendRequestForm(forms.Form):
	receiver = forms.ModelChoiceField(queryset=User.objects.all())

```

*2. **Adding respective views***

*In the `friends/views.py` file:*

```python
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from friends.forms import SendFriendRequestForm
from friends.models import FriendRequest


def send_friend_request_view(request):
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

```


*3. **Including the forms to the `profile.html` file.***

*In the `account/templates/account/profile.html` file:*  

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
	</br>
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
	<a href="{% url 'friends:friend_list' user_id=id %}">
		<span> Friends ({{ friends|length }}) </span></br>
	</a>
	<br>

	{% if friend_request %}
	<!-- Friend requests -->
		<a href="{% url 'friends:friend_requests' user_id=id %}">
			<span> Friend Requests ({{ friend_request|length }}) </span></br>
		</a>
	{% endif %}

	<br>
	{% if is_friend %}
		<span> Message </span></br>
	{% endif %}

{% endif %}
	
{% endblock content %}
```

*4. **Creating the `urls.py` file in the `friends` app directory:***

*In the `friends/urls.py` file:*  

```python
from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
	path('send-friend-request/', views.send_friend_request_view, name='send_friend_request'),
]
```


*5. **Adding the reference to the `friends` app in the `main/urls.py` file:***

```python
...
urlpatterns = [
	...
	path('friends/', include('friends.urls', namespace='friends')),
	...
]
```

**NOTE:**  
- *We can now send friend requests to other users by clicking on the `Send Friend Request` button on the profile page*  
- *At this point `send_friend_request_view` and `cancel_friend_request_view` functions should be working as expected.*



#### ***ADDING FRIEND REQUESTS PAGE***

*This will allow the user to view the friend requests that they have received and accept or decline or cancel the friend requests*  

1. Adding the `friend_requests_view` function to the `friends/views.py` file:

```python
from account.models import Account
...
def friend_requests_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get('user_id')
		account = Account.objects.get(pk=user_id)
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse("You can't view another user's friend requests.")
	else:
		redirect('login')		
	return render(request, 'friends/friend_requests.html', context)
...
```

2. Adding respective url to the `friends/urls.py` file:

```python
...
urlpatterns = [
	...
	path('friend-requests/<user_id>/', views.friend_requests_view, name='friend_requests'),
	...
]
```

3. Creating the `friend_requests.html` file in the `friends/templates/friends` directory:

```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}

{% if friend_requests_count %}
	{% for request in friend_requests_count %}
		<a href="{% url 'account:profile' user_id=request.sender.id %}">
			<img src="{{request.sender.profile_image.url}}" alt="">
		</a>
		<a href="{% url 'account:profile' user_id=request.sender.id %}">
			<h4>{{request.sender.username}}</h4>
		</a>
	{% endfor %}
	
	{% else %} <!-- If no friends -->
		<p>No results</p>
{% endif %}
	
{% endblock content %}


```

4. Adding the link to the friend requests page in the `profile.html` file in the `account/templates/account` directory:

```html
...
	{% if friend_request %}
	<!-- Friend requests -->
		<a href="{% url 'friends:friend_requests' user_id=id %}">
			<span> person_add </span></br>
			<span> Friend Requests ({{ friend_request|length }}) </span></br>
		</a>
	{% endif %}
...
```

*At this point, we can access the friend requests page at `http://localhost:8000/friends/friend-requests/<user_id>/` and view the friend requests that the user has received*  


#### ***CANCEL FRIEND REQUEST***

1. Adding the `cancel_friend_request_view` function to the `friends/views.py` file:

```python
...
def cancel_friend_request_view(request):
	# DEBUG #
	# print(request.POST)
	# # # # #
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
		return redirect('account:profile', user_id=request.user.id)
...
```

2. Adding the `HandleFriendRequestForm` class to the `friends/forms.py` file:

```python
...
class HandleFriendRequestForm(forms.Form):
	friend_request_id = forms.ModelChoiceField(queryset=FriendRequest.objects.all())
```

3. Adding the respective url to the `friends/urls.py` file:

```python
...
urlpatterns = [
	...
	path('cancel-friend-request/', views.cancel_friend_request_view, name='cancel_friend_request'),
	...
]
```


#### ***ACCEPT FRIEND REQUEST***

1. Adding the `accept_friend_request_view` function to the `friends/views.py` file:

```python
def accept_friend_request_view(request):
	if request.method == 'POST':
		form = HandleFriendRequestForm(request.POST)
		if form.is_valid():
			friend_request_id = form.cleaned_data.get('friend_request_id')
			friend_request_id.accept()
			messages.success(request, f'You are now friends with {friend_request_id.sender.username}')
			return redirect('account:profile', user_id=request.user.id)
		else:
			return HttpResponse('Invalid form data.. accept_friend_request_view')
	else:
		messages.error(request, 'Debug: This is a POST-only endpoint')
		return redirect('account:profile', user_id=request.user.id)
...
```

2. Adding the respective url to the `friends/urls.py` file:

```python
...
urlpatterns = [
	...
	path('accept-friend-request/', views.accept_friend_request_view, name='accept_friend_request'),
	...
]
```

#### ***REMOVE FRIEND***

*This will allow the user to remove a friend from their friend list*

1. Adding the `remove_friend_view` function to the `friends/views.py` file:

```python
...
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from friends.forms import SendFriendRequestForm, HandleFriendRequestForm, RemoveFriendForm
from friends.models import FriendRequest, FriendList
from account.models import Account

...
def remove_friend_view(request):
	user = request.user
	# DEBUG #
	# print(request.POST)
	# print(f'this user: {user.id}')
    # # # # #
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
...
```

2. Adding the `RemoveFriendForm` class to the `friends/forms.py` file:

```python
...
class RemoveFriendForm(forms.Form):
	friend_id = forms.ModelChoiceField(queryset=User.objects.all())
```

3. Adding the respective url to the `friends/urls.py` file:

```python
...
urlpatterns = [
	...
	path('remove-friend/', views.remove_friend_view, name='remove_friend'),
	...
]
```


#### ***DECLINE FRIEND REQUEST***


1. Adding the `decline_friend_request_view` function to the `friends/views.py` file:

```python
...
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

```

2. Adding the respective url to the `friends/urls.py` file:

```python
...
urlpatterns = [
	path('decline-friend-request/', views.decline_friend_request_view, name='decline_friend_request'),
]
```


*At this point, hopefully, the users can now send friend requests, cancel friend requests, accept friend requests, decline friend requests, and remove friends from the friend list*


#### ***ADDING FRIENDS LIST PAGE***

*This will allow the user to view their friends list and remove friends from the list*

1. Adding the `friend_list.html` file to the `friends/templates/friends` directory:

```html
{% extends 'layout.html' %}
{% load static %}

{% block content %}

{% if friends %}
	{% for friend in friends %}
		<a href="{% url 'account:profile' user_id=friend.0.pk %}">
			<img src="{{ friend.0.profile_image.url }}" alt="profile_image">
		</a>
		
		<a href="{% url 'account:profile' user_id=friend.0.pk %}">
			<h4>{{ friend.0.username|truncatechars:50 }}</h4>
		</a>

		{% if friend.1 %}
			<a href="#">Send a Message</a>
		{% endif %}
			
		{% if friend.1 %}
			<p> FRIENDS </p>
			<span> check_circle_outline </span>
		{% else %}
			{% if friend.0 !=  request.user %}
				<p> Not Friends </p>
				<span>cancel</span>
			{% endif %}
		{% endif %}

		{% if friend.0 == request.user %}
				<p> This is you </p>
				<span> person_pin </span>
		{% endif %}

	{% endfor %}
	
{% else %} <!-- If no friends -->
	<p>No friends.</p>
{% endif %}
	
{% endblock content %}
```

2. Adding the `friends_list_view` function to the `friends/views.py` file:

```python
...
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
```

3. Adding the respective url to the `friends/urls.py` file:

```python
...
urlpatterns = [
	...
	path('friend-list/<user_id>/', views.friend_list_view, name='friend_list'),
	...
]
```

4. Adding the link to the friend list page in the `profile.html` file in the `account/templates/account` directory:

```html
...
	<!-- Friend list link -->
	<a href="{% url 'friends:friend_list' user_id=id %}">
		<span> Friends ({{ friends|length }}) </span></br>
	</a>
...
```

*At this point, the user can view their friends list at `http://localhost:8000/friends/friend-list/<user_id>/` and remove friends from the list*

5. Modifying the `account/account_search_view` function in the `account/views.py` file:

*This will allow the user to see the friend status of the search results in the search results page*  

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

			if user.is_authenticated:
				user_friend_list = FriendList.objects.get(user=user)
				for account in search_results:
					accounts.append((account, user_friend_list.is_mutual_friend(account)))
				context['accounts'] = accounts
			else:
				for account in search_results:
					accounts.append((account, False)) # False for indicating that the user is not a friend
				context['accounts'] = accounts

	return render(request, 'account/search_results.html', context)
...
```

**This shall conclude the friends system. The user can now send friend requests, cancel friend requests, accept friend requests, decline friend requests, remove friends from the friend list, and view their friends list**  


